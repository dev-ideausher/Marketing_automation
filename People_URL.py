import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from urllib.parse import urlparse
import csv
import pickle
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
# from concurrent.futures import ThreadP


def save_cookies(driver,filename):
    with open(filename,'wb') as file:
        pickle.dump(driver.get_cookies(),file)

def load_cookies(driver,filename):
    with open(filename,'rb') as file:
        cookies=pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def get_people_url():
 scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
 credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/shal1/OneDrive/Desktop/extra/pr/marketing-automations-401806-124a6a502fd9.json', scope)


 gc = gspread.authorize(credentials)
 spreadsheet = gc.open('Automated_Data')
 worksheet = spreadsheet.worksheet('Sheet1')


 data = worksheet.get_all_records()
 linkedin_urls = [row['Company LinkedIn'] for row in data]


 headers = data[0].keys()
 new_column_name = "Personal Linkedin URL"
 if new_column_name not in headers:
    headers = list(headers) + [new_column_name]
    worksheet.update('A1', [headers])



 driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

 cookies_file='cookies.pkl'
 driver.get('https://www.linkedin.com/')
 if os.path.exists(cookies_file):
    print("This login is using cookies")
    load_cookies(driver, cookies_file)

 else:
    # driver.get('https://www.linkedin.com/')
    print("This login is using credentials")
    username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'session_key')))
    username_field.send_keys('bhavyasrivastava012@gmail.com')
    time.sleep(4)
    
    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'session_password')))
    with open('passwords.txt', 'r') as x:
        password = x.read()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    print('You are logged in!')

    # Save cookies to a file for future use
    save_cookies(driver, cookies_file)

 data_list = []

 for i, LinkedinURL in enumerate(linkedin_urls):
    try:
        parsed_url = urlparse(LinkedinURL)
        company_name = parsed_url.path.split("/")[-1]
        # time.sleep(4)

        driver.get(LinkedinURL)
        print(LinkedinURL)

        people_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.LINK_TEXT, 'People')))
        people_element.click()

        search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'people-search-keywords')))
        search_bar.send_keys(f"CEO at {company_name}")
        search_bar.send_keys(Keys.RETURN)

        time.sleep(5)

        profile_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-entity-lockup__content.ember-view')))
  
        name_div = WebDriverWait(profile_div, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-entity-lockup__title.ember-view')))

        anchor = WebDriverWait(name_div, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-aware-link.link-without-visited-state')))
   

        href_attribute = anchor.get_attribute('href')
        worksheet.update(f'G{i + 2}', href_attribute)

    except Exception as e:
        # Print an error message if scraping fails for a specific URL
        print(f"Error scraping LinkedIn URL: {LinkedinURL}. Skipping to the next URL.")
        continue

 driver.quit()
 print(f'Profile URLs updated in the Google Sheet')

# get_people_url()
