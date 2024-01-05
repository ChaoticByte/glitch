#!/usr/bin/env python3

from sys import path
path.append("../../")

from PIL import Image

from glitch import led_screen

if __name__ == "__main__":
    img: Image.Image = Image.open("original.png").convert("RGB")
    led_screen(img)
    img.save("result.png")
