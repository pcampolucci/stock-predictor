"""
Title: Helpers set of functions for RNN forecast predictor

Author: Pietro Campolucci
"""

# import packages
import numpy as np


def make_partitions(dataset, label, start, end, past_size, future_size, step, single_step=False):
    """ Legend for names:
        - dataset = all the data
        - label = only the data to be predicted
        - start = starting time for partitions
        - end = ending time for partitions
        - past_size = days in the past used for train
        - future_size = days in future to be predicted
        - step = days considered
    """

    train_data = []
    label_data = []
    start += past_size

    if end is None:
        # then the dataset is finished, adapt to furthest future we have
        end = len(dataset) - future_size

    for datum in range(start, end):
        # make an array of n training batches of m past data collection of x variables (3D array)
        idx = range(datum - past_size, datum, step)
        train_data.append(dataset[idx])

        if single_step:  # then we create batches to predict only in the next observation
            label_data.append(label[datum + future_size])
        else:
            label_data.append(label[datum:datum + future_size])

    return np.array(train_data), np.array(label_data)

