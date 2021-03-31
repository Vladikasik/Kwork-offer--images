from lat_lon_parser import *
from haversine import haversine, Unit
from random import randint
from math import cos, radians

a = to_dec_deg(55.0, 40.0, 51.64)
b = to_dec_deg(37.0, 8.0, 15.02)
print('first coordinates')
print(a)
print(b)

num = 15 # from settings

x_1 = randint(-num, num)
pre_x_2 = int((num**2 - x_1 ** 2)**0.5)
x_2 = randint(-pre_x_2, pre_x_2)

a_1 = a + x_1*(0.000008984/cos(radians(a)))
b_1 = b + x_2*0.000008998

print()
print(f'x1 = {x_1}')
print(f'x2 = {x_2}')

print()
print('second coordinates')
print(a_1)
print(b_1)

dist = haversine((a, b), (a_1, b_1), unit=Unit.METERS)

print()
print('distance')
print(dist)