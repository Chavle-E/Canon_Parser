import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from scraper import scrape_canon_preview, scrape_canon_image, scrape_canon_specs
from mongo import collection
import json
from fake_useragent import UserAgent
import random
from chatgpt import generate_description


# Adding Options to webdriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--incognito")

# Generating random user-agents
ua = UserAgent()
user_agent = ua.random

chrome_options.add_argument(f'--user-agent={user_agent}')


driver = webdriver.Chrome(options=chrome_options)
cameras = []

categories = ['compact-cameras']
for category in categories:
    camera_preview = scrape_canon_preview(category, driver)
    cameras.extend(camera_preview)

for camera in cameras:
    camera['brand'] = 'Canon'
    camera['images'] = scrape_canon_image(camera['detailed_link'], driver)
    specs_data = scrape_canon_specs(camera['detailed_link'], driver)
    camera['pdf'] = specs_data['pdf']
    camera['specs'] = specs_data['specs']
    camera["description"] = generate_description(camera)
    for i in range(random.randrange(1, 3)):
        time.sleep(i)


driver.quit()


def save_data(cameras_arg):
    """
    Saves scraped camera data to a JSON file.
    """
    for camera_arg in cameras_arg:
        with open('canon_cameras.json', 'a') as json_file:
            json.dump(camera_arg, json_file, indent=4)
            json_file.write(',\n')


collection.insert_many(cameras)
