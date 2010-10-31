#!/usr/bin/python
import sys, time, os, commands
import numpy, scipy, Image

import config
from engine import Board
from ip import *

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

def write_xml(wallpapers, dirname):
    """Given a list of wallpaper filepaths, will output them to the correct xml format"""
    
    wallpapers.sort(key=lambda a: int(a.split('.')[0]))
    wallpapers = [os.path.join(dirname, w) for w in wallpapers]
    result = ""
    result += START_TIME
    for i in xrange(len(wallpapers) - 1):
        result += write_static(wallpapers[i])
        result += write_transition(wallpapers[i], wallpapers[i+1])
    result += write_static(wallpapers[len(wallpapers) - 1])
    result += write_transition(wallpapers[-1], wallpapers[0])
    return """<background>%s</background>""" % (result)
            
def generate_lifeforms(dirname):
    # load board from file
    board = Board(filename=config.life, rows=config.rows, cols=config.cols)
    
    # generate image to add to the images
    print "Generating life images. Please be patient, this may take a while.\n"

    while board.step < config.steps:
        print ".",
        board.execute(config.sample_rate) 
        
        img = generate_image(board.get_array(), board.get_size())
        filepath = os.path.join(dirname, "%d.png"%board.step)
        img.save(filepath)


if __name__ == "__main__" :
    try:
        if not os.path.isdir(config.directory):
            os.mkdir(config.directory)
        
        lifename = os.path.split(config.life)[1].split(".")[0]
        dirname = os.path.join(config.directory, lifename)
        
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        
        generate_lifeforms(dirname)
        
        wallpapers = list()
        for filename in os.listdir(dirname):
            if filename[-4:]=='.png':
                wallpapers.append(filename)
            
        print "\nWriting XML."
        xml = write_xml(wallpapers, dirname)
        
        xmlfile = os.path.join(dirname, "%s.xml"%lifename)
        f = file(xmlfile, 'w')
        f.write(xml)
        f.close()
        
        print "Done! You can now set the wallpaper by selecting '%s' as the wallpaper."%xmlfile
            
    except Exception as e:
        print e

