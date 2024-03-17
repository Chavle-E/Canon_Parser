from scraper import scrape_canon_preview, scrape_canon_image, scrape_canon_specs
import json
# import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
ua = UserAgent()
user_agent = ua.random

options.add_argument(f'--user-agent={user_agent}')
driver = webdriver.Chrome(options=options)
cameras = []

categories = ['mirrorless-cameras', 'dslr-cameras', 'compact-cameras']
for category in categories:
    camera_preview = scrape_canon_preview(category, driver)
    cameras.extend(camera_preview)
print(cameras)
for camera in cameras:
    camera['brand'] = 'Canon'
    camera['images'] = scrape_canon_image(camera['detailed_link'], driver)
    specs_data = scrape_canon_specs(camera['detailed_link'], driver)
    camera['pdf'] = specs_data['pdf']
    camera['specs'] = specs_data['specs']

driver.quit()


def save_data(cameras_arg):
    """
    Saves scraped camera data to a JSON file.
    """
    for camera_arg in cameras_arg:
        with open('canon_cameras.json', 'a') as json_file:
            json.dump(camera_arg, json_file, indent=4)
            json_file.write(',\n')


save_data(cameras)
