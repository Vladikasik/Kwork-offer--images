from exif import Image
from log_all import Loger
from GpsEditor import GPS


class ImageEditor:

    def __init__(self, filename, query_edit=None):

        self.log = Loger()  # creating logger object (this is my custom logging
        self.log.welcome()  # logging about program start

        self.filename = filename
        self.query = query_edit

        self.edit_time = None
        self.edit_gps = None

    # first and main function
    def _edit_image(self):

        self.log.start_edit(self.filename)  # logging about edit start

        if not self.query:  # if class were created without query what to edit
            self.log.no_arg(self.filename)
            self._return_error(answer='NoQuery')
            return  # exiting func after logging exception

        try:
            image_data = self._image_data()
            self.log.loaded(self.filename)
            
        except Exception as ex:  # if something wrong with loading image
            self._return_error(answer=str(ex))

    # load image + get metadate
    def _image_data(self):

        with open(self.filename, 'rb') as image_file:
            image_data = Image(image_file)  # getting data via library

        return image_data

    # just print value_name:value_value
    def _test_print_values(self, image_data):
        exit_str = ''
        for i in image_data.list_all():
            try:  # it a[1] value
                exit_str += str(i) + ':' + str(image_data[i]) + '\n'
            except:
                try:  # it also can be a.1 value
                    exit_str += str(i) + ':' + str(image_data.i) + '\n'
                except:  # idk what to do then
                    exit_str += str(i) + ':' + 'cannot get it' + '\n'
        #  write all the data to txt file to watch it then
        with open('all_data.txt', 'w') as f:
            f.write(exit_str)

    def _return_error(self, answer):
        print(f'Here is error {answer}')  # TODO replace with error image with explonation

if __name__ == '__main__':
    changer = ImageEditor('my_test1.JPG')
    changer._test_print_values(changer._image_data())
