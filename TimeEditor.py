from datetime import datetime, timedelta


class TimeEditor:

    def __init__(self, str_time, seconds, plus=True):

        self.start_time = datetime.strptime(str_time, '%Y:%m:%d %H:%M:%S')
        if not plus:
            exit_time = self.start_time - datetime.timedelta(seconds=seconds)
        else:
            exit_time = self.start_time + datetime.timedelta(seconds=seconds)

        exit_str = exit_time.strftime('%Y:%m:%d %H:%M:%S')

        return exit_str
