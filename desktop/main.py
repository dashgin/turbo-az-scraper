#!/usr/bin/env python
from logging import PlaceHolder
import requests
import sys
import time
import threading
from tkinter import *
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    UnexpectedAlertPresentException,
    InvalidArgumentException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from utils import (
    WHATSAPP_MESSAGE_INPUT_XPATH,
    get_mac_addr,
    get_url,
    get_xpath_with_text,
)


class Task(threading.Thread):
    def __init__(self, master, task):
        threading.Thread.__init__(self, target=task, args=(master,))

        if not hasattr(master, "thread_enviar") or not master.thread_enviar.is_alive():
            master.thread_enviar = self
            self.start()


class TextWithPlaceholder(Text):
    """
    tkinter's text widget with placeholder
    """

    def __init__(self, parent, placeholder, *args, **kwargs):
        self.placeholder = placeholder
        super().__init__(parent, *args, **kwargs)
        self.insert_placeholder()
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def insert_placeholder(self):
        """insert the placeholder into text box"""
        lbl = Label(
            self,
            text=self.placeholder,
            compound="left",
            fg="darkgray",
            bg=self.cget("bg"),
            font=(None, 10, "bold"),
        )
        self.window_create("end", window=lbl)
        self._placeholder = self.window_names()[0]

    def on_focus_in(self, event):
        try:
            # check whether the placeholder exists
            item = self.window_cget(1.0, "window")
            if item == self._placeholder:
                # remove the placeholder
                self.delete(1.0, "end")
        except:
            # placeholder not found, do nothing
            pass

    def on_focus_out(self, event):
        if self.get(1.0, "end-1c") == "":
            # nothing input, so add back the placeholder
            self.insert_placeholder()


class WhatsappSenderApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Whatsapp Sender App")
        self.geometry("600x400")
        self.main_container = Frame(self)
        self.main_container.pack(fill="both", expand=True)
        self.message_input = TextWithPlaceholder(
            self.main_container,
            height=5,
            padx=10,
            pady=10,
            placeholder="Mesajınızı buraya yazın",
        )
        self.message_input.pack(fill="both", expand=True)

        self.send_button = Button(
            self.main_container,
            text="Send",
            command=lambda: Task(self, self.send_messages),
            fg="white",
            bg="green",
            font="Helvetica 12 bold italic",
            height=1,
            state="normal",
        )

        self.send_button.pack(side=LEFT, fill=X, expand=True)

        self.clear_output_button = Button(
            self.main_container,
            text="Clear output",
            command=self.clear_output,
            fg="white",
            bg="gray",
            font="Helvetica 12 bold italic",
            height=1,
            state="normal",
        )
        self.clear_output_button.pack(side=RIGHT)

        # self.cancel_button = Button(
        #     self.main_container,
        #     text="Cancel",
        #     command=self.cancel,
        #     fg="white",
        #     bg="red",
        #     font="Helvetica 12 bold italic",
        #     height=1,
        #     state="normal",
        # )
        # self.cancel_button.pack(side="top", fill="both", expand=True)
        self.output_area = Text(
            self, wrap="word", padx=10, pady=10, bg="black", fg="yellow"
        )
        self.output_area.pack(side="top", fill="both", expand=True)
        self.output_area.tag_configure("stderr", foreground="#b22222")

    def cancel(self):
        self.send_button.configure(state="normal")
        try:
            self.driver.quit()
        except Exception:
            pass
        self.destroy()

    def clear_output(self):
        try:
            self.output_area.configure(state="normal")
            self.output_area.delete("1.0", "end")
            self.output_area.configure(state="disabled")
        except Exception:
            pass

    @staticmethod
    def show_lisence_error():
        messagebox.showerror(
            "Lisenziya Xetasi",
            "Lisenziyaniz yoxdur!\nEger varsa programi baglayib yeniden acin ve ya internet elaqenizi yoxlayin",
        )

    def _print(self, message, widget):
        """
        write given text to textarea
        """
        widget.configure(state="normal")
        widget.insert("end", message + "\n")
        widget.configure(state="disabled")

    def get_chrome_driver(self):
        options = Options()
        options.add_argument("--user-data-dir=chrome-data")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            driver.implicitly_wait(5)
            self._print("Chrome driver is ready", self.output_area)
            return driver

        except InvalidArgumentException:
            self._print(
                "close other chrome driver(s) from task manager and try again",
                self.output_area,
            )
            self._print("Chrome driver is not ready", self.output_area)
            sys.exit(1)

    def get_message_input(self):
        return self.message_input.get("1.0", "end-1c") or "Bos mesaj"

    def send_whatsapp_message(self, phone, message, driver):

        waiter = WebDriverWait(driver, 5)
        wait_counter = 0

        while True:
            try:
                time.sleep(3)
                # try:
                waiter.until(
                    ec.presence_of_element_located(
                        (By.XPATH, "//canvas[@aria-label='Scan me!']")
                    )
                )
                # except Exception as e:
                #     self._print(
                #         "Waiting for QR code to appear", self.output_area
                #     )
                #     self._print(e, self.output_area)
                #     continue

                wait_counter += 1
                if wait_counter % 1000 == 0:
                    self._print("Waiting for user to log in...", self.output_area)
            except TimeoutException:
                self._print("Logged in to WhatsApp", self.output_area)
                break

        # check if number is valid
        _url = get_url(phone, message)
        driver.get(_url)

        while True:
            try:
                time.sleep(2)
                self._print("Trying to get message input", self.output_area)
                msg_box = driver.find_element(By.XPATH, WHATSAPP_MESSAGE_INPUT_XPATH)
                msg_box.send_keys("\n")
                time.sleep(0.5)
                self._print(
                    f"Successfully send message to {phone} with message: {message}",
                    self.output_area,
                )
                break
            except NoSuchElementException:
                try:
                    driver.find_element(
                        By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/progress'
                    )
                    self._print("Loading Whatsapp", self.output_area)
                    time.sleep(1)
                    continue
                except NoSuchElementException:
                    try:
                        driver.find_element(
                            By.XPATH, get_xpath_with_text("Starting Chat")
                        )
                        self._print("Starting Chat", self.output_area)
                        time.sleep(1)
                        continue

                    except NoSuchElementException:
                        try:
                            driver.find_element(
                                By.XPATH,
                                get_xpath_with_text(
                                    "Phone number shared via url is invalid."
                                ),
                            )
                            self._print(
                                f"{phone} is not a valid number",
                                self.output_area,
                            )
                            break
                        except NoSuchElementException:
                            self._print(
                                "check your internet connection", self.output_area
                            )

            except UnexpectedAlertPresentException:
                self._print("Xeta", self.output_area)
                break

    def send_messages(self, master):
        self.send_button.configure(state="disabled")

        try:
            api_response = requests.post(
                url="http://127.0.0.1:8000/api/cars/all/",
                data={"mac_id": get_mac_addr()},
            ).json()
            if api_response["message"] == "success":
                PHONE_NUMBERS_JSON = api_response["data"]
                self.driver = self.get_chrome_driver()

                try:
                    for i in PHONE_NUMBERS_JSON:
                        self.send_whatsapp_message(
                            phone=i["phone"],
                            message=self.get_message_input(),
                            driver=self.driver,
                        )
                    result = {"message": "success"}

                except Exception as e:
                    result = {"message": "error"}
                    self._print(f"Error: {e}", self.output_area)

                self.driver.quit()
                messagebox.showinfo(result["message"], result["message"])
                self.send_button.configure(state="normal")
                return result

        except requests.exceptions.ConnectionError:
            self.show_lisence_error()
            self.send_button.configure(state="normal")
            return {"message": "error"}


if __name__ == "__main__":
    app = WhatsappSenderApp()
    app.mainloop()
