#!/usr/bin/env python3

from sys import path
path.append("../../")

from PIL import Image

from glitch import pixel_smear
from glitch import hsv

if __name__ == "__main__":
    img: Image.Image = Image.open("original.png").convert("RGB")
    pixel_smear(img, limiter=lambda p: hsv(p)[0] < .85 and hsv(p)[1] < .5, wrap=True)
    img.save("result.png")
