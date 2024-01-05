#!/usr/bin/env python3

from sys import path
path.append("../../")

from PIL import Image

from glitch import pixel_sort
from glitch import hsv

if __name__ == "__main__":
    img: Image.Image = Image.open("original.png").convert("RGB").rotate(90, expand=True)
    pixel_sort(img, limiter=lambda p: hsv(p)[1] < .9, sortkey=lambda p: hsv(p)[0], wrap=True)
    img.rotate(-90, expand=True).save("result.png")
