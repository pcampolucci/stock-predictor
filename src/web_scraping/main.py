"""
Web Scraping Algorithm

REQUIREMENTS:
- selenium
- xlsxwriter
- webdriver-manager
"""


import base
import data_collection
import csv
import xlrd
import os

def csv_from_excel(filename):
    wb = xlrd.open_workbook(filename + '.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(filename + '_input.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

#run the files
base
data_collection

#combine the data collected by the base file and by the data_collection file

name_dict = {"sinopec": "SHI", "shell": "RDS-A", "exxonmobil": "XOM", "lukoil": "LUKOY"}

#Extract information from oil price file and eur to dollar conversion file
oil_price = []
conversion_rate = []

with open('oil.csv', 'r') as oil_file:
    oil_data = csv.reader(oil_file, delimiter=',')
    next(oil_data)
    for row in oil_data:
        if row[0] != '12/05/2018':
            oil_price.append(row[1])

with open('euro_dollar.csv', 'r') as conversion_file:
    conversion_data = csv.reader(conversion_file, delimiter=',')
    for i in range(5):
        next(conversion_data)

    for row in conversion_data:
        if row[1] != "." and row[0] != '05/12/2018':
            conversion_rate.append(row[1])

conversion_rate = conversion_rate[:len(conversion_rate)-2]
conversion_rate.reverse()

#create csv file from xlsx file
for file in name_dict:
    filename = file
    csv_from_excel(filename)
    os.remove(filename + '.xlsx')

for file in name_dict:
    filename_input = file + '_input.csv'
    filename = file + '.csv'

    with open(filename_input, 'r') as input_file:
        with open(filename, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            reader = csv.reader(input_file)
            count = 0
            writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adj close', 'Volume', 'Oil Price', 'EUR/USD'])
            for row in reader:
                if row == [] or row[1] == "Dividend":
                    pass
                else:
                    writer.writerow(row + [oil_price[count]] + [conversion_rate[count]])
                    count += 1
    os.remove(file + '_input.csv')




