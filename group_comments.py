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
TARGET_URL = os.getenv('GROUP_COMMENTS_URL')
if not TARGET_URL:
    raise ValueError("GROUP_COMMENTS_URL not found in environment variables")

def delete_group_comments(driver):
    try:
        logging.info(f"Navigating to {TARGET_URL}")
        driver.get(TARGET_URL)
        
        # Wait for initial page load
        time.sleep(10)

        iteration_count = 0
        
        while True:
            try:
                perform_delete_group_comments(driver)
                iteration_count += 1
                logging.info(f"Completed iteration {iteration_count}")
                
                # Reload page every 10 iterations
                if iteration_count % 10 == 0:
                    logging.info("Reloading page after 10 iterations")
                    driver.get(TARGET_URL)
                    time.sleep(5)  # Wait for page to load
                
            except Exception as e:
                logging.error(f"Error in iteration: {str(e)}")
                # Wait a bit before retrying
                time.sleep(5)

            


    except KeyboardInterrupt:
        logging.info("\nScript stopped by user")
    finally:
        driver.quit()
        logging.info("Browser closed")



def perform_delete_group_comments(driver):

    try:
        logging.info("Waiting for checkbox...")
        # Wait for and select the checkbox

        # Click action options
        action_options = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Action options']"))
        )
        action_options.click()
        logging.info("Action options clicked")

        time.sleep(0.1)

        # Click menuitem
        menuitem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Delete') or contains(text(), 'Move to trash')]"))
            #EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='menuitem'][tabindex='0']"))
        )
        menuitem.click()
        logging.info("Menuitem clicked")
        time.sleep(0.1)

        # Click delete span
        delete_span = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "(//span[text()='Delete'])[2] or (//span[text()='Move to Trash'])"))
        )
        delete_span.click()
        logging.info("Delete button clicked")
        time.sleep(1)
        # Wait for page reload
        logging.info("Waiting for page reload...")
        time.sleep(1)  # Increased wait time for Facebook's processing
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise 