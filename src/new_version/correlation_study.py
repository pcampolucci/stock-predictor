"""
Title: Correlation study class

Author: Pietro Campolucci
"""

# import packages
from src.new_version.retreive_data import GetDataset
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# get path
path = os.path.dirname(os.path.realpath(__file__)) + "/correlation_plots/"

# DEBUG
DEBUG = True


class Correlation:

    def __str__(self):
        return "Correlation class of " + self.company

    def __init__(self, company, interval, days):
        self.database = GetDataset(company, interval, days).database
        self.company = company

    def plotter(self, filtered_dataset, title):
        filtered_dataset = MinMaxScaler().fit_transform(filtered_dataset)

        with sns.color_palette("Blues_d"):
            plt.figure(figsize=(10, 5))
            sns.set_style('whitegrid', {'grid.linestyle': '--'})
            ax = sns.lineplot(data=filtered_dataset[:, 0], alpha=1, color='r')
            ax = sns.lineplot(data=filtered_dataset[:, 1], alpha=0.5)
            ax = sns.lineplot(data=filtered_dataset[:, 2], alpha=0.5)
            ax.invert_xaxis()
            ax.set_title(f'Normalized values for {self.company}')
            ax.legend(loc='upper left', labels=['Company', 'Euro', 'Oil'])
            ax.set(xlabel='Time - Days in the Past', ylabel='Normalization - Close Value')
            plt.savefig(path + title + self.company + ".pdf")

        return 0

    def plot_close(self):
        close_dataset = self.database[['company_close', 'euro_close', 'oil_close']]
        title = "close_plot_"
        self.plotter(close_dataset, title)
        return 0

    def plot_return(self):
        return_dataset = self.database[['company_return', 'euro_return', 'oil_return']]
        title = "return_plot_"
        self.plotter(return_dataset, title)
        return 0

    def plot_corr_matrix(self):
        corr = self.database[
            ['company_open', 'company_close', 'euro_open', 'euro_close', 'oil_open', 'oil_close', 'company_return',
             'euro_return', 'oil_return']
        ].corr()

        plt.figure(figsize=(8, 4))
        mask = np.triu(np.ones_like(corr, dtype=np.bool))
        corr_plot = sns.heatmap(corr, mask=mask, annot=True)
        corr_plot.set_title(f"Correlation matrix for {company_name}")

        for item in corr_plot.get_xticklabels():
            item.set_rotation(45)

        plt.tight_layout()
        plt.savefig(path + "correlation_matrix_" + self.company + ".pdf")

        return 0


# debugging script =============================================================================================
if DEBUG:
    company_name = "RDS-B"
    interval_test = "1d"
    days_test = 5000
    dataset = Correlation(company_name, interval_test, days_test)
    dataset.plot_close()
    dataset.plot_return()
    dataset.plot_corr_matrix()

