#!/usr/bin/env python3

from sys import path
path.append("../../")

from PIL import Image

from glitch import channel_offset
from glitch import hsv

if __name__ == "__main__":
    img: Image.Image = Image.open("original.png").convert("RGB")
    channel_offset(img, (2, 0), (-2, -2), (0, 2))
    img.save("result.png")
