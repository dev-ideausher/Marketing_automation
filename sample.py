from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Define the path to the Edge WebDriver executable
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    # Navigate to Amazon
    driver.get('https://www.amazon.in')
    driver.maximize_window()

    # Click the menu button
    menu_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'nav-hamburger-menu')))
    menu_btn.click()

    # Click the login button
    login_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'hmenu-customer-name')))
    login_btn.click()

    # Enter username and submit
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ap_email')))
    username_field.send_keys('bhavyasrivastava012@gmail.com')
    username_field.send_keys(Keys.RETURN)

    # Enter password and submit
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ap_password')))
    password = 'govind9628370719'
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    print('You are logged in!')

    # Search for "Spiderman Statue"
    search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))
    search_field.send_keys('T-shirt')
    search_loop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'nav-right')))
    search_loop.click()

    print('The search was made successfully!')

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the browser
    driver.quit()
