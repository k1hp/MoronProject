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

driver = webdriver.Chrome(options=options_chrome)

url = 'https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?stock=now-today-tomorrow-later'
driver.get(url)

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
        match = re.fullmatch(r"(.+)\s\[(.+)\]", text)

        if "\n" in price_element.text:
            price = price_element.text.split("\n")[0]
        else:
            price = price_element.text

        if match is None:
            continue
        # Выводим название и цену товара

        print(f"Название: {match.group(1)} Характеристики:{match.group(2)} Цена: {price}")

    try:
        # Ищем кнопку "Следующая страница"
        next_button = driver.find_element(By.CSS_SELECTOR,"a.pagination-widget__page-link.pagination-widget__page-link_next")
        next_button.click() # Кликаем на кнопку "Следующая страница"

        #  Необязательно: Добавляем небольшую задержку
        time.sleep(10)

        page_number += 1

    except NoSuchElementException as e:
        print("Больше нет страниц")
        break # Выходим из цикла, если не нашли кнопку "Следующая страница"

driver.quit()