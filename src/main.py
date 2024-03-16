from selenium import webdriver
from scraper import scrape_canon_preview
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2  # 2 means 'Block'
})

# Initialize WebDriver with ChromeOptions
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


scrape_canon_preview('mirrorless-cameras', driver)

driver.quit()
