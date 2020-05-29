from bs4 import BeautifulSoup
from selenium import webdriver
import xlsxwriter
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

#name = input("Input the company name:")
name_dict = {"sinopec": "SHI", "shell": "RDS-A", "exxonmobil": "XOM", "lukoil": "LUKOY"}
for name in name_dict:
    print(name)
    #Create .xlsx workbook and sheet
    workbook = xlsxwriter.Workbook(name + '.xlsx')
    worksheet = workbook.add_worksheet()

    #Get information from Yahoo! finance
    url = ('https://finance.yahoo.com/')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_size(480, 320)
    # maximize window
    driver.maximize_window()
    driver.get(url)
    # accept the terms and conditions window
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@name='agree']")))
    driver.find_element_by_xpath("//button[@name='agree']").click()
    # enter name of company
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='yfin-usr-qry']")))
    element.send_keys(name_dict[name])
    time.sleep(2)
    # push search button
    driver.find_element_by_xpath("//button[@id='search-button']").click()
    # Navigate to historical data
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Historical Data')]")))
    driver.find_element_by_xpath("//span[contains(text(),'Historical Data')]").click()
    #Select Time Period
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@class='C($linkColor) Fz(14px)']")))
    driver.find_element_by_xpath("//span[@class='C($linkColor) Fz(14px)']").click()
    # Select time span of 5 years
    driver.find_element_by_xpath("//span[contains(text(),'5Y')]").click()
    # Click done button
    #driver.find_element_by_xpath("//button[contains(@class,'Py(9px) Miw(80px)! Fl(start)')]").click()
    # Click apply button
    try:
        driver.find_element_by_xpath("//div[contains(@class,'M(0) O(n):f D(ib) Bdrs(4px) Fz(s) Pos(a) C($featureCueBgc) Start(0) T(15px)')]//*[contains(@class,'H(18px) W(18px) Va(m)! close:h_Fill(white)! close:h_Stk(white)! Cur(p)')]").click()
        driver.find_element_by_xpath("//button[contains(@class,'Py(9px) Fl(end)')]").click()
    except:
        driver.find_element_by_xpath("//button[contains(@class,'Py(9px) Fl(end)')]").click()

    # Scroll loop, change max_run_time to increase/decrease the tie needed to load the page
    pre_scroll_height = driver.execute_script('return document.body.scrollHeight;')
    run_time, max_run_time = 0, 5
    while True:
        iteration_start = time.time()
        # Scroll webpage, the 100 allows for a more 'aggressive' scroll
        driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')

        post_scroll_height = driver.execute_script('return document.body.scrollHeight;')

        scrolled = post_scroll_height != pre_scroll_height
        timed_out = run_time >= max_run_time

        if scrolled:
            run_time = 0
            pre_scroll_height = post_scroll_height
        elif not scrolled and not timed_out:
            run_time += time.time() - iteration_start
        elif not scrolled and timed_out:
            break

    source = driver.page_source
    # quit the driver in order
    driver.quit()

    #Creating usable HTML from the source
    soup = BeautifulSoup(source, 'lxml')
    #Find the HTML for the table to minimise the amount of data to work with
    table = soup.find('table')\

    #Find all the header values (eg. Date, Open, Close)
    #These are surrounded by the 'th' tag
    col = 0
    for head in table.find_all('th'):
        worksheet.write(0, col, head.span.text)
        col += 1

    #Retrieve all the different values per day
    table_body = table.find('tbody')
    row = 0
    for info in table_body.find_all('tr', limit=None):
        col = 0
        for data in info.find_all('td'):
            worksheet.write(row, col, data.span.text)
            col += 1
        row += 1

    workbook.close()



