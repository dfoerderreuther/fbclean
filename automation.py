from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import platform
import logging
import os
import shutil
from comments import delete_comments
from group_comments import delete_group_comments
from likes import delete_likes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    chrome_options = Options()
    # Add any additional options if needed
    # chrome_options.add_argument('--headless')  # Uncomment to run in headless mode
    
    # Specify the correct ChromeDriver version for Mac ARM64
    if platform.system() == 'Darwin' and platform.machine() == 'arm64':
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Add Facebook-specific options
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    
    # Create profile directory in current working directory
    original_profile = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default')
    automation_dir = os.path.join(os.getcwd(), 'chrome_profile')
    automation_profile = os.path.join(automation_dir, 'Default')
    
    # Create the automation directory if it doesn't exist
    if not os.path.exists(automation_dir):
        logging.info("Creating automation profile directory...")
        os.makedirs(automation_dir)
        # Copy the profile if it doesn't exist
        if not os.path.exists(automation_profile):
            logging.info("Copying Chrome profile...")
            shutil.copytree(original_profile, automation_profile)
    
    # Use the automation profile
    chrome_options.add_argument(f'--user-data-dir={automation_dir}')
    
    try:
        # Use the system ChromeDriver installed via Homebrew
        service = Service('/opt/homebrew/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        logging.error(f"Error setting up ChromeDriver: {str(e)}")
        raise

def main():
    driver = setup_driver()

    

    delete_comments(driver)
    # delete_group_comments(driver)
    # delete_likes(driver)

if __name__ == "__main__":
    main() 