from uuid import UUID, getnode as get_mac

DEBUG = False

WHATSAPP_MESSAGE_INPUT_XPATH = (
    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
)


def get_mac_addr():
    mac = get_mac()
    return UUID(int = mac).hex[-12:]


def get_url(phone, message):
    whatsapp_url = "https://web.whatsapp.com/send?phone={}&text={}"

    full_msg = f"""
        *Salam {phone}*!
        {message}
        """
    return whatsapp_url.format(phone, full_msg)


def get_xpath_with_text(text):
    """"""
    return f"//div[text()='{text}']"


# class TextRedirector(object):
#     """
#     Example:
#     class MyApp(Tk):
#         def __init__(self):
#             Tk.__init__(self)
#             ...
#             sys.stdout = TextRedirector(self.text, "stdout")
#             ...
#     """

#     def __init__(self, widget, tag="stdout"):
#         self.widget = widget
#         self.tag = tag

#     def write(self, str):
#         self.widget.configure(state="normal")
#         self.widget.insert("end", str, (self.tag,))
#         # self.widget.configure(state="disabled")

#     def flush(self):  # needed for file like object
#         pass
