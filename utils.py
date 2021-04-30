import time
import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

# Loading variables from .env file
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
URL = os.getenv('URL')

SESSION_INFO_FILE_PATH = 'session_info.txt'


def __attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)

    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver


def __get_status(driver):
    try:
        driver.execute(Command.STATUS)
        return True
    except:
        return False


def get_driver():
    if not os.path.exists(SESSION_INFO_FILE_PATH):
        open(SESSION_INFO_FILE_PATH, 'a').close()

    with open(SESSION_INFO_FILE_PATH, 'rt') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    if not lines:
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        print('URL', driver.command_executor._url)
        print('SESSION ID', driver.session_id)
        with open(SESSION_INFO_FILE_PATH, 'w') as f:
            f.writelines([driver.command_executor._url + '\n', driver.session_id])
    else:
        driver = __attach_to_session(executor_url=lines[0], session_id=lines[1])
        if not __get_status(driver):
            print('cleaning session')
            open(SESSION_INFO_FILE_PATH, 'w').close()
            return get_driver()

    return driver


def login(driver, username, your_password):
    # finds the username box
    try:
        username_element = driver.find_element_by_name("username")
    except:
        print("Already logged in")
        return

    # sends the entered username
    username_element.send_keys(username)

    # finds the password box
    password_element = driver.find_element_by_name("password")

    # sends the entered password
    password_element.send_keys(your_password)

    # finds the login button
    password_element.send_keys(Keys.RETURN)
    time.sleep(4)

    save_login_info_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
    save_login_info_button.click()

    time.sleep(4)
