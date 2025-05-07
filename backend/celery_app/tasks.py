import time

from backend.celery_app import app
# from backend.parser.parser_dns import parse_processors, parse_videocards, parse_ssd, parse_ram, parse_motherboards, parse_power_units  
from backend.parser.utils.custom_driver import our_driver
from undetected_chromedriver import ChromeOptions
# from backend.database.managers import clear_components  
from backend.parser.testik import parse_processors, parse_videocards, parse_motherboards


@app.task
def parser():

    time.sleep(1)

    # driver = our_driver(options=options_add())
    #
    # parse_processors(driver)
    # parse_videocards(driver)
    #     # parse_motherboards(driver)
    #
    # driver.close()
    # driver.quit()


    return "Парсинг успешно завершен",


def options_add():
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--enable-javascript")
    options.add_argument(
        "--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    return options

# docker run -d -p 6379:6379 redis

# docker compose up --build -d  
# celery -A backend.celery_app beat  
# celery -A backend.celery_app worker --loglevel=info -P gevent