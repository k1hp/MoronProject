from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions
from backend.app.parser.utils.custom_driver import our_driver
from backend.app.parser.utils.main_parser_utils import get_text_card, next_page
import time, re
from typing import List


def parse_processors(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/?stock=now-today-tomorrow-later&f[1zs]=cln9-1p2j-gfw3-agnc-68te&f[13]=bn-bo-bq-1ox-1oz-1qs-br-234&f[5e8]=cr&f[1b]=d4w-68vs&f[42s]=cr&f[4r]=1y8-1y7-1y9-1ya-azk-37kr-1yb-e3o-1cze-1md4-2am-ahu9-ahmj-2al-cann-1y3-1y5-37k7-37kq-1so-1sp"
    re_shablon = r"Процессор\s(.+)\s\[(.+)\]"
    result = list()
    driver.get(url)
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product"))
        )
        # Проходимся по карточкам товаров
        for product in products:

            text_card = get_text_card(product, re_shablon)

            if text_card == False:
                continue
            else:
                match, price = text_card

            name_product = match.group(1)
            specs_product = match.group(2).split(",")

            if "DDR5" not in match.group(2):
                # result.append(dict(name = name_product, socket = specs_product[0], core = specs_product[1][1:2], frequency = specs_product[1][5:], L2_cache = specs_product[2][6:],
                #                     L3_cache = specs_product[3][6:],RAM = specs_product[4][5:9], RAM_frequency = specs_product[4][10:], TDP = specs_product[5][5:]))
                result.append(
                    dict(
                        name=name_product,
                        socket=specs_product[0],
                        core=specs_product[1][1:2],
                        frequency=specs_product[1][5:],
                        l2_cache=specs_product[2][6:],
                        l3_cache=specs_product[3][6:],
                        ddr4="DDR4",
                        ddr5=None,
                        RAM_frequency=specs_product[4][10:],
                        TDP=specs_product[5][5:],
                        price=price
                    )
                )

            else:
                result.append(
                    dict(
                        name=name_product,
                        socket=specs_product[0],
                        core=specs_product[1][1:2],
                        frequency=specs_product[1][5:],
                        l2_cache=specs_product[-5][6:],
                        l3_cache=specs_product[-4][6:],
                        ddr4="DDR4",
                        ddr5="DDR5",
                        RAM_frequency=specs_product[-2][6:],
                        TDP=specs_product[-1][5:],
                        price=price
                    )
                )

        if next_page(driver) == False:
            break

    return result

def parse_videocards(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=6&stock=now-today-tomorrow-later&f[1a]=cv-d1-cw-be4-d2-cx-be1-aqo-1qx-5q5a&f[1b]=73b6-48og-d3-mkl0"
    re_shablon = r"Видеокарта\s(.+)\s\[.+\]\s\[(.+)\]"
    result = list()
    driver.get(url)
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product"))
        )
        # Проходимся по карточкам товаров
        for product in products:

            text_card = get_text_card(product, re_shablon)

            if text_card == False:
                continue
            else:
                match, price = text_card

            name_product = match.group(1)
            specs_product = match.group(2).split(",")

            result.append(
                dict(
                    name=name_product,
                    PCIe=specs_product[0][5:8],
                    VRAM=specs_product[0][9:13],
                    type_VRAM=specs_product[0][14:],
                    MIW=specs_product[1][1:],
                    GPU_frequency=specs_product[-1][5:],
                    price=price
                )
            )

        if next_page(driver) == False:
            break

    return result

def parse_motherboards(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?stock=now-today-tomorrow-later&brand=asrock-asus-gigabyte-msi&f[1zs]=cln9-1p2j-gfw3-agnc-68te&f[59]=6-2ld-1zy&f[765]=bp-bm-24f-bn-1oy-bo-1p2"
    re_shablon = r"Материнская\sплата\s(.+)\s\[(.+)\]"
    result = list()
    driver.get(url)
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product"))
        )
        # Проходимся по карточкам товаров
        for product in products:

            text_card = get_text_card(product, re_shablon)

            if text_card == False:
                continue
            else:
                match, price = text_card

            name_product = match.group(1)
            specs_product = match.group(2).split(",")

            result.append(
                dict(
                    name=name_product,
                    socket=specs_product[0],
                    chipset=specs_product[1][1:],
                    RAM=specs_product[2][3:7],
                    RAM_frequency=specs_product[2][8:],
                    form_factor=specs_product[-1][1:],
                    price=price
                )
            )

        if next_page(driver) == False:
            break

    return result

def parse_ram(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaya-pamyat-dimm/?stock=now-today-tomorrow-later&brand=apacer-gskill-kingston-kingstonfury-patriotmemory-teamgroup-xpgadata-acer-adata-agi-ardorgaming-basetech-corsair-crucial-netac-samsung&f[7l4]=cw-cx-aqo-1qx-5q5a-1qw-bvzp-1qz&f[1b]=d4w-68vs&f[478]=20j-20d-20e&f[j]=kc4"
    re_shablon = r"Оперативная\sпамять\s(.+)\s\[.+\]\s.+\s\[(.+)\]"
    result = list()
    driver.get(url)
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product"))
        )
        # Проходимся по карточкам товаров
        for product in products:

            text_card = get_text_card(product, re_shablon)

            if text_card == False:
                continue
            else:
                match, price = text_card

            name_product = match.group(1)
            specs_product = match.group(2).split(",")

            if "CL" in match.group(2):
                result.append(
                    dict(
                        name=name_product,
                        type=specs_product[0],
                        volume=re.search(r"(\d+)\s*ГБ", specs_product[1]).group(1)+" ГБ",
                        quantity=specs_product[1][6:],
                        frequency=specs_product[2][1:],
                        cl=specs_product[3][1:3],
                        price=price
                    )
                )

        if next_page(driver) == False:
            break

    return result

def parse_power_units(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89c2216404e77/bloki-pitaniya/?stock=now-today-tomorrow-later&fr[89h]=500-1550&f[5w]=240-4y-241-4v-117p-242&f[5a6]=i0bi-cfsb-bait-7la-f7ta-k9tt-k9tr-k9tq-k9u4-k9u3-k9tw-k9u1-k9tu-k9tz&f[5g]=20v"
    re_shablon = r"Блок\sпитания\s(.+)\s\[.+\]\s.+\s\[(.+)\]"
    result = list()
    driver.get(url)
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product"))
        )
        # Проходимся по карточкам товаров
        for product in products:

            text_card = get_text_card(product, re_shablon)

            if text_card == False:
                continue
            else:
                match, price = text_card

            name_product = match.group(1)
            specs_product = match.group(2).split(",")

            result_slov = dict(
                        name=name_product,
                        power=specs_product[0],
                        certificate=specs_product[1][1:],
                        pin_cpu=re.search(r"^(.*?)\spin", specs_product[4][1:]).group(1),
                        pin_gpu=re.search(r"^(.*?)\spin", specs_product[-1][1:]).group(1),
                        price=price
                    )

            if len(specs_product) == 9:
                result_slov["pin_gpu"] = f"({re.search(r"^(.*?)\spin", specs_product[-2][1:]).group(1)})" + " + " + f"({re.search(r"^(.*?)\spin", specs_product[-1][1:]).group(1)})"
                result_slov["pin_cpu"] = f"({re.search(r"^(.*?)\spin", specs_product[4][1:]).group(1)})" + " + " + f"({re.search(r"^(.*?)\spin", specs_product[5][1:]).group(1)})"

            if "16 pin" in match.group(2) and len(specs_product) == 8:
                result_slov["pin_gpu"] = f"({re.search(r"^(.*?)\spin", specs_product[-2][1:]).group(1)})" + " + " + f"({re.search(r"^(.*?)\spin", specs_product[-1][1:]).group(1)})"

            elif "16 pin" not in match.group(2) and len(specs_product) == 8:
                result_slov["pin_cpu"] = f"({re.search(r"^(.*?)\spin", specs_product[4][1:]).group(1)})" + " + " + f"({re.search(r"^(.*?)\spin", specs_product[5][1:]).group(1)})"

            result.append(result_slov)

        if next_page(driver) == False:
            break

    return result

def parse_ssd(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/dd58148920724e77/ssd-m2-nakopiteli/?stock=now-today-tomorrow-later&brand=adata-apacer-ardorgaming-kingston-msi-samsung-xpgadata-acer-corsair-crucial-gigabyte-kingspec-patriotmemory-westerndigital&fr[1h7]=239-8000"
    re_shablon = r"^(.*?)накопитель\s(.+)\[.+\]\s\[(.+)\]"
    result = list()
    driver.get(url)
    while True:
        # Задержка для прогрузки текущей страницы
        time.sleep(10)
        # Находим карточки товаров
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product"))
        )
        # Проходимся по карточкам товаров
        for product in products:

            text_card = get_text_card(product, re_shablon)

            if text_card == False:
                continue
            else:
                match, price = text_card

            name_product = match.group(2)
            specs_product = match.group(3).split(",")
            print(name_product)
            result.append(
                dict(
                    name=name_product,
                    connector="M.2",
                    type=match.group(1).split()[-1],
                    interface=specs_product[0],
                    volume=re.search(r"^(.*?)\sM.2", match.group(1)).group(1),
                    sread=specs_product[1][10:],
                    swrite=specs_product[2][10:],
                    tbw=specs_product[-1][7:],
                    price=price
                )
            )

        if next_page(driver) == False:
            break

    return result


if __name__ == "__main__":
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--enable-javascript')
    options.add_argument("--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    driver = our_driver(options=options)
    parse_ssd(driver)
