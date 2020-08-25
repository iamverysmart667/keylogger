from datetime import datetime

class Ticker:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def start(self):
        self.start_time = datetime.now()
        return self.start_time

    def stop(self):
        self.stop_time = datetime.now()
        elapsed_time = self.stop_time - self.start_time 

        result = elapsed_time.microseconds // 1000 + elapsed_time.seconds * 1000

        return result

    def is_started(self):
        return bool(self.start_time)
