from selenium import webdriver
from scraper import scrape_canon_preview, scrape_canon_image, scrape_canon_specs
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

# Initialize WebDriver with ChromeOptions
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
cameras = []

# categories = ['mirrorless-cameras', 'dslr-cameras', 'compact-cameras']
# for category in categories:
#     camera_preview = scrape_canon_preview(category, driver)
#     cameras.extend(camera_preview)
# for camera in cameras:
#     camera['brand'] = 'Canon'
#     camera['images'] = scrape_canon_image(camera['detailed_link'], driver)
#     camera['pdf'] = scrape_canon_specs(camera['detailed_link'], driver)['pdf']
#     camera['specs'] = scrape_canon_specs(camera['detailed_link'], driver)['specs']


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
