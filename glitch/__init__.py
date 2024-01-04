# Copyright (c) 2024 Julian Müller (ChaoticByte)

from colorsys import rgb_to_hsv as _rgb_to_hsv
from typing import Any
from typing import Callable

from PIL import Image
from PIL import ImageChops

def led_screen(img: Image.Image):
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
    data = list(img.getdata())
    width = img.width
    height = img.height
    i = 0
    while i < len(data):
        y = i // width
        row_limit = ((y + 1) * width)
        while i < row_limit:
            p = data[i]
            x = i % width
            for j in range(4):
                x_curr = x + j
                if x_curr < width:
                    for k in range(4):
                        if j > 2 or k > 2:
                            p_curr = (0, 0, 0)
                        else:
                            p_curr = [0, 0, 0]
                            p_curr[j] = p[j]
                            p_curr = tuple(p_curr)
                        y_curr = y + k
                        if y_curr < height:
                            img.putpixel((x_curr, y_curr), p_curr)
                    i += 1
        i += width * 3

def pixel_sort(img: Image.Image, limiter: Callable[[tuple], bool] = lambda p: hsv(p)[2] > 0.5, sortkey: Callable[[tuple], Any] = lambda p: hsv(p)[2], wrap: bool = False):
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
    assert callable(limiter)
    assert callable(sortkey)
    assert type(wrap) == bool
    data = list(img.getdata())
    width = img.width
    i = 0
    while i < len(data):
        y = i // width
        x = i % width
        if limiter(data[i]): # sort valid sub-rows
            start = i
            if wrap:
                i_limit = len(data)
            else:
                i_limit = (y + 1) * width
            while i < i_limit:
                if not limiter(data[i]):
                    break
                i += 1
            sorted_sub = sorted(data[start:i], key=sortkey)
            if wrap:
                for j, p in enumerate(sorted_sub):
                    img.putpixel(
                        ((x + j) % width,
                        y + ((x + j) // width)),
                        p)
            else:
                for j, p in enumerate(sorted_sub):
                    img.putpixel((x + j, y), p)
        else: i += 1

def pixel_smear(img: Image.Image, limiter: Callable[[tuple], bool] = lambda p: hsv(p)[2] > 0.5, wrap: bool = False):
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
    assert callable(limiter)
    assert type(wrap) == bool
    data = list(img.getdata())
    width = img.width
    i = 0
    while i < len(data):
        p = data[i]
        if limiter(p): # repeat valid sub-rows
            if wrap:
                i_limit = len(data)
            else:
                i_limit = ((i // width) + 1) * width
            while i < i_limit:
                if not limiter(data[i]):
                    break
                img.putpixel((i % width, (i // width)), p)
                i += 1
        else: i += 1

def channel_offset(img: Image.Image, offset_red: tuple, offset_green: tuple, offset_blue: tuple):
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
    assert all([type(t) == tuple for t in (offset_red, offset_green, offset_blue)])
    assert all([len(t) == 2 and all([type(v) == int for v in t]) for t in (offset_red, offset_green, offset_blue)])
    width = img.width
    height = img.height
    img_copy = img.copy()
    img.paste((0, 0, 0), (0, 0, width, height)) # /?
    for i, o in enumerate([offset_red, offset_green, offset_blue]):
        chan_shifted = ImageChops.offset(img_copy.getchannel(i), o[0], o[1])
        for j, p in enumerate(chan_shifted.getdata()):
            x = j % width
            y = j // width
            p_dest = list(img.getpixel((x, y)))
            p_dest[i] = p
            img.putpixel((x, y), tuple(p_dest))

# Helpers

def hsv(pixel: tuple) -> float:
    r, g, b = pixel[0], pixel[1], pixel[2]
    return _rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
