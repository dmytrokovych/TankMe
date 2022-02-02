from PIL import Image
import os
from sys import argv


color_swaps = {
#   'swapN': [(old_rgb), (new_rgb)],
    'swap1': [(43, 51, 159, 255), (117, 9, 14, 255)],
    'swap2': [(50, 61, 186, 255), (147, 11, 17, 255)],
    'swap3': [(63, 72, 204, 255), (182, 14, 22, 255)],
    'swap4': [(89, 99, 210, 255), (221, 17, 28, 255)],
    'swap5': [(113, 120, 217, 255), (240, 57, 67, 255)],
    'swap6': [(35, 43, 129, 255), (71, 5, 9, 255)],
    'bactr': [(255, 255, 255, 255), (255, 255, 255, 0)]
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
