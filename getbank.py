from time import sleep

import undetected_chromedriver as uc 
from selenium import webdriver
from datetime import datetime,timedelta
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
import sys

def extract_table_data(driver):
    #click 'Query'button
    click_query = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[1]/div/div/div/mbb-information-account/mbb-source-account/div/div[4]/div/div[1]/form/div[3]/div[2]/button'))
    )
    ActionChains(driver).click(click_query).perform()
    print('query clicked...')
    sleep(3)

    # extract table data
    
    table_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'table-striped'))
    )
    
    rows = table_element.find_elements(By.TAG_NAME, 'tr')
    table_data = []
    with open('extract_data.txt', mode='w', encoding='utf-8') as log_file:
        log_file.write(' ' + '\n')

    for row in rows:
        header_rows = row.find_elements(By.TAG_NAME, "th")
        h_row_data = [h_cell.text for h_cell in header_rows]
        table_data.append(h_row_data)
        with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
            log_file.write(' '.join(h_row_data) + '\n')

        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]
        table_data.append(row_data)
        with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
            log_file.write(' '.join(row_data) + '\n')
    sleep(10)
    sleep(10)
    print('again extract data...')
    extract_table_data(driver)
def extract_data(driver):
    # menu click
    signed = WebDriverWait(driver, 500000000).until(
        EC.visibility_of_element_located((By.ID, 'MNU_GCME_040000'))
    )
    ActionChains(driver).click(signed).perform()
    login_time = datetime.now()
    login_time_history = login_time.strftime("%#d/%#m/%Y/%Hh/%Mm/%Ss")
    with open('login_history.txt', mode='a', encoding='utf-8') as log_file:
        log_file.write(login_time_history + '\n')

    sub_meun = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, 'MNU_GCME_040001'))
    )
    ActionChains(driver).click(sub_meun).perform()
    sleep(13)
    # input end and start_date
    WebDriverWait(driver, 500).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'chartjs-render-monitor'))
    )

    current_date = datetime.now()
    end_date = current_date.strftime("%#d/%#m/%Y")
    diff_date = current_date - timedelta(days=1)
    start_date = diff_date.strftime("%#d/%#m/%Y")
    # print('_______')
    # WebDriverWait(driver, 500).until(
    #     EC.visibility_of_element_located((By.CLASS_NAME, 'mat-form-field-autofill-control'))
    # )
    # print('ffffffffffffff')
    # _date_input = driver.find_element(By.CLASS_NAME,'mat-form-field-autofill-control')
    # _date_input[1].send_keys(start_date)

    
    print('extract success!!!')
    extract_table_data(driver)
    
    sleep(60*4)
    sys.exit()

if __name__ == "__main__":
 
    file_name = f'.\\setting.json'
    with open(file_name) as file:
        info = json.load(file)

    driver = webdriver.Chrome()
    url = "https://online.mbbank.com.vn/pl/login?returnUrl=%2F"
    driver.get(url)
    driver.maximize_window()
    print('open chrome...')

    user_name = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, 'user-id'))
    )
    user_name.send_keys(info['USER_NAME'])

    password = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, 'new-password'))
    )
    password.send_keys(info['PASSWORD'])
    print('please type code.')
    try:
        extract_data(driver)
    except Exception as e:
        login_time = datetime.now()
        login_time_history = login_time.strftime("%#d/%#m/%Y/%Hh/%Mm/%Ss")
        with open('login_history.txt', mode='a', encoding='utf-8') as log_file:
            log_file.write(e + login_time_history + '\n')
        extract_data(driver)
