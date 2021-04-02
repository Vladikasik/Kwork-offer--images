import random
from lat_lon_parser import *
from random import randint


class GPS:

    # coordinates be like [(43.03, 32.78, 32.43), (43.03, 32.78, 32.43)]
    def __init__(self, coordinates, edit_to):
        coordinates = coordinates.split('_')
        self.lat = float(coordinates[0])
        self.long = float(coordinates[1])

        print(self.lat)
        print(self.long)

        self.met = int(edit_to)

    def _edit(self):
        latitude = to_dec_deg(self.lat)
        longitude = to_dec_deg(self.long)

        x_1 = randint(-self.met, self.met)
        pre_x_2 = int((self.met ** 2 - x_1 ** 2) ** 0.5)
        x_2 = randint(-pre_x_2, pre_x_2)

        latitude_new_deg = latitude + x_1 * 0.000008984
        longitude_new_deg = longitude + x_2 * 0.000008998

        latitude_exit = to_str_dec_deg(latitude_new_deg)
        longitude_exit = to_str_dec_deg(longitude_new_deg)

        exit_list = [latitude_exit[:-1], longitude_exit[:-1]]
        return exit_list

