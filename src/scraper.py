from bs4 import BeautifulSoup
from selenium_utils import scroll_to_load_more, wait_for_page_load
from schema import CanonPreview, ImageURLS

BASE_URL = 'https://www.usa.canon.com/'


def scrape_canon_preview(category, driver):
    url = f"https://www.usa.canon.com/shop/cameras/{category}"
    driver.get(url)
    wait_for_page_load(driver)
    # Click Load more to load all the cameras
    scroll_to_load_more(driver, "//button[@class='primary amscroll-load-button' and @amscroll_type='after']")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    category = soup.find('h1', class_="product-item-name").get_text(strip=True)
    amscroll_divs = {}
    for i in range(1, 4):
        amscroll_divs[f'page_{i}'] = soup.find_all('div', attrs={'amscroll-page': str(i)})
    validated_data = []
    for page, divs in amscroll_divs.items():
        for div in divs:
            div_html = str(div)
            div_soup = BeautifulSoup(div_html, 'html.parser')

            camera_names = div_soup.find_all('h2', class_='product name product-item-name')
            price_spans = div_soup.find_all('span', class_='normal-price')
            for name, price_span in zip(camera_names, price_spans):
                camera_dict = {
                    'model': name.get_text(strip=True),
                    'price': price_span.find('span', class_='price').get_text(strip=True),
                    'detailed_link': name.find('a', class_='product-item-link').get('href'),
                    'category': category
                }

                CanonPreview.parse_obj(camera_dict)
                validated_data.append(camera_dict)

    return validated_data


def scrape_canon_image(url, driver):
    driver.get(url)
    wait_for_page_load(driver)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    photos = soup.find_all('div', class_='fotorama__thumb fotorama__loaded fotorama__loaded--img')
    image_urls = []
    for photo in photos:
        image_urls.append(photo.find('img', class_='fotorama__img')['src'])

    ImageURLS.parse_obj({'images': image_urls})

    return image_urls


def scrape_canon_specs(url, driver):
    driver.get(url)
    wait_for_page_load(driver)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    spec_classes = " ".join(['tech-spec', 'xml', 'cms-accordion', 'attr-group-info'])
    pdf_classes = " ".join(['tech-spec', 'pdf', 'cms-accordion', 'attr-group-info'])

    spec_divs = soup.find_all('div', class_=lambda x: x and spec_classes in x)
    pdf_div = soup.find('div', class_=lambda y: y and pdf_classes in y)
    specs_data = []
    for specs in spec_divs:
        keys = specs.find_all('div', class_='tech-spec-attr attribute')
        values = specs.find_all('div', class_='tech-spec-attr attribute-value')
        for key, value in zip(keys, values):
            key_text = key.get_text(strip=True)
            value_text = value.get_text(strip=True)
            specs_data.append({key_text: value_text})

    final_data = {
        'specs': specs_data if specs_data else None,
        'pdf': pdf_div.find('a')['href'] if pdf_div and pdf_div.find('a') else None
    }

    return final_data

