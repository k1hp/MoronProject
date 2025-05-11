from undetected_chromedriver import ChromeOptions
from backend.parser.utils.custom_driver import our_driver
from backend.parser.utils.main_parser_utils import get_characteristics_product, get_product_and_images_urls, product_handler
# from backend.parser.manager import JsonManager
# from backend.database.managers import add_components
# from backend.database.creation import COMPONENTS
from typing import List


def parse_processors(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/?stock=now-today-tomorrow-later&f[1zs]=cln9-1p2j-gfw3-agnc-68te&f[13]=bn-bo-bq-1ox-1oz-1qs-br-234&f[5e8]=cr&f[1b]=d4w-68vs&f[4r]=1y3-1y5-1y8-1y7-1y9-37k7-1ya-azk-37kr-37kq-1yb-e3o-1cze-1md4-2am-ahu9-ahmj-2al-cann-1so-1sp&f[42s]=cr&f[1e6]=98"
    result = list()
    driver.get(url)
    product_urls, product_images = get_product_and_images_urls(driver)

    for product_url in product_urls:
        driver.get(product_url)

        characteristics_product = get_characteristics_product(driver)

        if characteristics_product == False:
            continue

        result.append(product_handler("processors",characteristics_product,product_images[0]))

        del product_images[0]

    return result


def parse_videocards(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=6&stock=now-today-tomorrow-later&brand=asrock-asus-gigabyte-kfa2-msi-palit-sapphire-nvidia&f[1a]=cv-d1-cw-be4-d2-cx-be1-aqo-1qx-5q5a&f[1b]=73b6-48og-d3-mkl0"
    result = list()
    driver.get(url)
    product_urls, product_images = get_product_and_images_urls(driver)

    for product_url in product_urls:
        driver.get(product_url)

        characteristics_product = get_characteristics_product(driver)

        if characteristics_product == False:
            continue

        result.append(product_handler("videocards",characteristics_product,product_images[0]))

        del product_images[0]

    return result


def parse_motherboards(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/?stock=now-today-tomorrow-later&brand=asrock-asus-gigabyte-msi&f[1zs]=cln9-1p2j-gfw3-agnc-68te&f[59]=6-2ld-1zy&f[765]=bp-bm-24f-bn-1oy-bo-1p2&f[4om]=21"
    result = list()
    driver.get(url)
    product_urls, product_images = get_product_and_images_urls(driver)

    for product_url in product_urls:
        driver.get(product_url)

        characteristics_product = get_characteristics_product(driver)

        if characteristics_product == False:
            continue

        result.append(product_handler("motherboards",characteristics_product,product_images[0]))

        del product_images[0]

    return result


def parse_ram(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaya-pamyat-dimm/?stock=now-today-tomorrow-later&rely=1&brand=kingston-kingstonfury-xpgadata-gskill-patriotmemory-corsair&f[1b]=d4w-68vs&f[7l4]=cx-1qx-5q5a-1qw-bvzp-1qz-cw-aqo&f[478]=20j-20d-20e&f[4om]=21&f[j]=kc4&f[606]=5662-565r&f[8je]=cfsi-cfsr"
    result = list()
    driver.get(url)
    product_urls, product_images = get_product_and_images_urls(driver)

    for product_url in product_urls:
        driver.get(product_url)

        characteristics_product = get_characteristics_product(driver)

        if characteristics_product == False:
            continue

        result.append(product_handler("ram", characteristics_product, product_images[0]))

        del product_images[0]

    return result


def parse_power_units(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/17a89c2216404e77/bloki-pitaniya/?stock=now-today-tomorrow-later&rely=1&brand=aerocool-chieftec-cougar-deepcool-gamerstormdeepcool-gigabyte-lianli-montech-msi-thermaltake-xpgadata-zalman&fr[89h]=500-1550&f[5w]=240-4y-241-4v-117p-242&f[6e]=25x-6iq3&f[5a6]=i0bi-cfsb-bait-7la-f7ta-k9tt-k9tr-k9tq-k9u4-k9u3-k9tw-k9u1-k9tu-k9tz&f[5g]=20v&f[2d1]=bc9q"
    result = list()
    driver.get(url)
    product_urls, product_images = get_product_and_images_urls(driver)

    for product_url in product_urls:
        driver.get(product_url)

        characteristics_product = get_characteristics_product(driver)

        if characteristics_product == False:
            continue

        result.append(product_handler("power_units", characteristics_product, product_images[0]))

        del product_images[0]

    return result


def parse_ssd(driver) -> List[dict]:
    url = "https://www.dns-shop.ru/catalog/dd58148920724e77/ssd-m2-nakopiteli/?stock=now-today-tomorrow-later&brand=adata-kingston-samsung-xpgadata-patriotmemory-crucial-corsair-gigabyte-westerndigital&fr[1h7]=239-8000&f[4sw]=21&f[7xp]=21"
    result = list()
    driver.get(url)
    product_urls, product_images = get_product_and_images_urls(driver)

    for product_url in product_urls:
        driver.get(product_url)

        characteristics_product = get_characteristics_product(driver)

        if characteristics_product == False:
            continue

        result.append(product_handler("ssd", characteristics_product, product_images[0]))

        del product_images[0]

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
    driver = our_driver()
    parse_processors(driver)
