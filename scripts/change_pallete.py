from PIL import Image
import os
from sys import argv


color_swaps = {
    #   'swapN': [(old_rgb), (new_rgb)],
    'swap1': [(173, 188, 58, 255), (126, 189, 57, 255)],
    'swap2': [(168, 161, 41, 255), (98, 168, 40, 255)],
    'swap3': [(113, 221, 238, 255), (94, 218, 236, 255)]
}

path = argv[1]


def change_pallete(picture):
    width, height = picture.size
    for swap in color_swaps.values():
        new_color = swap[1]
        for x in range(width):
            for y in range(height):
                current_color = picture.getpixel((x, y))
                if current_color == swap[0]:
                    picture.putpixel((x, y), new_color)


for file_name in os.listdir(path):
    picture = Image.open(path + "\\" + file_name)
    change_pallete(picture)
    picture.save(path + "\\" + file_name, "PNG")
    print("Successful")
