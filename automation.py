from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import platform
import logging
import os
import shutil

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

def perform_actions(driver):
    try:
        logging.info("Waiting for checkbox...")
        # Wait for and select the checkbox
        checkbox = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "comet_activity_log_select_all_checkbox"))
        )
        checkbox.click()
        logging.info("Checkbox clicked")
        
        logging.info("Looking for Remove span...")
        # Click on the "Remove" span
        remove_span = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Remove']"))
        )
        remove_span.click()
        logging.info("Remove span clicked")
        
        logging.info("Waiting for confirmation dialog...")
        # Wait for and handle the confirmation dialog
        confirmation_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Remove Interaction?']"))
        )
        
        logging.info("Sleep 1 second")
        time.sleep(1) 
        logging.info("Looking for Remove button in dialog...")
        try:
            # Wait for the button to be both visible and clickable
            remove_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@aria-label='Remove'])[2]"))
            )
            logging.info("Successfully found Remove button")
            
            # Try multiple click methods
            try:
                # First try regular click
                logging.info("Sleep 1 second")
                time.sleep(1) 
                remove_button.click()
            except:
                try:
                    # If that fails, try JavaScript click
                    parent = remove_button.find_element(By.XPATH, "..")
                    driver.execute_script("arguments[0].click();", parent)
                except Exception as e:
                    logging.error(f"All click attempts failed: {str(e)}")
                    raise
            
            logging.info("Remove button clicked")
        except Exception as e:
            logging.error(f"Failed to find Remove button: {str(e)}")
            raise
        
        # Wait for page reload
        logging.info("Waiting for page reload...")
        time.sleep(10)  # Increased wait time for Facebook's processing
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

def main():
    driver = setup_driver()
    try:
        target_url = "https://www.facebook.com/100000618339720/allactivity?activity_history=false&category_key=COMMENTSCLUSTER&manage_mode=false&should_load_landing_page=false"
        logging.info(f"Navigating to {target_url}")
        driver.get(target_url)
        
        # Wait for initial page load
        time.sleep(10)
        
        while True:
            try:
                perform_actions(driver)
                logging.info("Completed one iteration")
            except Exception as e:
                logging.error(f"Error in iteration: {str(e)}")
                # Wait a bit before retrying
                time.sleep(5)
            
    except KeyboardInterrupt:
        logging.info("\nScript stopped by user")
    finally:
        driver.quit()
        logging.info("Browser closed")

if __name__ == "__main__":
    main() 