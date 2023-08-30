# %% [markdown]
# # スタサプRPA

# %%
# selenium 4
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
        self.options.add_argument('--headless')

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

        self.exams_skip = True
        self.load_exams_skip_config()

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
        """タイムアウト時間設定"""
        self.timeout = os.getenv("TIMEOUT_SEC")
        if self.timeout == None:
            self.timeout = 20
        else:
            self.timeout = float(self.timeout)

    def load_credential(self) -> None:
        """ログイン情報を読み込む"""
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

    def load_exams_skip_config(self):
        """確認問題(1度しかできない)をスキップするかの設定を読み込む"""
        load_config = os.getenv("EXAMS_SKIP")
        if load_config == None:
            return
        self.exams_skip = bool(load_config)

    def release_credential(self):
        """ログイン情報を変数から解放する"""
        self.__email = self.__password = None

    def login(self, count=0):
        """ログインする

        Args:
            count (int, optional): 試行回数. Defaults to 0.

        Note:
            これはログインに失敗したとき再帰的に繰り返します.
            ただし2回のみです.
        """
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

    def count_task(self) -> dict:
        """宿題の数を数える

        Returns:
            dict: { active_homework : int, expired_homework : int }
        """
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

    def process_todo(self):
        """宿題を1件ずつ呼び出し処理する"""
        while len(self.is_active_homework_empty) > 0:
            self.driver.get(self._studysapuri_uri_dict["homework_active"])
            self.first_taskwork_open()
            self.lesson_automation()
            self.count_task()
            self.sub_tab_all_close()
        while len(self.is_expired_homework_empty) > 0:
            self.driver.get(self._studysapuri_uri_dict["homework_expired"])
            self.lesson_automation()
            self.count_task()
            self.sub_tab_all_close()
        print("Task completed.")

    def sub_tab_all_close(self) -> None:
        """すべてのタブを開く"""
        for t in self.__tab:
            self.driver.switch_to.window(t)
            self.driver.close()

    def first_taskwork_open(self):
        """宿題を開く"""
        WebDriverWait(self.driver, self.timeout*5).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "[class*=BasicTemplate__Main]")
            )
        )
        time.sleep(5)
        with open("JS/examAvoid.js", "r", encoding="UTF-8") as f:
            try:
                self.driver.execute_script(f.read())
            except:
                print("Err?")
            time.sleep(0.1)
        print("wait...")
        WebDriverWait(self.driver, self.timeout*5).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "span[class*=isIncomplete],span[class*=isInProgress]")
            )
        )

        f = open("JS/incompleteClick.js", "r", encoding="UTF-8")
        self.driver.execute_script(f.read())
        f.close()
        print("first_taskwork_open fin")

    def video_automation(self):
        """動画を自動化する"""
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
            try:
                self.driver.execute_script(comand)
            except:
                pass
        f.close()
        time.sleep(1)

    def lesson_automation(self):
        if "exams" in self.driver.current_url.split("/") and self.exams_skip:
            return

        """宿題を捌く
        """
        # 要素を探す
        WebDriverWait(self.driver, timeout=20).until(
            lambda d: d.find_element(
                by=By.CSS_SELECTOR,
                value='ul[class*="LessonStepList"] > li > a span[class*=isIncomplete]',
            )
        )

        after_second_lesston_list = []
        for element in self.driver.find_elements(
            By.CSS_SELECTOR, 'ul[class*="LessonStepList"] > li > a'
        ):
            if (
                len(element.find_elements(
                    By.CSS_SELECTOR, "span[class*=isIncomplete]"))
                > 0
            ):
                after_second_lesston_list.append(element.get_attribute("href"))

        map(
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

    def quession_automation(self, isExams=False):
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
            if isExams:
                f = open("JS/examSubmit.js", "r", encoding="UTF-8")
                time.sleep(2)
                self.driver.execute_script(f.read())
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
            if "lessons" in self.driver.current_url:
                self.driver.get(self.driver.current_url.replace(
                    "lessons", "questions"))
            time.sleep(0.05)

    def destroy(self):
        self.release_credential()
        print("Credential discarded.")
        self.driver.quit()
        self = None
        return self


# %%
instans = StudysapuriSkip()
instans.process_todo()
instans.destroy()
