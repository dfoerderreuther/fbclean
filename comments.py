from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get target URL from environment variable
TARGET_URL = os.getenv('COMMENTS_URL')
if not TARGET_URL:
    raise ValueError("COMMENTS_URL not found in environment variables")

def delete_comments(driver):
    try:
        logging.info(f"Navigating to {TARGET_URL}")
        driver.get(TARGET_URL)
        
        # Wait for initial page load
        time.sleep(10)

        
        while True:
            try:
                perform_delete_comments(driver)
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



def perform_delete_comments(driver):

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