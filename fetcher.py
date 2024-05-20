import pyotp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Fetch the Vodafone bills.')

# Add the arguments
parser.add_argument('--mode', type=str, default="last", help='The mode to fetch the bills. Options: last, all')
parser.add_argument('--username', type=str, required=True, help='The username')
parser.add_argument('--password', type=str, required=True, help='The password')
parser.add_argument('--secret_key', type=str, required=False, help='The 2FA secret key')
parser.add_argument('--download_path', type=str, default=None, help='The download path for the invoices')
parser.add_argument('--login_url', type=str, default="https://www.vodafone.de/meinvodafone/account/login", help='Vodafone login URL')
parser.add_argument('--invoice_overview_url', type=str, default="https://www.vodafone.de/meinvodafone/services/ihre-rechnungen/rechnungen", help='Vodafone invoice overview URL')
parser.add_argument('--remote_url', type=str, default=None, help='The URL of the remote Selenium server')

# Parse the arguments
args = parser.parse_args()

# Initialize a WebDriver instance
chrome_options = Options()

if args.download_path:
  chrome_options.add_experimental_option('prefs',  {
      "download.default_directory": args.download_path, # Change this to your download directory
  })

# Set the capabilities
capabilities = chrome_options.to_capabilities()

if args.remote_url:
    driver = webdriver.Remote(
        command_executor=args.remote_url,
        options=chrome_options
    )
else:
    driver = webdriver.Chrome(options=chrome_options)

def initVodafoneInvoiceFetcher(username, password, secret_key):
    # Open the login page
    driver.get(args.login_url)

    # Wait for the cookie consent banner and accept it
    cookie_consent_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'dip-consent-summary-reject-all')))
    cookie_consent_button.click()

    # Wait until the username field is present and visible
    username_field = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtUsername')))
    password_field = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtPassword')))

    # Fill in the username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Click the login button
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
    login_button.click()

    if secret_key:
      totp_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#totpcontrol')))

      # Generate the TOTP code
      totp = pyotp.TOTP(secret_key)
      totp_code = totp.now()

      # Fill in the TOTP code
      totp_field.send_keys(totp_code)

      # Click the login button
      login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
      login_button.click()

    time.sleep(10)

    # Navigate to the invoice overview page
    driver.get(args.invoice_overview_url)

    time.sleep(10)

    # Get all the download buttons
    download_buttons = driver.find_elements(By.CSS_SELECTOR, 'svg[automation-id="table_2_svg"]')

    if args.mode == "last":
        download_buttons[0].click()
        time.sleep(2)  # Add a delay to allow the download to start

    if args.mode == "all":

      for button in download_buttons:
          button.click()
          time.sleep(2)  # Add a delay between downloads to avoid overwhelming the server

initVodafoneInvoiceFetcher(args.username, args.password, args.secret_key)