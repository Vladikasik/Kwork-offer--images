from exif import Image

with open('my_test1.jpg', 'rb') as file:
    my_image = Image(file)

for i in my_image.list_all():
    print(i)
