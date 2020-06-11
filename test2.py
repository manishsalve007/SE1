#! /usr/bin/env python                                                                                                                                                             
import os
import sys
import re
import tempfile

def getVideoDetails(filepath):
    tmpf = tempfile.NamedTemporaryFile()
    os.system("ffmpeg -i \"%s\" 2> %s" % (filepath, tmpf.name))
    lines = tmpf.readlines()
    tmpf.close()
    metadata = {}
    for l in lines:
        l = l.strip()
        if l.startswith('Duration'):
            metadata['duration'] = re.search('Duration: (.*?),', l).group(0).split(':',1)[1].strip(' ,')
            metadata['bitrate'] = re.search("bitrate: (\d+ kb/s)", l).group(0).split(':')[1].strip()
        if l.startswith('Stream #0:0'):
            metadata['video'] = {}
            metadata['video']['codec'], metadata['video']['profile'] = \
                [e.strip(' ,()') for e in re.search('Video: (.*? \(.*?\)),? ', l).group(0).split(':')[1].split('(')]
            metadata['video']['resolution'] = re.search('([1-9]\d+x\d+)', l).group(1)
            metadata['video']['bitrate'] = re.search('(\d+ kb/s)', l).group(1)
            metadata['video']['fps'] = re.search('(\d+ fps)', l).group(1)
        if l.startswith('Stream #0:1'):
            metadata['audio'] = {}
            metadata['audio']['codec'] = re.search('Audio: (.*?) ', l).group(1)
            metadata['audio']['frequency'] = re.search(', (.*? Hz),', l).group(1)
            metadata['audio']['bitrate'] = re.search(', (\d+ kb/s)', l).group(1)
    return metadata

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python 1.py <filepath(absolute or relative)>")
        sys.exit("Syntax Error")
    p = ( getVideoDetails(sys.argv[1]) )
    x = (p['video']['resolution'])
    y = (p['bitrate'])
    bit =  y.split(' ', 1 )[0]
    res = x.split("x");
    br = 500
    flag = 1
    if int(bit) < br:
	print("poor bitrate")
	flag = 0
    else:
        print("Bitrate quality check passed.")
    w = 640
    h = 360
    if int(res[0]) < w or int(res[1]) < h :
	print("Poor video resolution.")	
	flag = 0
    else:
  	print("Video resolution quality check passed.")
    z = (p['video']['fps'])
    fps = (z.split("f"));
    frame = 30
    if int(fps[0]) < frame:
	print("poor fps")
	flag = 0
    else:
        print("Video fps quality check passed.")
    d = (p['duration'])
    dur = d.split(":");
    l = 3600
    ol = float(dur[0]) * 3600 + float(dur[1]) * 60 + float(dur[2])
    if(ol <= l):
	print("Video duration check passed.")
    else:
	print("Video duration too long to upload to the server.")
	flag = 0
    if(flag == 1):
	print
	print("Video is ready to upload to the server.")
    else:
	print
	print("Video isn't ready to upload to the server.")
   
    
   
    
