from datetime import datetime

class TimeEditor:

    def __init__(self, str_time):
        
        self.start_time = datetime.strptime(str_time, '%b %d %Y %I:%M%p')