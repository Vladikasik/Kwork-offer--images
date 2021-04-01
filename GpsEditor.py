import random
from lat_lon_parser import *
from random import randint


class GPS:

    # coordinates be like [(43.03, 32.78, 32.43), (43.03, 32.78, 32.43)]
    def __init__(self, coordinates, edit_to):
        self.lat = coordinates[0]
        self.long = coordinates[1]

        print(self.lat)
        print(self.long)

        self.met = edit_to

    def _edit(self):
        latitude = to_dec_deg(self.lat[0], self.lat[1], self.lat[2])
        longitude = to_dec_deg(self.long[0], self.long[1], self.long[2])

        x_1 = randint(-self.met, self.met)
        pre_x_2 = int((self.met ** 2 - x_1 ** 2) ** 0.5)
        x_2 = randint(-pre_x_2, pre_x_2)

        latitude_new_deg = latitude + x_1 * 0.000008984
        longitude_new_deg = longitude + x_2 * 0.000008998

        latitude_exit = to_str_deg_min_sec(latitude_new_deg)
        longitude_exit = to_str_deg_min_sec(longitude_new_deg)

        lat_str = self._to_str(latitude_exit)
        long_str = self._to_str(longitude_exit)

        exit_list = [lat_str, long_str]
        return exit_list

    def _to_str(self, string):
        string = string.split()
        degr = '(' + string[0].replace('°', '') + '.0 '
        minu = string[1].replace("'", '') + '.0 '
        secu = string[2].replace('"', '') + ')'
        return degr + minu + secu


if __name__ == '__main__':
    gps = GPS([(55.0, 40.0, 51.64), (37.0, 8.0, 15.02)], 0)
    print(gps._edit())
