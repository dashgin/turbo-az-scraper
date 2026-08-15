import datetime
import os
import platform
import sys
import time
import warnings

import art
from colorama import init, Fore
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    UnexpectedAlertPresentException,
    InvalidArgumentException
)
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored

warnings.filterwarnings('ignore')

# -------------------------------------------------- VARIABLES --------------------------------------------------------
WHATSAPP_MESSAGE_INPUT_XPATH = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
PHONE_NUMBERS_JSON = [
    {
        "phone_number": "+994709051195",
        "message": "Test message",
        "name": "Dashgin",
    },
    {
        "phone_number": "+994602016800",
        "message": "test message",
        "name": "Me"
    }
]


# ---------------------------------------------------- UTILS ----------------------------------------------------------
def get_url(phone_number, message, user_name):
    base_msg = f"""
        *Hi {user_name}*! \n
        \n{message}\n
        Thanks!
        """
    return f'https://web.whatsapp.com/send?phone={phone_number}&text={base_msg}'


def get_xpath_with_text(text):
    return f"//div[text()='{text}']"


def print_(message, _type):
    if _type == 'INFO':
        print(
            f"[{colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan')}] [{colored('INFO', 'green')}] {message})"
        )

    elif _type == 'WARNING':
        print(
            f"[{colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan')}] "
            f"[{colored('WARNING', 'yellow')}] {message})"
        )
    elif _type == 'ERROR':
        print(
            f"[{colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan')}] [{colored('ERROR', 'red')}] {message})"
        )
    elif _type == 'SUCCESS':
        print(
            f"[{colored(datetime.datetime.now().strftime('%H:%M:%S'), 'cyan')}] [{colored('SUCCESS', 'green')}] {message})"
        )


# ---------------------------------------------------------------------------------------------------------------------

options = Options()
options.add_argument("--user-data-dir=chrome-data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

try:
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    driver.implicitly_wait(10)
    waiter = WebDriverWait(driver, 10)
    print_("Chrome driver is ready", 'SUCCESS')

except InvalidArgumentException:
    print_("close other chrome driver(s) and try again from task manager", "WARNING")
    print_("Chrome driver is not ready", "ERROR")
    sys.exit(1)

print_("Chrome driver is ready 2", 'SUCCESS')


def send_whatsapp_message(phone_number, message, user_name):
    wait_counter = 0

    while True:
        try:
            waiter.until(ec.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']")))
            wait_counter += 1
            if wait_counter % 1000 == 0:
                print_("Waiting for user to log in...", 'WARNING')
        except TimeoutException:
            print_("Logged in to WhatsApp", 'INFO')
            break

    # check if number is valid
    _url = get_url(phone_number, message, user_name)
    driver.get(_url)

    while True:
        try:
            time.sleep(6)
            print('trying to get message input')
            msg_box = driver.find_element(By.XPATH, WHATSAPP_MESSAGE_INPUT_XPATH)
            msg_box.send_keys('\n')
            time.sleep(2)
            print_(f"Successfully send message to {str(i['phone_number'])}, name: {str(i['name'])}", 'INFO')
            break
        except NoSuchElementException:
            try:
                driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/progress')
                print_("Loading Whatsapp", 'INFO')
                time.sleep(1)
                continue
            except NoSuchElementException:
                try:
                    driver.find_element(By.XPATH, get_xpath_with_text('Starting Chat'))
                    print_("Starting Chat", 'INFO')
                    time.sleep(1)
                    continue

                except NoSuchElementException:
                    try:
                        driver.find_element(By.XPATH,
                                            get_xpath_with_text("Phone number shared via url is invalid."))
                        print_(f"{i['phone_number']} is not a valid number ", 'ERROR')
                        break
                    except NoSuchElementException:
                        print_(f"check your internet connection", 'ERROR')

        except UnexpectedAlertPresentException:
            print_("Alert is present", 'ERROR')
            break


if __name__ == '__main__':
    # Initialize colorama
    init()
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    # Display ASCII art
    print(art.text2art("Py Auto WhatsApp Sender"))
    print(Fore.CYAN + "\nCreated By:" + Fore.RESET + "Dashgin\n")
    print(Fore.YELLOW + "GitHub: " + Fore.RESET + "@dashgin")
    print(Fore.YELLOW + "Instagram:" + Fore.RESET + " @dasqinxudiyev")
    print(Fore.YELLOW + "Blog Site:" + Fore.RESET + "dashgin.me\n")

    # Send whatsapp message
    for i in PHONE_NUMBERS_JSON:
        send_whatsapp_message(i['phone_number'], i['message'], i['name'])
    # Close chromedriver
    driver.quit()
