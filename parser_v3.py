import undetected_chromedriver as UC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

urls = [
    "https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/?stock=now-today-tomorrow-later&f[1zs]=cln9-1p2j-agnc-68te-gfw3&f[13]=bn-bo-bq-1ox-1oz-1qs-br-234&f[1b]=d4w-68vs",
    "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=6&stock=now-today-tomorrow-later&f[1a]=cv-d1-cw-be4-d2-cx-be1-aqo-1qx-5q5a&f[1b]=73b6-48og-d3-mkl0",
    "https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?stock=now-today-tomorrow-later&brand=asrock-asus-gigabyte-msi&f[1zs]=cln9-1p2j-gfw3-agnc-68te&f[59]=6-2ld-1zy&f[765]=bp-bm-24f-bn-1oy-bo-1p2",
    "https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaya-pamyat-dimm/?stock=now-today-tomorrow-later&f[1b]=d4w-68vs&f[7l4]=cx-aqo-1qx-5q5a-1qw-bvzp-1qz-cw&f[478]=20j-20d-20e&f[j]=kc4",
    "https://www.dns-shop.ru/catalog/17a89c2216404e77/bloki-pitaniya/?stock=now-today-tomorrow-later&fr[89h]=500-1550&f[5w]=240-4y-241-4v-117p-242&f[5a6]=i0bi-cfsb-bait-7la-f7ta-k9tt-k9tr-k9tq-k9u4-k9u3-k9tw-k9u1-k9tu-k9tz&f[5g]=20v",
    "https://www.dns-shop.ru/catalog/dd58148920724e77/ssd-m2-nakopiteli/?stock=now-today-tomorrow-later&fr[1h7]=239-8000"]

re_shablon = [r"(.+)\s\[(.+)\]", r"(.+)\s\[.+\]\s\[(.+)\]", r"(.+)\s\[(.+)\]",
              r"(.+)\s\[.+\]\s.+\s\[(.+)\]", r"(.+)\s\[.+\]\s.+\s\[(.+)\]", r"(.+)\s\[.+\]\s\[(.+)\]"]

# Функция самого парсера
def parser(url, re_shablon):
    # Передаем нужную url в драйвер
    driver.get(url)
    # Задержка чтобы первая страница успела прогрузится
    time.sleep(10)

    page_number = 1
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        print(f"Страница: {page_number}")
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product")))
        # Проходимся по карточкам товаров
        for product in products:
            try:
                # Находим название и цену товара внутри текущей карточки
                name_element = WebDriverWait(product, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "catalog-product__name-wrapper")))
                price_element = WebDriverWait(product, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "product-buy__price")))
            # Ловим ошибку, если вдруг не находим карточку, название или цену
            except NoSuchElementException:
                continue
            # Передаем в переменную text название товара и извлекаем нужное с помощью шаблона
            text = name_element.text
            match = re.fullmatch(re_shablon, text)
            # Проверяем есть ли вторая цена у товара (В днс бывает две цены, одна со скидкой, другая без)
            if "\n" in price_element.text:
                price = price_element.text.split("\n")[0]
            else:
                price = price_element.text
            # Проверям получили ли название карточки, и соответствует ли оно шаблону
            if match is None:
                continue

            # Выводим название и цену товара
            print(f"Название: {match.group(1)} Характеристики:{match.group(2)} Цена: {price}")

        try:
            # Ищем кнопку "Следующая страница"
            next_button = driver.find_element(By.CSS_SELECTOR,
                                              "a.pagination-widget__page-link.pagination-widget__page-link_next")
            # Кликаем на кнопку "Следующая страница"
            next_button.click()

            page_number += 1
        # Ловим ошибочку, если не нашли кнопку "Следующая страница", и заканчиваем с этой категорией товара
        except NoSuchElementException:
            print("Больше нет страниц")
            break
# Функция для выбора категорий (бета)
def choise_category():
    while True:
        try:
            # Просим пользователя ввести кол-во нужных ему категорий
            quantity_category = int(input("Введите кол-во категорий от 1 до 6: "))
        # Ловим ошибочку, если пользователь забыл что такое цифры
        except ValueError:
            print("Ошибка, введите целое число от 1 до 6")
            continue

        user_category = []
        # Если пользователю нужны все 6 категорий, то заполняем ими список
        if quantity_category == 6:
            user_category = [x for x in range(6)]
            return user_category
            break
        # Возвращаем пользователя к вводу кол-ва категорий, если ввел недопустимое их кол-во
        elif quantity_category < 1 or quantity_category > 6:
            print("Категорий всего 6, введите число от 1 до 6")
            continue

        else:
            while True:

                try:
                    # Просим вводить пользователя по одной категории
                    category = int(input("Введите одну из нужных категорий: "))
                # Ловим ошибочку, если пользователь забыл что такое цифры
                except ValueError:
                    print("Ошибка, введите целое число от 1 до 6")
                    continue
                # Возвращаем пользователя к вводу категории, если ввел недопустимую категорию
                if (category > 6) or (category < 1):
                    print("Такой категории не существует")
                # Добавляем в список нужные пользователю категории
                else:
                    user_category.append(category-1)
                    quantity_category = quantity_category - 1

                if quantity_category < 1:
                    break

        return user_category
        break
# Функция старта парсера (бета)
def start_parser():
    # Делаем driver глобальной переменной чтобы его было видно
    global driver
    # Создаем список категорий с помощью функции choise_category
    category = choise_category()

    print("Запуск парсера...")
    time.sleep(1)
    # Запускаем сам драйвер
    driver = UC.Chrome()
    # Проходимся по нужным пользователю категориям
    for i in range(len(category)):
        parser(urls[category[i]], re_shablon[category[i]])

    try:
        driver.close()
    except Exception:
        print("Парсинг завершен")
    finally:
        print("Парсинг завершен")

start_parser()
