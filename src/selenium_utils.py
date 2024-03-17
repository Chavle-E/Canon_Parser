from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


def wait_for_page_load(driver):
    WebDriverWait(driver,
                  10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))


def find_load_more(driver, xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def scroll_page_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page.")
            break

        last_height = new_height


def scroll_to_load_more(driver, xpath):
    while True:
        try:
            load_more_button = find_load_more(driver, xpath)
            if load_more_button:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                    load_more_button)
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                time.sleep(1)
                load_more_button.click()
                time.sleep(3)
            else:
                print("No more 'Load More' buttons to click.")
                break
        except NoSuchElementException:
            print("The 'Load More' button does not exist.")
            break
        except Exception as e:
            print("Print")
            scroll_page_to_bottom(driver)
            break
