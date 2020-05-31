#!/usr/bin/python3
# MIT License

# Copyright (c) 2020 Pavel Slama

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import getenv
from requests import get
from ftplib import FTP
import datetime
import time
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

cameraComponent = getenv('CAMERA_COMPONENT')
headingSensor = getenv('HEADING_SENSOR')
hassUrl = getenv('HASS_URL')
token = getenv('TOKEN')
sendInterval = getenv('SEND_INTERVAL')

ftpHost = getenv('FTP_HOST')
ftpUser = getenv('FTP_USER')
ftpPassword = getenv('FTP_PASSWORD')
remotePath = getenv('FTP_REMOTE_PATH')
remoteFile = getenv('FTP_REMOTE_FILE')

degrees = 0.0
imageFile = "image.jpg"
font = ImageFont.truetype("./assets/DejaVuSans.ttf", 25)
headers = {
    "Authorization": "Bearer "+token,
    "content-type": "application/json",
}

if cameraComponent is None or \
        headingSensor is None or \
        hassUrl is None or \
        token is None or \
        ftpHost is None or \
        remotePath is None or \
        remoteFile is None:
    raise ValueError("All setting is required")


def get_data(url):
    try:
        response = get(hassUrl+url, headers=headers)
        return response.json()
    except:
        print("can't get host")
        return None


def do():
    """ Get picture """
    data = get_data("/api/states/"+cameraComponent)

    if data is None:
        return

    if 'attributes' in data and 'entity_picture' in data['attributes']:
        picture_url = get(hassUrl+data['attributes']
                          ['entity_picture'], headers=headers)
        open(imageFile, 'wb').write(picture_url.content)
    else:
        print("no picture")
        return

    """ Get heading """
    data = get_data("/api/states/"+headingSensor)

    if data is None:
        return

    if 'state' not in data:
        print("no heading")
        return

    degrees = float(data['state'])

    img = Image.open(imageFile)
    draw = ImageDraw.Draw(img)
    draw.text((430, 450), datetime.datetime.now().strftime(
        "%d.%m.%Y %H:%M"), (255, 255, 255), font=font)

    compass = Image.open("./assets/compass.png")
    img.paste(compass, (555, 10), compass)

    needle = Image.open("./assets/needle.png")
    needle = needle.rotate(angle=degrees, resample=PIL.Image.BICUBIC).transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(needle, (556, 10), needle)

    img = img.convert('RGB')
    img.save(imageFile, "jpeg", quality=100)

    del draw, img, compass, needle

    try:
        session = FTP(ftpHost, ftpUser, ftpPassword)
        session.cwd(remotePath)
        file = open(imageFile, 'rb')
        session.storbinary('STOR ' + remoteFile, file)
        file.close()
        session.quit()
    except:
        print("FTP error")
        return


try:
    while True:
        do()
        time.sleep(sendInterval)
except KeyboardInterrupt:
    exit()
