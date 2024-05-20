import pyotp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Fetch the Vodafone bills.')

# Add the arguments
parser.add_argument('--username', type=str, required=True, help='The username')
parser.add_argument('--password', type=str, required=True, help='The password')
parser.add_argument('--secret_key', type=str, required=True, help='The 2FA secret key')
parser.add_argument('--download_path', type=str, default="./downloads", help='The download path for the invoices')

# Parse the arguments
args = parser.parse_args()

# Initialize a WebDriver instance
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": args.download_path, # Change this to your download directory
})

driver = webdriver.Chrome(options=chrome_options)

def initVodafoneInvoiceFetcher(username, password, secret_key):
    # Define the URL for the login request
    login_url = 'https://www.vodafone.de/meinvodafone/account/login'

    driver.get(login_url)

    # Wait for the cookie consent banner and accept it
    cookie_consent_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'dip-consent-summary-reject-all')))
    cookie_consent_button.click()

    # Wait until the username field is present and visible
    username_field = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtUsername')))
    password_field = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtPassword')))

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
    login_button.click()

    totp_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#totpcontrol')))

    totp = pyotp.TOTP(secret_key)
    totp_code = totp.now()
    totp_field.send_keys(totp_code)

    time.sleep(2)
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
    login_button.click()

    time.sleep(10)

    # Navigate to the other page
    driver.get('https://www.vodafone.de/meinvodafone/services/ihre-rechnungen/rechnungen')

    time.sleep(10)

    # Get all the download buttons
    download_buttons = driver.find_elements(By.CSS_SELECTOR, 'svg[automation-id="table_2_svg"]')
    print(download_buttons)
    for button in download_buttons:
        button.click()
        time.sleep(2)  # Add a delay between downloads to avoid overwhelming the server

    time.sleep(60)

initVodafoneInvoiceFetcher(args.username, args.password, args.secret_key)