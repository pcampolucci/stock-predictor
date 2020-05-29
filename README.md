# Important Note
The documentation set of our project may be found in the Group2_EWI3615TU_documentation_set.pdf file. This file contains an overview of our work, right after the "Contents" page. Everything is explained in a more detailed manner in the subsequent chapters of the report. Furthermore, supporting material may be found in the appendices. 

# Predicting Stocks

The script developed by Group 02 provides a user interface that will give the user a few company choices. Once the user selects the company he or she is interested in, the web scraping algorithm updates the values in the database with the latest ones from the web. Once this process is completed, data is ready to be trained. Trained data is then used to make the most recent possible prediction on the stock trend of that company. Predictions are written to .csv files that will be used from the GUI to show the plot the user asked for. Below a diagram helps to understand the process. 

![alt text](/img/image_1.png)

### Requirements

The user must first install the following packages:

- statsmodels
- tensorflow
- apt-pkg
- sklearn
- pandas
- selenium
- xlsxwriter
- webdriver-manager

### Executing the tool



