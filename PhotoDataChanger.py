from exif import Image
from log_all import Loger

class ImageEditor:

    def __init__(self, filename, query=None):
        
        self.log = Loger()

        self.filenmae = filename
        self.query = query
    
    def _edit_image(self):
        
        if not selfr.query:
            self.log.no_arg(self.filename)
            self._return_error_image
    
    def _return_error_image(self):
        print('Here is error image returning') # TODO replace with error image with explonation