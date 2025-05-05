from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re

def get_text_card(product,re_shablon):
    try:
        # Находим название и цену товара внутри текущей карточки
        name_element = product.find_element(By.CLASS_NAME, "catalog-product__name-wrapper")
        price_element = product.find_element(By.CLASS_NAME, "product-buy__price")
    # Ловим ошибку, если вдруг не находим карточку, название или цену
    except NoSuchElementException:
        return False
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
        return False
    return match,price


def next_page(driver):
    try:
        # Ищем кнопку "Следующая страница"
        next_button = driver.find_element(By.CSS_SELECTOR,"a.pagination-widget__page-link.pagination-widget__page-link_next")
        # Кликаем на кнопку "Следующая страница"
        next_button.click()

    # Ловим ошибочку, если не нашли кнопку "Следующая страница", и заканчиваем с этой категорией товара
    except NoSuchElementException:
        print("Больше нет страниц")
        return False

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
            print("Вы выбрали все категории")
            user_category = [x for x in range(6)]
            return user_category
            break
        # Возвращаем пользователя к вводу кол-ва категорий, если ввел недопустимое их кол-во
        elif quantity_category < 1 or quantity_category > 6:
            print("Категорий всего 6, введите число от 1 до 6")
            continue

        else:
            print("Список категорий с номерами:\n1 - Процессоры\n2 - Видеокарты\n3 - Материнские платы\n"
                  "4 - Оперативная память\n5 - Блоки питания\n6 - ССД_M2")
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