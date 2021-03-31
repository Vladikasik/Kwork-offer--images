from datetime import datetime

class TimeEditor:

    def __init__(self, str_time):
        
        self.start_time = datetime.strptime(str_time, '%Y:%m:%d %H:%M:%S')
        print(self.start_time)

if __name__=='__main__':
    editor = TimeEditor('2021:03:23 03:39:50')
    