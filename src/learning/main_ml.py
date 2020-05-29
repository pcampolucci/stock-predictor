"""
MAIN SCRIPT FOR STOCK MARKET PREDICTION

MAIN FUNCTIONALITY:
- Scripts receives the category of the company and the name of the company
- The web scraping gets to work and sends to a local folder the csv files to interpret
- The scripts then waits for the web scraping to be done, then it seeks and extract the values it needs
- The scripts makes the prediction up to 30 days, these information will then be sent to the GUI and plotted directly as a graph

REQUIREMENTS:
- statsmodels
- tensorflow
- apt-pkg

"""

# Import packages

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import csv
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy
import scipy.linalg
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from helpers import *

import warnings  
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.preprocessing.text import Tokenizer

mpl.rcParams['figure.figsize'] = (8, 3)
mpl.rcParams['axes.grid'] = False

# 0) SIMULATE INFORMATION RETRIEVAL FROM GUI AND DATA STORAGE FROM DATA SCRAPING

def separator():
    print("=" * 100, "\n")

separator()
print("Predictor Algorithm started ...\n")
company = input("Simulating Automated KeyWord (eni, shell, total): ")
print("\n")

# scrape data based on the user input and store them as csv/excel with the name of the user input
separator()
print(f"Retreiving data from database and building batches ...")

# 1) GET DATA AND REORGANIZE IT

path = os.getcwd() + "/database/"
files = [str(company) + ".csv", "crude_oil.csv", "euro_to_usd.csv"]

cols = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
target = pd.read_csv(path + files[0])
target = target.dropna()
target['Open'] = target['Open'].astype(float)

factor_1 = pd.read_csv(path + files[1])
factor_2 = pd.read_csv(path + files[2])

target = target.assign(factor_1 = factor_1[' value'])  # e.g. crude oil
target = target.assign(factor_2 = factor_2[' value'])  # e.g. euro_to_usd

# add gradients to database
n_days = 5

target = target.assign(factor_1_change = np.gradient(target["factor_1"].shift(n_days) - target["factor_1"].shift(n_days + 1)))
target = target.assign(factor_2_change = np.gradient(target["factor_2"].shift(n_days) - target["factor_2"].shift(n_days + 1)))
target = target.assign(RETURN = (target["Close"] - target["Open"]))
target = target.dropna()

print(f" DATA CONSIDERED:\n {target.head()} \n")

# 2) BUILD MACHINE LEARNING TOOL AND GET PREDICTIONS

separator()
print(f"Shaping data ...")

features_considered = ['factor_1', 'factor_2', 'factor_1_change', 'factor_2_change', 'Close']

features = target[features_considered]
features.index = target['Date']

train_split = 1000  # TODO make it proportional to the total number automatically

# normalize the dataset for better interpretation (mean normalization)
dataset = features.values
data_mean = dataset[:train_split].mean(axis=0)
data_std = dataset[:train_split].std(axis=0)

dataset = (dataset-data_mean)/data_std

print(f"mean normalized dataset of features = \n\n {dataset} \n")

print(f"shape of dataset = {dataset.shape}")

# batches definition
labels = dataset[:, -1]  # values to predict (in this case "Close")
n_past = 50  # time stamps that will affect the future values (the more the more computing)
n_prediction = 30  # the time stamp in the future of which we want to find the prediction
STEP = 1

train_batches, train_labels = make_batches(dataset, labels, 0, train_split, n_past, n_prediction, STEP)
valid_batches, valid_labels = make_batches(dataset, labels, train_split, None, n_past, n_prediction, STEP)

print(f"By considering 5 contributing variables and the data instered, we obtain: ")
print(f"\nTrain data of shape: {train_batches.shape} and {train_labels.shape}")
print(f"\nValidation data of shape: {valid_batches.shape} and {valid_labels.shape}\n")
print ('Single window of past history : {}'.format(train_batches[0].shape), "\n")
print ('Single window of predicted output : {}'.format(train_labels[0].shape), "\n")

BATCH_SIZE = 100 # single example batch size
BUFFER_SIZE = 1000 # level of randomness

separator()
print(f"Training session started ... ")

train = tf.data.Dataset.from_tensor_slices((train_batches, train_labels))
train = train.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()

validate = tf.data.Dataset.from_tensor_slices((valid_batches, valid_labels))
validate = validate.batch(BATCH_SIZE).repeat()

# Build prediction model by specifying the techniques
sequential = tf.keras.models.Sequential()
lstm_model = sequential

lstm_model.add(tf.keras.layers.LSTM(32,
                                    return_sequences=True,
                                    input_shape=train_batches.shape[-2:]))  # 32 units

lstm_model.add(tf.keras.layers.LSTM(16,
                                    activation='relu'))  # 32 unitstrain_batches.shape[-2:])) # 32 units

lstm_model.add(tf.keras.layers.Dense(30))  # 1 unit

lstm_model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')

# train the model
EVALUATION_INTERVAL = 200
EPOCHS = 10

trained_alg = lstm_model.fit(train, epochs=EPOCHS,
                                            steps_per_epoch=EVALUATION_INTERVAL,
                                            validation_data=validate,
                                            validation_steps=30)

print("\n")
separator()
print("Training completed!\n")
print("Plotting train history\n")

# plot training overview
plot_train_history(trained_alg)

unknown = dataset[-50:, :]
unknown = unknown[np.newaxis, ...]

x_past, y_past, x_future, y_future = get_data_for_plot(unknown[0], lstm_model.predict(unknown)[0])

# bring the values back to the originals
y_past = (y_past + data_mean[-1]) * data_std[-1]
y_future = (y_future + data_mean[-1]) * data_std[-1]

plt.figure()
plt.title(f"Future prediction about {company}")
plt.plot(x_past, y_past, label="Recent Trend")
plt.plot(x_future, y_future, label="Prediction")
plt.legend(loc = "upper left")
plt.xlabel("Time (days)")
plt.ylabel("Close value")
plt.show()

# write predicted data to file
separator()
filename = path + "predictions/" + str(company) + "_prediction.csv"
print(f"Writing data to {filename}\n")

with open(filename, mode='w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow([x_past])
    writer.writerow([y_past])
    writer.writerow([x_future])
    writer.writerow([y_future])

separator()

