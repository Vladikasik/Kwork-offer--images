from datetime import datetime, timedelta


class TimeEditor:

    def __init__(self, str_time, minutes, plus=True):

        self.start_time = datetime.strptime(str_time, '%Y:%m:%d %H:%M:%S')
        if not plus:
            exit_time = self.start_time - datetime.timedelta(minutes=minutes)
        else:
            exit_time = self.start_time + datetime.timedelta(minutes=minutes)

        self.exit_str = exit_time.strftime('%Y:%m:%d %H:%M:%S')

    def get_exit_str(self):

        return self.exit_str
