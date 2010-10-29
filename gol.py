#!/usr/bin/python
import sys
import time, os, commands
import pylab, numpy, Image, ImageDraw, ImageChops, ImageEnhance
from os import path

import config
from engine import Board
from distance import distance_transform

if __name__ == "__main__" :
    try:
        # load board from file
        board = Board(filename=config.life)
        # generate image to add to the images
        img2 = Image.new('RGB', config.resolution)
        draw = ImageDraw.Draw(img2)
        draw.rectangle(((0,0), img2.size), fill=config.fill, outline=config.fill)

        while True:
            board.execute(config.sample_rate)
            a = distance_transform(board.get_array())

            img = Image.fromarray(a).convert('RGB')
            if config.enhance:
                enh = ImageEnhance.Contrast(img)
                img = enh.enhance(config.enhance)
            img = ImageChops.add (img, img2)
            img = img.resize(config.resolution, Image.ANTIALIAS)

            if not config.save_all:
                filepath = os.path.join(config.directory, "wallpaper.jpg")
            else:
                filepath = os.path.join(config.directory, "%d.jpg"%board.step)

            img.save(filepath)
            commands.getstatusoutput("gconftool-2 -t str --set /desktop/gnome/background/picture_filename %s"%filepath)
            time.sleep(config.interval)

    except Exception as e:
        print e

