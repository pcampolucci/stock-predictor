"""
Helpers script for main correct operation
"""
import numpy as np
import matplotlib.pyplot as plt


def make_batches(dataset, label, start, end, past_size, future_size, step, single_step=False):
    """ The function will divide the dataset in batches of steps defined by the user """

    data = []
    labels = []

    start += past_size

    if end is None:
        # then the dataset is finished, adapt to furthest future we have
        end = len(dataset) - future_size

    for datum in range(start, end):
        # make an array of n training batches of m past data collection of x variables (3D array)
        idx = range(datum - past_size, datum, step)
        data.append(dataset[idx])

        if single_step:  # then we create batches to predict only in the next observation
            labels.append(label[datum + future_size])

        else:
            labels.append(label[datum:datum + future_size])

    return np.array(data), np.array(labels)


def plot_train_history(history):
    # from the trained algorithm is possible to retieve the loss data during training and validation
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # the x axis corresponds to the epochs that we performed
    epochs = range(len(loss))

    # plot the values
    plt.figure()

    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title(f"Behavior or loss factor along {epochs} epochs")
    plt.legend()

    plt.show()


def get_time(length):
    time = []
    for step in range(-length, 0, 1):
        time.append(step)

    return time


def show_plot(plot_data, delta, title):
    labels = ['History', 'True Future', 'Model Prediction']
    marker = ['.-', 'rx', 'go']
    time_steps = get_time(plot_data[0].shape[0])
    if delta:
        future = delta
    else:
        future = 0

    plt.title(title)
    for i, x in enumerate(plot_data):
        if i:
            plt.plot(future, plot_data[i], marker[i], markersize=10, label=labels[i])
        else:
            plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])

    plt.legend()
    plt.xlim([time_steps[0], (future + 5) * 2])
    plt.xlabel('Time-Step')
    return plt


def multi_step_plot(history, true_future, prediction, sample_n):
    plt.figure(figsize=(8, 4))
    plt.title(f"30 days prediction for sample {sample_n+1}")
    num_in = get_time(len(history))
    num_out = len(true_future)

    plt.plot(num_in, np.array(history[:, -1]), label='History')
    plt.plot(np.arange(num_out)/STEP, np.array(true_future), 'bo',
           label='True Future')
    if prediction.any():
        plt.plot(np.arange(num_out)/STEP, np.array(prediction), 'ro',
             label='Predicted Future')
    plt.legend(loc='upper left')
    plt.xlabel('Time')
    plt.ylabel('Close (Normalized)')
    plt.show()

def get_data_for_plot(history, prediction):

    time_history = np.array(get_time(len(history)))
    close_history = np.array(history[:, 1])
    time_future = np.arange(prediction.shape[0])
    close_future = np.array(prediction)

    return time_history, close_history, time_future, close_future



