from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions
from backend.parser.utils.custom_driver import our_driver
from backend.parser.utils.main_parser_utils import get_text_card, next_page
from backend.parser.manager import JsonManager
from backend.database.managers import add_components
from backend.database.creation import COMPONENTS
import time, re
from typing import List


def parse_processors(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/?stock=now-today-tomorrow-later&f[1zs]=cln9-1p2j-gfw3-agnc-68te&f[13]=bn-bo-bq-1ox-1oz-1qs-br-234&f[5e8]=cr&f[1b]=d4w-68vs&f[4r]=1y3-1y5-1y8-1y7-1y9-37k7-1ya-azk-37kr-37kq-1yb-e3o-1cze-1md4-2am-ahu9-ahmj-2al-cann-1so-1sp&f[42s]=cr&f[1e6]=98"
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

                result.append(
                    dict(
                        name=name_product,
                        socket=specs_product[0].strip(),
                        core=specs_product[1][1:3].strip(),
                        frequency=specs_product[1][5:].strip(),
                        l2_cache=specs_product[-4][6:].strip(),
                        l3_cache=specs_product[-3][6:].strip(),
                        ddr4="DDR4",
                        ddr5=None,
                        RAM_frequency=specs_product[-2][10:].strip(),
                        TDP=specs_product[-1][5:].strip(),
                        price=price,
                    )
                )

            elif len(specs_product) == 6:
                result.append(
                    dict(
                        name=name_product,
                        socket=specs_product[0].strip(),
                        core=specs_product[1][1:3].strip(),
                        frequency=specs_product[1][5:].strip(),
                        l2_cache=specs_product[-4][6:].strip(),
                        l3_cache=specs_product[-3][6:].strip(),
                        ddr4="DDR4",
                        ddr5="DDR5",
                        RAM_frequency=specs_product[-2][-1:-9:-1][::-1].strip(),
                        TDP=specs_product[-1][5:].strip(),
                        price=price,
                    )
                )

            else:
                result.append(
                    dict(
                        name=name_product,
                        socket=specs_product[0].strip(),
                        core=specs_product[1][1:3].strip(),
                        frequency=specs_product[1][5:].strip(),
                        l2_cache=specs_product[-5][6:].strip(),
                        l3_cache=specs_product[-4][6:].strip(),
                        ddr4="DDR4",
                        ddr5="DDR5",
                        RAM_frequency=specs_product[-2][-1:-9:-1][::-1].strip(),
                        TDP=specs_product[-1][5:].strip(),
                        price=price,
                    )
                )

        if next_page(driver) == False:
            break

    JsonManager().file_write_components("processors", result)
    add_components(data=result, table=COMPONENTS["processors"])

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
            gpu_prev = re.search(r"GPU\s*(\d+)\s*МГц", specs_product[-1])

            if gpu_prev:
                result.append(
                    dict(
                        name=name_product,
                        PCIe=specs_product[0][5:8].strip(),
                        VRAM=specs_product[0].split(" ")[2].strip() + " ГБ",
                        type_VRAM=specs_product[0][14:].strip(),
                        MIW=specs_product[1][1:].strip(),
                        GPU_frequency=gpu_prev.group(1) + " МГц",
                        price=price,
                    )
                )

            else:
                continue

        if next_page(driver) == False:
            break

    JsonManager().file_write_components("videocards", result)
    add_components(data=result, table=COMPONENTS["videocards"])

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
                    socket=specs_product[0].strip(),
                    chipset=specs_product[1][1:].strip(),
                    RAM=specs_product[2][3:7].strip(),
                    RAM_frequency=specs_product[2][8:].strip(),
                    form_factor=specs_product[-1][1:].strip(),
                    price=price,
                )
            )

        if next_page(driver) == False:
            break

    JsonManager().file_write_components("motherboards", result)
    add_components(data=result, table=COMPONENTS["motherboards"])

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
                        type=specs_product[0].strip(),
                        volume=re.search(r"(\d+)\s*ГБ", specs_product[1]).group(1).strip()
                               + " ГБ",
                        quantity=specs_product[1][6:].strip(),
                        frequency=specs_product[2][1:].strip(),
                        cl=specs_product[3][1:3].strip(),
                        price=price,
                    )
                )

        if next_page(driver) == False:
            break

    JsonManager().file_write_components("ram", result)
    add_components(data=result, table=COMPONENTS["ram"])

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
                price=price,
            )

            if len(specs_product) == 9:
                result_slov["pin_gpu"] = (
                        f"({re.search(r"^(.*?)\spin", specs_product[-2][1:]).group(1)})"
                        + " + "
                        + f"({re.search(r"^(.*?)\spin", specs_product[-1][1:]).group(1)})"
                )
                result_slov["pin_cpu"] = (
                        f"({re.search(r"^(.*?)\spin", specs_product[4][1:]).group(1)})"
                        + " + "
                        + f"({re.search(r"^(.*?)\spin", specs_product[5][1:]).group(1)})"
                )

            if "16 pin" in match.group(2) and len(specs_product) == 8:
                result_slov["pin_gpu"] = (
                        f"({re.search(r"^(.*?)\spin", specs_product[-2][1:]).group(1)})"
                        + " + "
                        + f"({re.search(r"^(.*?)\spin", specs_product[-1][1:]).group(1)})"
                )

            elif "16 pin" not in match.group(2) and len(specs_product) == 8:
                result_slov["pin_cpu"] = (
                        f"({re.search(r"^(.*?)\spin", specs_product[4][1:]).group(1)})"
                        + " + "
                        + f"({re.search(r"^(.*?)\spin", specs_product[5][1:]).group(1)})"
                )

            result.append(result_slov)

        if next_page(driver) == False:
            break

    JsonManager().file_write_components("power_units", result)
    add_components(data=result, table=COMPONENTS["power_units"])

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

            result.append(
                dict(
                    name=name_product,
                    connector="M.2",
                    type=match.group(1).split()[-1].strip(),
                    interface=specs_product[0].strip(),
                    volume=re.search(r"^(.*?)\sM.2", match.group(1)).group(1).strip(),
                    sread=specs_product[1][10:].strip(),
                    swrite=specs_product[2][10:].strip(),
                    tbw=specs_product[-1][7:].strip(),
                    price=price,
                )
            )

        if next_page(driver) == False:
            break

    JsonManager().file_write_components("ssd", result)
    add_components(data=result, table=COMPONENTS["ssd"])

    return result


if __name__ == "__main__":
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--enable-javascript")
    options.add_argument(
        "--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'"
    )
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    driver = our_driver(options=options)
    # parse_processors(driver)
    # parse_ssd(driver)
    # parse_motherboards(driver)
    # parse_power_units(driver)
    # parse_videocards(driver)
    # parse_ram(driver)