from selenium import webdriver
from scraper import scrape_canon_preview, scrape_canon_image
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

# Initialize WebDriver with ChromeOptions
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
cameras = []

categories = ['mirrorless-cameras', 'dslr-cameras', 'compact-cameras']
for category in categories:
    camera_preview = scrape_canon_preview(category, driver)
    cameras.extend(camera_preview)
for camera in cameras:
    camera['images'] = scrape_canon_image(camera['detailed_link'], driver)



driver.quit()
