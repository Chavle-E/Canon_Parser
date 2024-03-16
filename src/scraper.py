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

    for page, divs in amscroll_divs.items():
        for div in divs:
            div_html = str(div)
            div_soup = BeautifulSoup(div_html, 'html.parser')

            camera_names = div_soup.find_all('h2', class_='product name product-item-name')
            camera_prices = div_soup.find_all('span', class_='price')
            for name in camera_names:
                model = name.get_text(strip=True)
            for price in camera_prices:
                print(price.get_text(strip=True))



