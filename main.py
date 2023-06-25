# selenium 4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


options = webdriver.FirefoxOptions()
# options.add_argument('--headless')

driver = webdriver.Firefox(service=FirefoxService(
    GeckoDriverManager().install()), options=options)
