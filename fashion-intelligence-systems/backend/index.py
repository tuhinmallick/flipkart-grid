from flask import Flask
from flask import request
import cv2
import numpy as np
from PIL import Image
import base64
import imutils
import io
from collections import deque
import os
from base64 import b64encode
import sys
from colourChange import *

app = Flask(__name__)
@app.route("/")
def home():
    return "Hello World"

def readb64(uri):
    encoded_data = uri
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("temp/imageToSaveCvized.png", img);
    return img

@app.route("/change_colour/", methods=['GET', 'POST'])
def objpredict():
    img = request.json["img"]
    incolour = request.json["incolour"]
    outcolour = request.json["outcolour"]
    print(img);
    return changeColourAPI(img, incolour, outcolour)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
