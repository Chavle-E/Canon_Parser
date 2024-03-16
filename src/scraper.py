from bs4 import BeautifulSoup
from selenium_utils import scroll_to_load_more, wait_for_page_load

BASE_URL = 'https://www.usa.canon.com/'


def scrape_canon_preview(category, driver):
    url = f"https://www.usa.canon.com/shop/cameras/{category}"
    driver.get(url)
    wait_for_page_load(driver)
    # Click Load more to load all the cameras
    scroll_to_load_more(driver, "//button[@class='primary amscroll-load-button' and @amscroll_type='after']")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    amscroll_divs = {}
    for i in range(1, 4):
        amscroll_divs[f'page_{i}'] = soup.find_all('div', attrs={'amscroll-page': str(i)})

    print(amscroll_divs)


    # for product_div in product_divs:
    #     ol = product_div.find('ol', {'id': 'product-items'})
    #     cameras = ol.find_all('li')
    #     for camera in cameras:
    #         name_h2 = camera.find('h2', class_='product name product-item-name')
    #         model = name_h2.find('a', class_='product-item-link').text.strip()
    #         print(model)
