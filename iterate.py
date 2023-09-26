import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # You may need to specify the path to your WebDriver executable

# Load your CSV file containing company names and LinkedIn URLs
csv_file = 'linkedin_results.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Create empty lists to store extracted information
company_names = []
emails = []
phone_numbers = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    company_name = row['Company Name']
    linkedin_profile_url = row['Profile URL']

    # Navigate to the LinkedIn profile using the provided URL
    driver.get(linkedin_profile_url)

    time.sleep(10)

    try:
        view_email = driver.find_element(By.XPATH, "//div[@class='x_xUayd' and div/span[text()='View email address']]")

        # Check if the element is displayed before clicking
        if view_email.is_displayed():
            view_email.click()
            time.sleep(4)

        view_password = driver.find_element(By.XPATH, "//div[@class='x_xUayd' and div/span[text()='View mobile number']]")

        # Check if the element is displayed before clicking
        if view_password.is_displayed():
            view_password.click()
            time.sleep(4)

    except Exception as e:
        # Handle the case where the elements are not found or not visible
        email_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'x_GxQlI')))
        email = email_element.text

        phone_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'x_XitPs')))
        phone = phone_element.text

    # Append extracted information to the respective lists
    company_names.append(company_name)
    emails.append(email)
    phone_numbers.append(phone)

    # Wait for 20 seconds before proceeding to the next profile
    time.sleep(20)

# Create a new DataFrame with the extracted information
result_df = pd.DataFrame({'Company Name': company_names, 'Email': emails, 'Phone Number': phone_numbers})

# Save the DataFrame to a new CSV file
result_csv = 'extracted_info.csv'  # Replace with your desired CSV file path
result_df.to_csv(result_csv, index=False)

# Close the WebDriver after processing all profiles
driver.quit()

