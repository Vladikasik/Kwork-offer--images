from lat_lon_parser import *
from haversine import haversine, Unit
a = to_dec_deg(55.0, 40.0, 51.64)
b = to_dec_deg(37.0, 8.0, 15.02)
print(a)
print(b)
cos = 0.00001 / 1.2765031207774693
dist = haversine((a, b), (a + cos, b + cos), unit=Unit.METERS)
print(dist)