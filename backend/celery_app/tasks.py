from celery_app import app
from parser.parser_dns import parse_processors
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions
from parser.utils.custom_driver import our_driver


@app.task
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
def parse_processors():
    return 'hello world'




# docker run -d -p 6379:6379 redis
# celery -A celery_app beat
# celery -A myproject worker --loglevel=info -P gevent