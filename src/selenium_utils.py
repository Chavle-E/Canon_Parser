from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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


def scroll_to_load_more(driver, load_more_xpath=None):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        if load_more_xpath:
            try:
                load_more_button = driver.find_element_by_xpath(load_more_xpath)
                if load_more_button.is_displayed():
                    driver.execute_script("arguments[0].click();", load_more_button)
                    time.sleep(3)
            except Exception as e:
                print(f"No more 'Load More' button to click or error clicking it: {e}")

        scroll_page_to_bottom(driver)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height
