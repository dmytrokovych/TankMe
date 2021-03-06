from PIL import Image
import os
from sys import argv

path = argv[1]


def convertImage(file_name):
    img = Image.open(file_name)
    img = img.convert("RGBA")

    datas = img.getdata()

    newData = []

    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(file_name, "PNG")
    print("Successful")


for file_name in os.listdir(path):
    convertImage(path + "\\" + file_name)
