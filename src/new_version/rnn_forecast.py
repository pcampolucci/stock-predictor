"""
Title: RNN Class for forecast prediction

Author: Pietro Campolucci
"""

# import packages
from src.new_version.retreive_data import GetDataset
from src.new_version.rnn_helpers import make_partitions


# debugging
DEBUG = True


class RNN:

    def __str__(self):
        print(f"RNN for {self.company}\n")

        norm = self.normalize_features()
        print("========= Normalization =========\n")
        print(f"mean normalized dataset of features = \n\n {norm} \n")
        print(f"shape of dataset = {norm.shape}\n")

        train_partitions, train_labels, valid_partitions, valid_labels = self.train_and_test()
        print("========= Train/Test Split =========\n")
        print(f"By considering the contributing variables and the data inserted, we obtain: ")
        print(f"Train data of shape: {train_partitions.shape} and {train_labels.shape}")
        print(f"Validation data of shape: {valid_partitions.shape} and {valid_labels.shape}")
        print('Single window of past history : {}'.format(train_partitions[0].shape))
        print('Single window of predicted output : {}'.format(train_labels[0].shape))

        return "\ndone"

    def __init__(self, company, interval, days, features, train_size, past_size, future_size):
        self.full_data = GetDataset(company, interval, days).database
        self.features = self.full_data[features]
        self.company = company
        self.amount = len(features)
        self.train_size = train_size
        self.past_size = past_size
        self.future_size =future_size

    def show_features(self):
        print(self.features)
        return 0

    def normalize_features(self):
        dataset = self.features.values
        data_mean = dataset.mean(axis=0)
        data_std = dataset.std(axis=0)
        dataset = (dataset - data_mean) / data_std
        return dataset

    def train_and_test(self):
        train_split = int(self.train_size * self.features.shape[0])

        labels = self.normalize_features()[:, 0]  # getting company close
        n_past = self.past_size  # time stamps that will affect the future values (the more the more computing)
        n_prediction = self.future_size  # the time stamp in the future of which we want to find the prediction
        step = 1

        train_partitions, train_labels = make_partitions(self.normalize_features(), labels, 0, train_split,
                                                         n_past, n_prediction, step)

        valid_partitions, valid_labels = make_partitions(self.normalize_features(), labels, train_split, None,
                                                         n_past, n_prediction, step)

        return train_partitions, train_labels, valid_partitions, valid_labels


# debugging script =============================================================================================
if DEBUG:
    company_name = "RDS-B"
    interval_test = "1d"
    days_test = 5000
    feat = ['company_close', 'euro_close', 'oil_close']
    rnn = RNN(company_name, interval_test, days_test, feat, 0.9, 50, 5)
    rnn.normalize_features()
    rnn.train_and_test()
    print(rnn)

