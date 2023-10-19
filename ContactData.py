from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import pickle
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1

def save_cookies(driver,filename):
    with open(filename,'wb') as file:
        pickle.dump(driver.get_cookies(),file)

def load_cookies(driver,filename):
    with open(filename,'rb') as file:
        cookies=pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def get_contact_data():
 scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
 credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/shal1/OneDrive/Desktop/extra/pr/marketing-automations-401806-124a6a502fd9.json', scope)

 gc = gspread.authorize(credentials)
 spreadsheet = gc.open('Automated_Data')
 worksheet = spreadsheet.worksheet('Sheet1')
 data = worksheet.get_all_records()
 linkedin_urls = [row['Personal Linkedin URL'] for row in data]
 company_names = [row['Company Name'] for row in data]

 headers = data[0].keys()
 new_column_names = ["Name", "Email", "Phone"]


 for new_column_name in new_column_names:
    if new_column_name not in headers:
        headers = list(headers) + [new_column_name]


 header_cells = worksheet.range(f"A1:{rowcol_to_a1(1, len(headers))}")
 for i, header in enumerate(headers):
    header_cells[i].value = header
 worksheet.update_cells(header_cells)

 options = webdriver.ChromeOptions()
 options.add_extension('./Resources/Apolloio.crx')  
 driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

#login to apollo
# apollo_cookies='apollo_cookies.pkl'
 driver.get('https://app.apollo.io/#/login')

# if os.path.exists(apollo_cookies):
#     print("This apollo login is using cookies")
#     load_cookies(driver, apollo_cookies)
# else:
 username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'o7-input')))
 username_field.send_keys('bhavya.srivastava@ideausher.com')
 time.sleep(4)
 password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'current-password')))
 password_field.send_keys('passwords')
 password_field.send_keys(Keys.RETURN)
 print('You are logged in Apollo!')

    # save_cookies(driver,apollo_cookies)

 time.sleep(4)
# Open the LinkedIn homepage
 Linkedin_cookies='cookies.pkl'
 driver.get('https://www.linkedin.com/')

 if os.path.exists(Linkedin_cookies):
    print("This linkedin login is using cookies")
    load_cookies(driver, Linkedin_cookies)

 else: 
    username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'session_key')))
    username_field.send_keys('bhavyasrivastava012@gmail.com')

    time.sleep(4)

    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'session_password')))
    with open('passwords.txt', 'r') as x:
        password = x.read()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    print('You are logged in!')

    save_cookies(driver, Linkedin_cookies)

 time.sleep(4)

# company_names = []
 emails = []
 phone_numbers = []
 names=[]

 header_row = worksheet.row_values(1)
 name_index = header_row.index("Name") + 1
 email_index = header_row.index("Email") + 1
 phone_index = header_row.index("Phone") + 1

 for linkedin_url, company_name in zip(linkedin_urls, company_names):
  try:
    driver.get(linkedin_url)
    # print(linkedin_url)

    time.sleep(10)

    try:
        view_email = driver.find_element(By.XPATH, "//div[@class='x_xUayd' and div/span[text()='View email address']]")

        
        if view_email.is_displayed():
            view_email.click()
            time.sleep(4)

        view_password = driver.find_element(By.XPATH, "//div[@class='x_xUayd' and div/span[text()='View mobile number']]")

        
        if view_password.is_displayed():
            view_password.click()
            time.sleep(4)

    except Exception as e:
        
        email_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'x_GxQlI')))
        # time.sleep(10)
        email = email_element.text
        # print(email)

        phone_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'x_XitPs')))
        phone = phone_element.text
        # print(phone)
        
    name_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'text-heading-xlarge.inline.t-24.v-align-middle.break-words')))
    name=name_element.text
    # print(name)
    

    emails.append(email)
    phone_numbers.append(phone)
    names.append(name)
    row_index = None
    for index, row in enumerate(data):
        if row['Personal Linkedin URL'] == linkedin_url:
            row_index = index + 2  
            break

    if row_index is not None:
        worksheet.update_cell(row_index, name_index, name)
        worksheet.update_cell(row_index, email_index, email)
        phone = f"'{phone}"
        worksheet.update_cell(row_index, phone_index, phone)

        print(f"Successfully retrieved information for :{name}")
    
  except Exception as e:
        print(f"Error scraping Company: {company_name}. Skipping to the next URL.")
        continue
 print("Sheet Updated with Contact Data")
 driver.quit()

# get_contact_data()
