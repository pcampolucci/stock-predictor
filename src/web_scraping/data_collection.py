from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import TimeoutException
import os
from pathlib import Path


path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))


#Get information from Nasdaq
url = ('https://www.nasdaq.com/')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(480, 320)
# maximize window
driver.maximize_window()
driver.get(url)

#accept the terms and conditions window
driver.find_element_by_xpath("/html/body/div[8]/button[3]").click()

#Click the search icon
driver.find_element_by_xpath("//button[@class='primary-nav__search']").click()
element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='search-overlay-input']")))
element.send_keys("BZ:NMX")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Brent Crude (BZ:NMX)')]")))
driver.find_element_by_xpath("//a[contains(text(),'Brent Crude (BZ:NMX)')]").click()

#Scroll to historical data section
find_elem = None
scroll_from = 0
scroll_limit = 1000
while not find_elem:
    sleep(2)
    driver.execute_script("window.scrollTo(%d, %d);" %(scroll_from, scroll_from+scroll_limit))
    scroll_from += scroll_limit
    try:
        find_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='historical-data__footer show']//a[@class='arrow-cta']")))
    except TimeoutException:
        pass

element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='historical-data__footer show']//a[@class='arrow-cta']")))
driver.find_element_by_xpath("//div[@class='historical-data__footer show']//a[@class='arrow-cta']").click()

# choose data for the past 5 years
driver.execute_script("window.scrollTo(0, 500)")
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'5Y')]")))
driver.find_element_by_xpath("//button[contains(text(),'5Y')]").click()

# download excel file for oil prices
driver.find_element_by_xpath("//a[@class='historical-data__download']").click()
sleep(5)
os.replace(path_to_download_folder + '\HistoricalQuotes.csv', "C:/Users/lotha/ewi3615tu-ds2/WebScraping/oil.csv")

#quit driver
driver.quit()

#Get information euro to usd
url = ('https://www.bundesbank.de/dynamic/action/en/statistics/time-series-databases/time-series-databases/745616/745616?dateSelect=2015&listId=www_s331_b01012_3&tsTab=1&tsId=BBEX3.D.USD.EUR.BB.AC.000&id=0')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(480, 320)
# maximize window
driver.maximize_window()
driver.get(url)
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Direct download (CSV)')]")))
driver.find_element_by_xpath("//a[contains(text(),'Direct download (CSV)')]").click()
sleep(10)
os.replace(path_to_download_folder + '\BBEX3.D.USD.EUR.BB.AC.000.csv', "C:/Users/lotha/ewi3615tu-ds2/WebScraping/euro_dollar.csv")

#quit driver
driver.quit()