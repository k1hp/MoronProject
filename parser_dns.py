from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.custom_driver import our_driver
from utils.main_parser_utils import get_text_card,next_page,choise_category
import time

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
def parser(url, re_shablon, driver):
    driver.get(url)

    time.sleep(10)
    parse_category(re_shablon, driver)

def parse_category(re_shablon, driver):
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product")))
        # Проходимся по карточкам товаров
        for product in products:

            text_card = get_text_card(product,re_shablon)

            if text_card == False:
                continue
            else:
                match, price = text_card
            # Выводим название и цену товара
            print(f"Название: {match.group(1)} Характеристики:{match.group(2)} Цена: {price}")

        if next_page(driver) == False:
            break

# Функция старта парсера (бета)
def start_parser():

    category = choise_category()

    print("Запуск парсера...")
    time.sleep(2)

    driver = our_driver()

    try:
        for i in range(len(category)):
            parser(urls[category[i]], re_shablon[category[i]], driver)

    except Exception as e:
        print(f"Парсинг завершился с ошибкой: {e}")
    finally:
        print("Парсинг завершен")

start_parser()
