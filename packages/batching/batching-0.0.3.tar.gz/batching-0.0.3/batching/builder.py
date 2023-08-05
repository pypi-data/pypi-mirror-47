from .utils import feature_df_to_nn_input, split_flat_df_by_time_gaps

from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

import multiprocessing as mp
from functools import partial
from operator import itemgetter
import logging


class Builder(object):
    def __init__(self,
                 storage,
                 features,
                 look_back,
                 look_forward,
                 n_seconds,
                 batch_size=8192,
                 pseudo_stratify=False,
                 stratify_nbatch_groupings=50,
                 verbose=False,
                 seed=None):
        self.batch_size = batch_size
        self._stratify = pseudo_stratify
        self._stratify_max_groupings = stratify_nbatch_groupings
        self._verbose = verbose

        self._features = features
        self._look_forward = look_forward
        self._look_back = look_back
        self._n_timesteps = look_back + look_forward + 1
        self._n_features = len(features)
        self._n_seconds = n_seconds
        self._logger = logging.getLogger(__name__)

        self._storage = storage

        if seed:
            np.random.seed(seed)

        self.scaler = StandardScaler()

    @staticmethod
    def _remove_false_anchors(df, label):
        anchors = df[label].rolling(3).apply(lambda x: x[0] == 0 and x[1] == 1 and x[2] == 0, raw=True)
        anchors_idx = (np.where(anchors.values == 1)[0] - 1).tolist()
        df.loc[anchors_idx, label] = 0
        return df[label]

    def _nn_input_from_sessions(self, session_df):
        valid_chunks = split_flat_df_by_time_gaps(session_df, self._n_seconds, self._look_back, self._look_forward)
        if not valid_chunks:
            return np.array([]).reshape((0, self._n_timesteps, self._n_features)), np.array([])

        # reformat for sequence models based on window params
        to_sequence = partial(feature_df_to_nn_input, self._features, self._look_back, self._look_forward)
        sequences = list(map(to_sequence, valid_chunks))
        train_data = np.concatenate(list(map(itemgetter(0), sequences)), axis=0)
        train_truth = np.concatenate(list(map(itemgetter(1), sequences)), axis=0)
        return train_data, train_truth

    def _scale_and_transform_session(self, session_df):
        session_df = session_df.dropna()
        session_df.loc[:, self._features] = self.scaler.transform(session_df[self._features])
        session_df["y"] = self._remove_false_anchors(session_df, "y")
        return self._nn_input_from_sessions(session_df)

    def _generate_session_sequences(self, session_df_list):
        with mp.pool.ThreadPool(mp.cpu_count()) as pool:
            for result in pool.imap_unordered(self._scale_and_transform_session, session_df_list):
                yield result

    def _imbalanced_minibatch_generator(self, X, y):
        n_batches = int(X.shape[0] // self.batch_size)
        ones = np.where(y == 1)[0]
        zeros = np.where(y == 0)[0]
        zero_ratio = len(zeros) / float(len(ones) + len(zeros))
        zeros_per_batch = int(self.batch_size * zero_ratio)
        ones_per_batch = int(self.batch_size - zeros_per_batch)

        if self._verbose:
            self._logger.info("balancing {} batches from {} ones and {} zeros".format(n_batches, len(ones), len(zeros)))
        for i in range(n_batches):
            ones_idx = np.random.choice(ones, size=ones_per_batch, replace=False)
            zeros_idx = np.random.choice(zeros, size=zeros_per_batch, replace=False)
            selection = np.concatenate([ones_idx, zeros_idx])
            yield (X[selection], y[selection])

    def _pseudo_stratify_batches(self, session_df_list):
        X_group, y_group = [], []

        group_count = 0
        for (X_batch, y_batch) in self.generate_batches(session_df_list):
            X_group.append(X_batch)
            y_group.append(y_batch)
            group_count += 1
            if group_count >= self._stratify_max_groupings:
                for (X_balanced, y_balanced) in self._imbalanced_minibatch_generator(np.concatenate(X_group, axis=0),
                                                                                     np.concatenate(y_group, axis=0)):
                    yield (X_balanced, y_balanced)
                X_group, y_group = [], []
                group_count = 0

        # yield remaining
        for i in range(group_count):
            yield (X_group[i], y_group[i])

    def save_meta(self):
        params = {
            'batch_size': self.batch_size,
            'features': self._features,
            'look_forward': self._look_forward,
            'look_back': self._look_back,
            'seconds_per_batch': self._n_seconds,
            'mean': self.scaler.mean_.tolist(),
            'std': self.scaler.scale_.tolist()
        }
        self._storage.save_meta(params)

    def load_meta(self):
        params = self._storage.load_meta()
        self.batch_size = params["batch_size"]
        self._features = params["features"]
        self._look_forward = params["look_forward"]
        self._look_back = params["look_back"]
        self._n_seconds = params["seconds_per_batch"]
        self.scaler.mean_ = np.array(params["mean"])
        self.scaler.scale_ = np.array(params["std"])

    def generate_batches(self, session_df_list):
        if self._verbose:
            self._logger.info("Scaling data")
        scale_df = pd.concat(session_df_list, axis=0, ignore_index=True).dropna()

        if self._verbose:
            self._logger.info("Total dataset shape {}".format(scale_df.shape))
        self.scaler.fit(scale_df[self._features])

        X_rem = np.array([]).reshape((0, self._n_timesteps, self._n_features))
        y_rem = np.array([])

        if self._verbose:
            self._logger.info("Generating batches")
        for (X_session, y_session) in self._generate_session_sequences(session_df_list):
            X_session = np.concatenate([X_session, X_rem], axis=0)
            y_session = np.concatenate([y_session, y_rem], axis=0)

            n_batches = int(X_session.shape[0] // self.batch_size)
            remainder = X_session.shape[0] % self.batch_size

            for batch_idx in range(n_batches):
                _bin = batch_idx * self.batch_size
                X = X_session[_bin:_bin + self.batch_size]
                y = y_session[_bin:_bin + self.batch_size]
                yield (X, y)

            X_rem = X_session[-remainder:]
            y_rem = y_session[-remainder:]

    def generate_and_save_batches(self, session_df_list):
        batch_generator = self._pseudo_stratify_batches if self._stratify else self.generate_batches

        for (X_batch, y_batch) in batch_generator(session_df_list):
            assert X_batch.shape[0] == self.batch_size
            assert y_batch.shape[0] == self.batch_size

            self._storage.save(X_batch, y_batch)

        self.save_meta()
