import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# передаем в настройки браузера юзер дату с куки
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument(r'user-data-dir=C:\Users\remge\AppData\Local\Google\Chrome\User Data')

urls = [
    "https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/?stock=now-today-tomorrow-later",
    "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=6&stock=now-today-tomorrow-later",
    "https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?stock=now-today-tomorrow-later",
    "https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaya-pamyat-dimm/?stock=now-today-tomorrow-later&f[1b]=d4w-68vs",
    "https://www.dns-shop.ru/catalog/17a89c2216404e77/bloki-pitaniya/?stock=now-today-tomorrow-later&fr[89h]=500-1550&f[5w]=240-4y-241-4v-117p-242",
    "https://www.dns-shop.ru/catalog/dd58148920724e77/ssd-m2-nakopiteli/?stock=now-today-tomorrow-later&fr[1h7]=239-8000"
]

re_shablon = [r"(.+)\s\[(.+)\]", r"(.+)\s\[.+\]\s\[(.+)\]", r"(.+)\s\[(.+)\]",
              r"(.+)\s\[.+\]\s.+\s\[(.+)\]", r"(.+)\s\[.+\]\s.+\s\[(.+)\]", r"(.+)\s\[.+\]\s\[(.+)\]"]


def parser(url,re_shablon):

    driver = webdriver.Chrome(options=options_chrome)

    parser_url = url
    driver.get(parser_url)

    page_number = 1
    while True:

        print(f"Страница: {page_number}")

        products = driver.find_elements(By.CLASS_NAME, "catalog-product")
        # Проходимся по карточкам товаров
        for product in products:
            try:
                # Находим название и цену товара внутри текущей карточки
                name_element = product.find_element(By.CSS_SELECTOR, "div.catalog-product__name-wrapper")
                price_element = product.find_element(By.CSS_SELECTOR, "div.product-buy__price")
            except NoSuchElementException as e:
                continue

            text = name_element.text
            match = re.fullmatch(re_shablon, text)

            if "\n" in price_element.text:
                price = price_element.text.split("\n")[0]
            else:
                price = price_element.text

            if match is None:
                continue


            print(f"Название: {match.group(1)} Характеристики:{match.group(2)} Цена: {price}")


        try:
            # Ищем кнопку "Следующая страница"
            next_button = driver.find_element(By.CSS_SELECTOR,"a.pagination-widget__page-link.pagination-widget__page-link_next")
            next_button.click() # Кликаем на кнопку "Следующая страница"

            time.sleep(5)

            page_number += 1

        except NoSuchElementException as e:
            print("Больше нет страниц")
            break # Выходим из цикла, если не нашли кнопку "Следующая страница"

    driver.quit()

for i in range(len(urls)):
    parser(urls[i],re_shablon[i])