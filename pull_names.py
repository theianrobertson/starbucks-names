"""
Pull some names out of the super-awesome Alex Graves site demoing how to
generate handwritten text via neural networks.
"""

import base64
import os
import sys
import requests
from bs4 import BeautifulSoup
import config


def pull_website(name):
    """Grab the data"""
    options = config.OPTIONS.copy()
    options['text'] = name
    resp = requests.get(config.BASE_URL, params=options)
    soup = BeautifulSoup(resp.text, 'html.parser')
    img_src = [
        img['src']
        for img in soup.find_all('img')
        if img['src'].startswith('data:image/jpeg;base64,')
        ][0]
    return img_src.split('data:image/jpeg;base64,')[1]


def create_image(base64_string, filename):
    """Creates an image file"""
    img_data = base64.b64decode(base64_string)
    with open(filename, 'wb') as output_file:
        output_file.write(img_data)


def go_grab_a_picture(name):
    """Runs the whole thang"""
    img_data = pull_website(name)
    filename = os.path.join(config.NAMES_DIR, '{}.jpg'.format(name))
    create_image(img_data, filename)


if __name__ == '__main__':
    try:
        NAME_TO_RUN = sys.argv[1]
    except:
        NAME_TO_RUN = 'Xzaiden'
    go_grab_a_picture(NAME_TO_RUN)
