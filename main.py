# %% [markdown]
# # スタサプ RPA

# %% [markdown]
# ## モジュール読み込み

# %%
# selenium 4
import math
import time
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# import selenium.webdriver.common.devtools.v114 as devtools
from selenium.webdriver.common.by import By
# .env file load
from dotenv import load_dotenv
load_dotenv()

# %% [markdown]
# ## インスタンスの生成
# ### 実行

# %%
options = webdriver.FirefoxOptions()
# options.add_argument('--headless')

driver = webdriver.Firefox(service=FirefoxService(
    GeckoDriverManager().install()), options=options)

driver.set_window_position(0, 0)
original_window = driver.current_window_handle


# %% [markdown]
# ### .env 読み込み

# %%
service_url = os.getenv("LOGIN_URL")
email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("PASSWORD")

# %% [markdown]
# 時刻測定用

# %%
start_time = time.perf_counter()

# %% [markdown]
# ### ログイン

# %%
driver.get(service_url)
username_input_element = driver.find_element(
    by=By.XPATH, value='//*[@id="root"]/div/div/div/form/div/div[2]/input')
password_input_element = driver.find_element(
    by=By.XPATH, value='//*[@id="root"]/div/div/div/form/div/div[3]/span/input')
login_button = driver.find_element(
    by=By.XPATH, value='//*[@id="root"]/div/div/div/form/div/button[2]/span[2]')

username_input_element.clear()
password_input_element.clear()
username_input_element.send_keys(email)
password_input_element.send_keys(password)
email, password = None, None
login_button.click()


# %% [markdown]
# ### URL を設定

# %%
studysapuri_uri_dict = {
    "homework_active": "https://learn.studysapuri.jp/ja/todos/active",
    "homework_expired": "https://learn.studysapuri.jp/ja/todos/expired",
}


# %% [markdown]
# ### 課題状況検査
#
# 課題の残りの数をカウントする

# %% [markdown]
# 残りの課題の数を調べる

# %%
def count_task() -> dict:
    global driver
    driver.get(studysapuri_uri_dict["homework_active"])
    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_elements(
            by=By.CSS_SELECTOR, value="[class*=BasicTemplate__Body]")
    )

    try:
        is_active_homework_empty = WebDriverWait(driver, timeout=4).until(
            lambda d: d.find_elements(
                by=By.CSS_SELECTOR, value="div > ul li > button")
        )
    except TimeoutException as err:
        is_active_homework_empty = []

    # -------------------------------------------------------------------

    driver.get(studysapuri_uri_dict["homework_expired"])
    WebDriverWait(driver, timeout=4).until(
        lambda d: d.find_elements(
            by=By.CSS_SELECTOR, value="[class*=BasicTemplate__Body]")
    )

    try:
        is_expired_homework_empty = WebDriverWait(driver, timeout=4).until(
            lambda d: d.find_elements(
                by=By.CSS_SELECTOR, value="div > ul li > button")
        )
    except TimeoutException as err:
        is_expired_homework_empty = []
    print(
        f"配信中の課題{len(is_active_homework_empty)}",
        f"期限切れ{len(is_expired_homework_empty)}"
    )

    return {
        "active_homework": len(is_active_homework_empty),
        "expired_homework": len(is_expired_homework_empty)
    }


pass


# %% [markdown]
# 最初の課題を開く処理

# %%
def first_taskwork_open():
    global driver
    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(
            by=By.CSS_SELECTOR, value='button[class*="TodoCard"]'
        )
    )
    first_taskwork = driver.find_element(
        by=By.CSS_SELECTOR, value='button[class*="TodoCard"]')
    first_taskwork.click()
    time.sleep(0.1)
    WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(
            by=By.CSS_SELECTOR, value='li[class*=TodoTopic]'
        )
    )
    first_todo = driver.find_element(
        by=By.CSS_SELECTOR, value='li[class*=TodoTopic]')
    first_todo.click()


# %% [markdown]
# 開かれた課題を実行する処理

# %%
call_count = 0


def process_todo():
    global driver
    tab = []

    def sub_tab_all_close() -> None:
        for t in tab:
            driver.switch_to.window(t)
            driver.close()

    def quession_automation() -> None:
        print("Call quession_automation")
        """確認問題をランダムに解く
        """
        global call_count
        call_count += 1

        # 待機
        button = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(
                by=By.CSS_SELECTOR, value="[class*=RaisedButton]")
        )

        print("Call quession_automation wait element,load and body")
        # 完全ロード待ち
        WebDriverWait(driver, timeout=20).until(
            expected_conditions.presence_of_all_elements_located)
        while True:

            # 要素待ち
            WebDriverWait(driver, timeout=20).until(
                lambda d: d.find_element(
                    by=By.CSS_SELECTOR, value="[class*=TopicsPage__Main]  button")
            )

            driver.execute_script("""
            var shuffleArray = (array) => {
                    const cloneArray = [...array];
                    for (let i = cloneArray.length - 1; i >= 0; i--) {
                        let rand = Math.floor(Math.random() * (i + 1));
                        let tmpStorage = cloneArray[i];
                        cloneArray[i] = cloneArray[rand];
                        cloneArray[rand] = tmpStorage;
                    }
                    return cloneArray;
                };
                
            setInterval(()=>{
                shuffleArray(document.querySelectorAll("[class*=TopicsPage__Main]  button"))
                    .forEach(each => each.click());
            })
                            
            setInterval(()=>{
            document.querySelector('button[class*=RaisedButton]').click();
            },Math.random() * ( 10000 - 1000 ) + 1000)
            """)
            if driver.current_url.endswith("result"):
                # 本当に終了したか判定
                checke_target_button = driver.find_elements(
                    by=By.CSS_SELECTOR, value="button[class*=RaisedButton]")
                if checke_target_button == 0:
                    break
                if checke_target_button == 0 and checke_target_button[0].text != "次の問題へ":
                    break
            time.sleep(0.05)

    # -----------------------------------------------------------------------------------------------
    # 各チャプタのタブを開く
    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(
        by=By.CSS_SELECTOR, value='ul[class*="LessonStepList"] > li > a')
    )

    after_second_lesston_list = map(lambda element: element.get_attribute("href"), driver.find_elements(
        by=By.CSS_SELECTOR, value='ul[class*="LessonStepList"] > li > a'))

    try:
        for href in list(after_second_lesston_list):
            driver.switch_to.new_window("tab")
            tab.append(driver.current_window_handle)
            driver.get(href)

            if "questions" in href.split("/"):
                print(href)
                quession_automation()

            # video wait
            WebDriverWait(driver, timeout=4).until(
                lambda d: d.find_element(
                    by=By.TAG_NAME, value="video")
            )
            WebDriverWait(driver, timeout=4).until(
                lambda d: d.find_element(
                    by=By.CSS_SELECTOR, value="[class*=hugereplaybutton]")
            )

            driver.execute_script(
                'document.querySelector("video").volume = 0;'
            )
            driver.execute_script(
                'document.querySelector("video").playbackRate = 16;'
            )
            driver.execute_script(
                'document.querySelector("button[class*=bmpui]").click();'
            )
            driver.execute_script(
                'setInterval(() => { document.querySelector("video").play() }, 2000)'
            )
            driver.execute_script('console.log("RUN");')
            time.sleep(1)

    except TimeoutException as err:
        print("Timeout Err")

    for i in range(1, 30+1):
        print(i, end="\t")
        time.sleep(1)
    print(tab)
    sub_tab_all_close()
    driver.switch_to.window(original_window)
# -------------------------------------------


driver.switch_to.window(original_window)

# %%
todo_homework = count_task()
while True:
    if todo_homework["active_homework"] != 0:  # 配信中の宿題の数が0でないとき
        global driver
        print("Processing= active_homework")
        driver.get(studysapuri_uri_dict["homework_active"])  # ページ移動
        first_taskwork_open()
        process_todo()
    elif todo_homework["expired_homework"] != 0:  # 期限切れのタスクを実行する
        print("Processing= expired_homework")
        driver.get(studysapuri_uri_dict["homework_expired"])  # ページ移動
        first_taskwork_open()
        process_todo()
    else:
        driver.switch_to.window(original_window)
        break
    todo_homework = count_task()

# %% [markdown]
# ```python
#
# count_task()  # タスクの数を調べる
# first_taskwork_open()  # 宿題のページ遷移
# process_todo()  # 宿題を始める
#
# ```

# %%
end_time = time.perf_counter()
print(f"{end_time-start_time} sec")

driver.quit()  # 終了
