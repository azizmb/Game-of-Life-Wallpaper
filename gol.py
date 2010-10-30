#!/usr/bin/python
import sys
import time, os, commands
import pylab, numpy, Image, ImageDraw, ImageChops, ImageEnhance
from os import path

import config
from engine import Board
from distance import distance_transform

START_TIME = """<starttime>
    <year>2009</year>
    <month>08</month>
    <day>04</day>
    <hour>00</hour>
    <minute>00</minute>
    <second>00</second>
  </starttime>
  <!-- This animation will start at midnight. -->""" 

def write_static(path, duration=config.sleep_interval):
    return """
	<static>
		<duration>%s</duration>
		<file>%s</file>
	</static>""" % (duration, path)

def write_transition(from_path, to_path, duration=config.transition_interval):
    return """
	<transition>
		<duration>%s</duration>
		<from>%s</from>
		<to>%s</to>
	</transition>""" % (duration, from_path, to_path)

def write_xml(wallpapers):
    """Given a list of wallpaper filepaths, will output them to the correct xml format"""
    
    wallpapers.sort(key=lambda a: int(a.split('/')[-1].split('.')[0]))
    
    result = ""
    result += START_TIME
    for i in xrange(len(wallpapers) - 1):
        result += write_static(wallpapers[i])
        result += write_transition(wallpapers[i], wallpapers[i+1])
    result += write_static(wallpapers[len(wallpapers) - 1])
    result += write_transition(wallpapers[-1], wallpapers[0])
    return """<background>%s</background>""" % (result)


def generate_lifeforms():
    # load board from file
    board = Board(filename=config.life, rows=config.rows, cols=config.cols)
    
    # generate image to add to the images
    img2 = Image.new('RGB', config.resolution)
    draw = ImageDraw.Draw(img2)
    draw.rectangle(((0,0), img2.size), fill=config.fill, outline=config.fill)

    print "Generating life images. Please be patient, this may take a while.\n"

    while board.step < config.steps:
        print ".",
        board.execute(config.sample_rate)
        a = distance_transform(board.get_array())

        img = Image.fromarray(a).convert('RGB')
        if config.enhance:
            enh = ImageEnhance.Contrast(img)
            img = enh.enhance(config.enhance)
        img = ImageChops.add (img, img2)
        img = img.resize(config.resolution, Image.ANTIALIAS)

        filepath = os.path.join(config.directory, "%d.png"%board.step)
        img.save(filepath)


if __name__ == "__main__" :
    try:
        generate_lifeforms()
        
        wallpapers = list()
        for filename in os.listdir(config.directory):
            if filename[-4:]=='.png':
                wallpapers.append(os.path.join(config.directory, filename))
            
        print "\nWriting XML."
        xml = write_xml(wallpapers)
        
        f = file(os.path.join(config.directory, "game-of-life.xml"), 'w')
        f.write(xml)
        f.close()
        
        print "Done! You can now set the wallpaper by selecting '%s/game-of-life.xml' as the wallpaper."%config.directory
            
    except Exception as e:
        print e

