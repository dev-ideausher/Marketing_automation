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


def save_cookies(driver,filename):
    with open(filename,'wb') as file:
        pickle.dump(driver.get_cookies(),file)

def load_cookies(Driver,filename):
    with open(filename,'rb') as file:
        cookies=pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_csv_data(csv_file):
    linkedin_urls=[]
    with open(csv_file,mode='r', newline='')as file:
        reader=csv.DictReader(file)
        for row in reader:
            linkedin_url=row.get('linkedin', '')
            if linkedin_url:
                linkedin_urls.append(linkedin_url)
    return linkedin_urls

csv_file='company_data.csv'
linkedin_urls=get_csv_data(csv_file)

print(linkedin_urls)

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
    with open('passswords.txt', 'r') as x:
        password = x.read()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    print('You are logged in!')

    # Save cookies to a file for future use
    save_cookies(driver, cookies_file)

data_list = []

for LinkedinURL in linkedin_urls:
   parsed_url = urlparse(LinkedinURL)

   company_name = parsed_url.path.split("/")[-1]
   time.sleep(4)

   driver.get(LinkedinURL)

   people_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.LINK_TEXT, 'People')))
   people_element.click()

   search_bar=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'people-search-keywords')))
   search_bar.send_keys(f"CEO at {company_name}")
   search_bar.send_keys(Keys.RETURN)

   time.sleep(5)
# people_div=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,'artdeco-card.org-people-profile-card__card-spacing.org-people__card-margin-bottom')))

# child_DIV = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID,'ember1152')))
   profile_div=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'artdeco-entity-lockup__content.ember-view')))
   name_div=WebDriverWait(profile_div,10).until(EC.presence_of_element_located((By.CLASS_NAME,'artdeco-entity-lockup__title.ember-view')))
   anchor=WebDriverWait(name_div,10).until(EC.presence_of_element_located((By.CLASS_NAME,'app-aware-link.link-without-visited-state')))



   href_attribute = anchor.get_attribute('href')

   data_list.append({'Company Name': company_name, 'Profile URL': href_attribute})


driver.quit()


output_csv_file = 'linkedin_results.csv'

with open(output_csv_file, mode='w', newline='') as output_file:
    fieldnames = ['Company Name', 'Profile URL']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)

print(f'Results saved to {output_csv_file}')
