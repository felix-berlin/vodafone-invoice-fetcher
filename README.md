# Vodafone Invoice Fetcher

This script automates the process of logging into a Vodafone account and downloading invoices. It uses Selenium to interact with the Vodafone website.

## Requirements

- Python 3
- Selenium
- ChromeDriver
- pyotp (if using 2FA)

## Usage

You can run the script from the command line with the following arguments:

- `--mode`: The mode to fetch the bills. Options: `last`, `all`. Default is `last`.
- `--username`: Your Vodafone username. This argument is required.
- `--password`: Your Vodafone password. This argument is required.
- `--secret_key`: Your 2FA secret key. This argument is optional.
- `--download_path`: The path where the invoices will be downloaded.
- `--login_url`: The Vodafone login URL. Default is `https://www.vodafone.de/meinvodafone/account/login`.
- `--invoice_overview_url`: The Vodafone invoice overview URL. Default is `https://www.vodafone.de/meinvodafone/services/ihre-rechnungen/rechnungen`.
- `--remote_url`: The URL of the remote Selenium server. This argument is optional.

Here's an example of how to run the script:

```bash
python fetcher.py --mode 'last' --username 'your_username' --password 'your_password' --secret_key 'your_secret_key'
```
