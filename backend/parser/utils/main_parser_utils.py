from sys import exception

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time, re
from typing import List


def get_product_and_images_urls(driver):

    product_urls = list()
    product_images = list()

    while True:
        time.sleep(10)

    # Явное ожидание загрузки элементов, чтобы Selenium не пытался их искать до загрузки страницы
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "catalog-product"))
        )
        for product in products:
            image_link_element = product.find_element(By.CLASS_NAME, "catalog-product__image-link")
            source_element = image_link_element.find_element(By.TAG_NAME, "source")
            image_url = source_element.get_attribute("data-srcset")
            product_images.append(image_url)

            # Находим все элементы <a> с указанным классом
        product_links = driver.find_elements(By.CLASS_NAME, "catalog-product__name")

            # Извлекаем атрибут href из каждого элемента
        product_urls.extend([link.get_attribute("href") for link in product_links])



        if next_page(driver) == False:
            break

    return product_urls, product_images



def get_characteristics_product(driver) -> List[dict]:

    try:

        podrobnee_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "product-card-top__specs-more.ui-link.ui-link_blue"))
        )
        podrobnee_link.click()

        expand_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "button-ui.button-ui_grey.button-ui_lg.product-characteristics__expand"))
        )
        expand_button.click()

    except Exception as e:
        return False

    time.sleep(5)

    price_element = driver.find_element(By.CLASS_NAME, "product-buy__price")
    price = price_element.text.split("₽")[0].strip() + "₽"

    elements = driver.find_elements(By.CLASS_NAME, "product-characteristics__spec-value")

    elements_texts = list()

    for element in elements:

            elements_texts.append(element.text.strip())

    elements_texts.append(price)

    return elements_texts



def next_page(driver):
    try:
        # 1. Wait for the next button to be clickable
        next_button = driver.find_element(By.CSS_SELECTOR,"a.pagination-widget__page-link.pagination-widget__page-link_next")

        # 2. Optionally, wait for the preloader to disappear (as before)
        try:
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "catalog-preloader_active"))
            )
        except TimeoutException:
            print("Preloader didn't disappear within 5 seconds, proceeding anyway.")

        # 3. Try to click the button, handling ElementClickInterceptedException
        next_button.click()


    # Ловим ошибочку, если не нашли кнопку "Следующая страница", и заканчиваем с этой категорией товара
    except NoSuchElementException:
        print("Больше нет страниц")
        return False


def product_handler(name, characteristics, image):

    type_product = name
    characteristics_product = characteristics
    image_product = image
    for_reg = " ".join(str(item) for item in characteristics_product if item is not None)

    if type_product == "processors":
        result = dict(
            name=characteristics_product[2],
            socket=characteristics_product[3],
            core=characteristics_product[8],
            l2_cache=characteristics_product[12],
            l3_cache=characteristics_product[13],
            frequency=(re.findall(r'(\d+)\s*ГГц', for_reg)[0]) + " ГГц",
            turbo_freq=(re.findall(r'(\d+)\s*ГГц', for_reg)[1]) + " ГГц",
            type_ram=characteristics_product[21],
            ram_frequency=characteristics_product[24],
            tdp=characteristics_product[26],
            price=characteristics_product[-1],
            image=image_product,
        )

        return result

    if type_product == "videocards":
        result = dict(
            name=characteristics_product[3],
            pcie=(re.findall(r'PCIe\s*\d+(?:\.\d+)?', for_reg))[0],
            gpu_frequency=(re.search(r'(\d+)\s*МГц', for_reg).group(1)) + " МГц",
            vram=(re.search(r'(\d+)\s*ГБ', for_reg).group(1)) + "ГБ",
            type_vram=(re.findall(r'GDDR\d+', for_reg))[0],
            miw=(re.search(r'(\d+)\s*бит', for_reg).group(1)) + " бит",
            price=characteristics_product[-1],
            image=image,
            )

        return result

    if type_product == "motherboards":
        result = dict(
            name=characteristics_product[3],
            form_factor=(re.search(r'(ATX|Mini-ATX|Micro-ATX|Mini-ITX|Mini-STX)', for_reg)).group(1),
            socket=(re.search(r"(LGA\s*\d+|AM\s*\d+)", for_reg, re.IGNORECASE)).group(1),
            chipset=(re.search(r"((AMD|Intel)\s*((PRO\s*\d+)|([A-Z]\d{3})|([A-Z]+\d+[A-Z]*)))", for_reg,re.IGNORECASE)).group(1),
            type_ram=(re.search(r'(DDR\d+)', for_reg, re.IGNORECASE)).group(1),
            max_ram=(re.search(r'(\d+)\s*ГБ', for_reg).group(1)) + " ГБ",
            ram_frequency=(re.search(r'(\d+)\s*МГц', for_reg).group(1)) + " МГц",
            pcie=(re.search(r'(\d+\.\d+)', for_reg)).group(1),
            price=characteristics_product[-1],
            image=image_product,
        )

        return result

    if type_product == "ram":
        result = dict(
            name=characteristics_product[3],
            type_ram=(re.search(r'(DDR\d+)', for_reg, re.IGNORECASE)).group(1),
            volume=(re.search(r'(\d+)\s*ГБ', for_reg).group(1)) + " ГБ",
            quantity=(re.search(r'(\d+)\s*шт', for_reg).group(1)) + " шт",
            rang=(re.search(r'(одноранговая|двухранговая)', for_reg)).group(1),
            ram_frequency=(re.search(r'(\d+)\s*МГц', for_reg).group(1)) + " МГц",
            cl=characteristics_product[-10],
            price=characteristics_product[-1],
            image=image_product,
        )

        return result

    if type_product == "power_units":
        result = dict(
            name=characteristics_product[3],
            power=(re.search(r'(\d+)\s*Вт', for_reg).group(1)) + " Вт",
            certificate=(re.search(r'(Bronze|Gold|Platinum)', for_reg)).group(1),
            pin_main=(re.search(r"(20\+4\s*pin|24\s*pin)", for_reg)).group(1),
            pin_cpu=characteristics_product[ characteristics_product.index((re.search(r"(20\+4\s*pin|24\s*pin)", for_reg)).group(1)) + 1],
            pin_gpu=characteristics_product[characteristics_product.index((re.search(r"(20\+4\s*pin|24\s*pin)", for_reg)).group(1)) + 2],
            price=characteristics_product[-1],
            image=image_product,
        )

        return result

    if type_product == "ssd":
        result = dict(
            name=characteristics_product[3],
            connector="M.2",
            type="NVMe",
            interface=characteristics_product[7],
            volume=(re.search(r'(\d+)\s*ГБ', for_reg).group(1)) + " ГБ",
            sread=(re.findall(r'(\d+)\s*Мбайт', for_reg)[0]) + " Мбайт/сек",
            swrite=(re.findall(r'(\d+)\s*Мбайт', for_reg)[1]) + " Мбайт/сек",
            tbw=(re.search(r'(\d+)\s*ТБ', for_reg).group(1)) + " ТБ",
            price=characteristics_product[-1],
            image=image_product,
        )

        return result


def get_text_card(product,re_shablon):
    try:
        # Находим название и цену товара внутри текущей карточки
        name_element = product.find_element(By.CLASS_NAME, "catalog-product__name-wrapper")
        price_element = product.find_element(By.CLASS_NAME, "product-buy__price")
        image_link_element = product.find_element(By.CLASS_NAME, "catalog-product__image-link")
        source_element = image_link_element.find_element(By.TAG_NAME, "source")
        image_url = source_element.get_attribute("data-srcset")
    # Ловим ошибку, если вдруг не находим карточку, название или цену
    except NoSuchElementException:
        return False
    # Передаем в переменную text название товара и извлекаем нужное с помощью шаблона
    text = name_element.text
    match = re.fullmatch(re_shablon, text)
    image = image_url
    # Проверяем есть ли вторая цена у товара (В днс бывает две цены, одна со скидкой, другая без)
    if "\n" in price_element.text:
        price = price_element.text.split("\n")[0]
    else:
        price = price_element.text
    # Проверям получили ли название карточки, и соответствует ли оно шаблону
    if match is None:
        return False

    return match, price, image


# def choise_category():
#     while True:
#         try:
#             # Просим пользователя ввести кол-во нужных ему категорий
#             quantity_category = int(input("Введите кол-во категорий от 1 до 6: "))
#         # Ловим ошибочку, если пользователь забыл что такое цифры
#         except ValueError:
#             print("Ошибка, введите целое число от 1 до 6")
#             continue
#
#         user_category = []
#         # Если пользователю нужны все 6 категорий, то заполняем ими список
#         if quantity_category == 6:
#             print("Вы выбрали все категории")
#             user_category = [x for x in range(6)]
#             return user_category
#             break
#         # Возвращаем пользователя к вводу кол-ва категорий, если ввел недопустимое их кол-во
#         elif quantity_category < 1 or quantity_category > 6:
#             print("Категорий всего 6, введите число от 1 до 6")
#             continue
#
#         else:
#             print("Список категорий с номерами:\n1 - Процессоры\n2 - Видеокарты\n3 - Материнские платы\n"
#                   "4 - Оперативная память\n5 - Блоки питания\n6 - ССД_M2")
#             while True:
#
#                 try:
#                     # Просим вводить пользователя по одной категории
#                     category = int(input("Введите одну из нужных категорий: "))
#                 # Ловим ошибочку, если пользователь забыл что такое цифры
#                 except ValueError:
#                     print("Ошибка, введите целое число от 1 до 6")
#                     continue
#                 # Возвращаем пользователя к вводу категории, если ввел недопустимую категорию
#                 if (category > 6) or (category < 1):
#                     print("Такой категории не существует")
#                 # Добавляем в список нужные пользователю категории
#                 else:
#                     user_category.append(category-1)
#                     quantity_category = quantity_category - 1
#
#                 if quantity_category < 1:
#                     break
#
#         return user_category