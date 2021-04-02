from exif import Image
from log_all import Loger
from GpsEditor import GPS
from TimeEditor import TimeEditor


class ImageEditor:

    def __init__(self, filename, query_edit=None):

        self.log = Loger()  # creating logger object (this is my custom logging
        self.log.welcome()  # logging about program start

        self.filename = filename

        self.edit_minutes = query_edit['time']
        self.new_coordinates = query_edit['gps']
        self.new_time = None

    # first and main function
    def edit_image(self):

        self.log.start_edit(self.filename)  # logging about edit start

        image_data = self._image_data()
        self.log.loaded(self.filename)
        time_editor = TimeEditor(image_data.datetime, self.edit_minutes[0], self.edit_minutes[1])
        self.new_time = time_editor.get_exit_str()
        print(image_data.datetime)
        print(self.new_time)
        # try:
        #     image_data = self._image_data()
        #     self.log.loaded(self.filename)
        #     time_editor = TimeEditor(image_data.datetime, self.edit_minutes[0], self.edit_minutes[1])
        #     self.new_time = time_editor.get_exit_str()
        #     print(self.new_time)
        # except Exception as ex:  # if something wrong with loading image
        #     self._return_error(answer=str(ex))

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
                exit_str += str(i) + ':' + str(image_data[i]) + '[i]' +'\n'
            except:
                try:  # it also can be a.1 value
                    exit_str += str(i) + ':' + str(image_data.i) + '\n'
                except:  # idk what to do then
                    exit_str += str(i) + ':' + 'cannot get it' + '\n'
        #  write all the data to txt file to watch it then
        print(exit_str)

    def _return_error(self, answer):
        print(f'Here is error {answer}')  # TODO replace with error image with explonation

