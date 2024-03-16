from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


def wait_for_page_load(driver):
    WebDriverWait(driver,
                  10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(3)


def find_load_more(driver, xpath):
    return WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )


def scroll_to_load_more(driver, xpath):
    while True:
        try:
            load_more_button = find_load_more(driver, xpath)
            if load_more_button:
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                    load_more_button)
                time.sleep(3)
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(3)
            else:
                print("No more 'Load More' buttons to click.")
                break
        except NoSuchElementException:
            print("The 'Load More' button does not exist.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
