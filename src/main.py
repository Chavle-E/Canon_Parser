from scraper import scrape_canon_preview, scrape_canon_image, scrape_canon_specs
import json
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={agent}')

driver = uc.Chrome(options=options)
cameras = []

categories = ['mirrorless-cameras', 'dslr-cameras', 'compact-cameras']
for category in categories:
    camera_preview = scrape_canon_preview(category, driver)
    cameras.extend(camera_preview)

for camera in cameras:
    print(camera['detailed_link'])
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
