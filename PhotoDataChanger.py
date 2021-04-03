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

        try:
            self.log.start_edit(self.filename)  # logging about edit start

            image_data = self._image_data()
            self.log.loaded(self.filename)
            time_editor = TimeEditor(image_data.datetime, self.edit_minutes[0], self.edit_minutes[1])
            self.new_time = time_editor.get_exit_str()
            image_data.datetime = self.new_time
            image_data.datetime_original = self.new_time
            image_data.datetime_degitized = self.new_time
            lat = eval(self.new_coordinates[0].replace('°', ', ').replace("'", ', '))
            long = eval(self.new_coordinates[1].replace('°', ', ').replace("'", ', '))
            image_data.gps_latitude = lat
            image_data.gps_longitude = long

            with open(self.filename, 'wb') as file:
                file.write(image_data.get_file())

            return self.filename
        except:
            return False
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
                    exit_str += str(i) + ':' + str(image_data.i) + '.i' + '\n'
                except Exception as ex:  # idk what to do then
                    exit_str += str(i) + ':' + str(ex) + '\n'
        #  write all the data to txt file to watch it then
        print(exit_str)

    def _return_error(self, answer):
        print(f'Here is error {answer}')  # TODO replace with error image with explonation

