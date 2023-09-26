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

def save_cookies(driver,filename):
    with open(filename,'wb') as file:
        pickle.dump(driver.get_cookies(),file)

def load_cookies(Driver,filename):
    with open(filename,'rb') as file:
        cookies=pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


options = webdriver.ChromeOptions()
options.add_extension('./Resources/Apolloio.crx')  # Replace with the path to your CRX file

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# driver.get('https://www.linkedin.com/in/lukefrey94/')
# driver.maximize_window()

#login to apollo
apollo_cookies='apollo_cookiers.pkl'
driver.get('https://app.apollo.io/#/login')

if os.path.exists(apollo_cookies):
    print("This apollo login is using cookies")
    load_cookies(driver, apollo_cookies)
else:
    username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'o7-input')))
    username_field.send_keys('bhavya.srivastava@ideausher.com')
    time.sleep(4)
    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'current-password')))
    password_field.send_keys('khushibhavya@007')
    password_field.send_keys(Keys.RETURN)
    print('You are logged in Apollo!')

    save_cookies(driver,apollo_cookies)

time.sleep(4)
# Open the LinkedIn homepage
Linkedin_cookies='cookies.pkl'
driver.get('https://www.linkedin.com/')

if os.path.exists(Linkedin_cookies):
    print("This linkedin login is using cookies")
    load_cookies(driver, Linkedin_cookies)

else: 
# Wait for the user to log in manually or automate the login process
    username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'session_key')))
    username_field.send_keys('bhavyasrivastava012@gmail.com')

    time.sleep(4)

    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'session_password')))
    with open('passswords.txt', 'r') as x:
        password = x.read()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    print('You are logged in!')

    save_cookies(driver, Linkedin_cookies)

time.sleep(4)

csv_file = 'linkedin_results.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)


company_names = []
emails = []
phone_numbers = []
names=[]


for index, row in df.iterrows():
    company_name = row['Company Name']
    linkedin_profile_url = row['Profile URL']

    driver.get(linkedin_profile_url)

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
        email = email_element.text

        phone_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'x_XitPs')))
        phone = phone_element.text
        
    name_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'text-heading-xlarge.inline.t-24.v-align-middle.break-words')))
    name=name_element.text
    print(name)
    

    company_names.append(company_name)
    emails.append(email)
    phone_numbers.append(phone)
    names.append(name)

   
    time.sleep(20)


result_df = pd.DataFrame({'Company Name': company_names, 'Email': emails, 'Phone Number': phone_numbers,'Name':names})


result_csv = 'extracted_info.csv' 
result_df.to_csv(result_csv, index=False)

driver.quit()

