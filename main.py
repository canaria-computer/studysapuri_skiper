# %% [markdown]
# # スタサプRPA

# %%

import os
import random as rd
import time

# selenium 4
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import TimeoutException, WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

os.environ["WDM_SSL_VERIFY"] = "0"

# import selenium.webdriver.common.devtools.v114 as devtools

# .env file load

load_dotenv()

# %% [markdown]
# # クラス作成

# %%


class StudysapuriSkip:
    def __init__(self, continue_login=True) -> None:
        self.options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')

        self.driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=self.options
        )

        self.driver.set_window_position(0, 0)
        self.original_window = self.driver.current_window_handle
        self.load_credential()

        self._studysapuri_uri_dict = {
            "homework_active": "https://learn.studysapuri.jp/ja/todos/active",
            "homework_expired": "https://learn.studysapuri.jp/ja/todos/expired",
        }

        self.load_timeout_config()
        if continue_login:
            try:
                self.login()
                self.count_task()
            except TimeoutException as err:
                print(err)
                self.driver.get("data:text,Login failed.")
            else:
                print("Login Successful")

        self.__tab = []

    def load_timeout_config(self) -> None:
        self.timeout = os.getenv("TIMEOUT_SEC")
        if self.timeout == None:
            self.timeout = 20
        else:
            self.timeout = float(self.timeout)

    def load_credential(self) -> None:
        self.service_url = os.getenv("LOGIN_URL")
        self.__email = os.getenv("EMAIL_ADDRESS")
        self.__password = os.getenv("PASSWORD")

        # 環境変数未設定時
        if self.__email == None:
            print("Your ID is None.")
            self.__email = input("Please input ID or email:")

        if self.__password == None:
            print("Your PASSWORD is None.")
            self.__password = input("Please input password:")

    def release_credential(self):
        self.__email = self.__password = None

    def login(self, count=0):
        self.driver.get(self.service_url)
        self.username_input_element = self.driver.find_element(
            by=By.XPATH, value='//*[@id="root"]/div/div/div/form/div/div[2]/input'
        )
        self.password_input_element = self.driver.find_element(
            by=By.XPATH, value='//*[@id="root"]/div/div/div/form/div/div[3]/span/input'
        )
        self.login_button = self.driver.find_element(
            by=By.XPATH, value='//*[@id="root"]/div/div/div/form/div/button[2]/span[2]'
        )
        # ----------------------------------
        self.username_input_element.clear()
        self.password_input_element.clear()
        self.username_input_element.send_keys(self.__email)
        self.password_input_element.send_keys(self.__password)
        time.sleep(1)
        self.login_button.click()
        time.sleep(rd.uniform(1, 5))
        if self.driver.current_url.endswith("login") and count < 3:
            print(self.driver.current_url)
            print("Retry...", count)
            self.login(count + 1)

    def count_task(self):
        self.driver.get(self._studysapuri_uri_dict["homework_active"])
        WebDriverWait(self.driver, timeout=self.timeout).until(
            lambda d: d.find_elements(
                by=By.CSS_SELECTOR, value="[class*=BasicTemplate__Body]"
            )
        )
        try:
            self.is_active_homework_empty = WebDriverWait(self.driver, timeout=4).until(
                lambda d: d.find_elements(
                    by=By.CSS_SELECTOR, value="div > ul li > button"
                )
            )
        except TimeoutException as err:
            self.is_active_homework_empty = []

        self.driver.get(self._studysapuri_uri_dict["homework_expired"])
        WebDriverWait(self.driver, timeout=self.timeout).until(
            lambda d: d.find_elements(
                by=By.CSS_SELECTOR, value="[class*=BasicTemplate__Body]"
            )
        )
        try:
            self.is_expired_homework_empty = WebDriverWait(
                self.driver, timeout=4
            ).until(
                lambda d: d.find_elements(
                    by=By.CSS_SELECTOR, value="div > ul li > button"
                )
            )
        except TimeoutException as err:
            self.is_expired_homework_empty = []

        print(
            f"配信中の課題{len(self.is_active_homework_empty)}",
            f"期限切れ{len(self.is_expired_homework_empty)}",
        )

        return {
            "active_homework": len(self.is_active_homework_empty),
            "expired_homework": len(self.is_expired_homework_empty),
        }

    def first_taskwork_open(self):
        WebDriverWait(self.driver, timeout=self.timeout * 2).until(
            lambda d: d.find_element(
                By.CSS_SELECTOR, 'button[class*="TodoCard"]')
        )
        self.first_taskwork = self.driver.find_element(
            By.CSS_SELECTOR, value='button[class*="TodoCard"]'
        )
        self.first_taskwork.click()

        WebDriverWait(self.driver, timeout=self.timeout * 5).until(
            expected_conditions.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "span[class*=isIncomplete]")
            )
        )

        self.first_todo = self.driver.find_element(
            By.CSS_SELECTOR, value="span[class*=isIncomplete]"
        )
        f = open("JS/incompleteClick.js", "r")
        try:
            self.driver.execute_script(f.read())
        except:
            print("An error has occurred.")
        finally:
            f.close()
            print("file resource released.")

    def process_todo(self):
        while len(self.is_active_homework_empty) > 0:
            self.driver.get(self._studysapuri_uri_dict["homework_active"])
            self.first_taskwork_open()
            self.lesson_automation()
            self.count_task()
        while len(self.is_expired_homework_empty) > 0:
            self.driver.get(self._studysapuri_uri_dict["homework_expired"])
            self.lesson_automation()
            self.count_task()
        print("\033[31m Task completed.\033[31m")

    def sub_tab_all_close(self) -> None:
        for t in self.__tab:
            self.driver.switch_to.window(t)
            self.driver.close()

    def first_taskwork_open(self):
        WebDriverWait(self.driver, timeout=self.timeout).until(
            lambda d: d.find_element(
                by=By.CSS_SELECTOR, value='button[class*="TodoCard"]'
            )
        )
        first_taskwork = self.driver.find_element(
            by=By.CSS_SELECTOR, value='button[class*="TodoCard"]'
        )
        first_taskwork.click()

        WebDriverWait(self.driver, timeout=100).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "span[class*=isIncomplete],span[class*=isInProgress]")
            )
        )

        f = open("JS/incompleteClick.js", "r")
        self.driver.execute_script(f.read())
        f.close()
        print("first_taskwork_open fin")

    def video_automation(self):
        # video wait
        WebDriverWait(self.driver, timeout=4).until(
            lambda d: d.find_element(by=By.TAG_NAME, value="video")
        )
        WebDriverWait(self.driver, timeout=4).until(
            lambda d: d.find_element(
                by=By.CSS_SELECTOR, value="[class*=hugereplaybutton]"
            )
        )
        f = open("JS/videoAutomation.js", "r", encoding="UTF-8")
        command_list = f.readlines()
        for comand in command_list:
            self.driver.execute_script(comand)
        f.close()
        time.sleep(1)

    def lesson_automation(self):
        # 要素を探す
        WebDriverWait(self.driver, timeout=20).until(
            lambda d: d.find_element(
                by=By.CSS_SELECTOR,
                value='ul[class*="LessonStepList"] > li > a span[class*=isIncomplete]',
            )
        )

        after_second_lesston_list = map(
            lambda element: element.get_attribute("href"),
            self.driver.find_elements(
                by=By.CSS_SELECTOR,
                value='ul[class*="LessonStepList"] > li > a span[class*=isIncomplete]',
            ),
        )

        try:
            for href in list(after_second_lesston_list):
                print(self.__tab, href)
                self.driver.switch_to.new_window("tab")
                self.__tab.append(self.driver.current_window_handle)
                self.driver.get(href)
                if "questions" in href.split("/"):
                    print(href)
                    self.quession_automation()
                self.video_automation()

        except TimeoutException as err:
            print("Timeout Err", err)

    def quession_automation(self):
        """確認問題のみ自動化する"""
        while True:
            # 要素待ち
            WebDriverWait(self.driver, timeout=20).until(
                lambda d: d.find_element(
                    by=By.CSS_SELECTOR, value="[class*=TopicsPage__Main]  button"
                )
            )
            f = open("JS/autoClick.js", "r", encoding="UTF-8")
            js_file_autoClick = f.read()
            self.driver.execute_script(js_file_autoClick)
            f.close()
            if self.driver.current_url.endswith("result"):
                # 本当に終了したか判定
                checke_target_button = self.driver.find_elements(
                    by=By.CSS_SELECTOR, value="button[class*=RaisedButton]"
                )
                if checke_target_button == 0:
                    break
                if (
                    checke_target_button == 0
                    and checke_target_button[0].text != "次の問題へ"
                ):
                    break
            time.sleep(0.05)


# %%
instans = StudysapuriSkip()

# %%
time.sleep(30)
instans.driver.quit()
# instans = StudysapuriSkip()
# instans.process_todo()
