from exif import Image
from log_all import Loger

class ImageEditor:

    def __init__(self, filename, query=None):
        
        self.log = Loger()
        self.log.welcome()

        self.filename = filename
        self.query = query
    
    def _edit_image(self):
        
        self.log.start_edit(self.filename)

        if not self.query:
            self.log.no_arg(self.filename)
            self._return_error(answer='NoQuery')
            return
        
        try:
            image_data = self._image_data()
            self.log.loaded(self.filename)
        except Exception as ex:
            self._return_error(answer=str(ex))

    
    def _image_data(self):
        
        with open(self.filename, 'rb') as image_file:
            image_data = Image(image_file)
        
        return image_data
    
    def _return_error(self, answer):
        print(f'Here is error {answer}') # TODO replace with error image with explonation