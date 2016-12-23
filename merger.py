"""Merge a name and a cup"""

import glob
import random
import os
import sys
from PIL import Image, ImageFilter
import config

def crop_image(image):
    """Crop an image to not include whatever is just white

    Parameters
    ----------
    image : PIL image
    """
    max_x = 0
    min_x = image.width - 1
    max_y = 0
    min_y = image.height - 1
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) != (255, 255, 255, 255):
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
    return image.crop((min_x, min_y, max_x, max_y))


def merge_images(cup, name_file, new_file):
    """Merge two images

    Parameters
    ----------
    cup : dict
        Dictionary with info about the cup
    name_file : str
        String with the name file
    new_file : str
        The new file name
    """
    cup_file = os.path.join(config.CUPS_DIR, cup['filename'])
    cup_image = Image.open(cup_file)
    name_image = Image.open(name_file)
    name_image = crop_image(name_image)

    #Resize the name image
    name_size = (
        cup['x_bottom'] - cup['x_top'], cup['y_bottom'] - cup['y_top'])
    name_image = name_image.resize(name_size, Image.ANTIALIAS)

    #Just use all-black
    name_blurred = Image.new('RGB',name_image.size,(0,0,0))

    #Create a mask (invisible if >= 240 in greyscale)
    mask = name_image.convert('L')
    mask = Image.eval(mask, lambda x: abs(x - 255))

    #Paste into the base image and save.
    cup_image.paste(name_blurred, (cup['x_top'], cup['y_top']), mask=mask)
    cup_image.save(new_file, 'JPEG', quality=90)


def main():
    try:
        name_file = os.path.join(config.NAMES_DIR, sys.argv[1] + '.jpg')
    except IndexError:
        name_files = glob.glob(os.path.join(config.NAMES_DIR, '*.jpg'))
        name_file = random.choice(name_files)
    merge_images(
        #random.choice(config.CUPS),
        config.CUPS[9],
        name_file,
        'test_file.jpg')

if __name__ == '__main__':
    main()