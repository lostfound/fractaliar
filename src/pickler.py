#!/usr/bin/python3
from xml.dom.minidom import Document, parse
from os import listdir
import os.path
import pickle

import sys
if sys.version_info[0] == 2:
    print ("!!")

SDIR = os.path.abspath('../svg')
FDIR = os.path.abspath('../svg/fractals')
CDIR = os.path.abspath('svg/fractals')
SHDIR= os.path.abspath( "../svg/shapes")
SHCDIR= os.path.abspath("svg/shapes")
fractals = []
shapes = []
fr_files = listdir(FDIR)
for n,fname in enumerate( sorted(fr_files) ):
    doc = parse(os.path.join(FDIR, fname))
    title = doc.getElementsByTagName('title')[0]
    fractal_name = title.attributes['data-name'].value
    fractal_title= title.firstChild.data
    fractal = {'name': fractal_name, 'title': fractal_title, 'file': os.path.join(CDIR, fname), 'no': n}
    fractals.append(fractal)

if sys.version_info[0] == 2:
 with open(os.path.join(SDIR, 'fractals.pickle'), 'w') as f:
    pickle.dump( fractals, f)
else:
 with open(os.path.join(SDIR, 'fractals.pickle'), 'wb') as f:
    pickle.dump( fractals, f)

sh_files = listdir(SHDIR)
for n,fname in enumerate( sh_files):
    doc = parse(os.path.join(SHDIR, fname))
    title = doc.getElementsByTagName('title')[0]
    shape_name = title.attributes['data-name'].value
    shape_title= title.firstChild.data
    shape = {'name': shape_name, 'title': shape_title, 'file': os.path.join(SHCDIR, fname), 'no': n}
    shapes.append(shape)
if sys.version_info[0] == 2:
 with open(os.path.join(SDIR, 'shapes.pickle'), 'w') as f:
    pickle.dump( shapes, f)
else:
 with open(os.path.join(SDIR, 'shapes.pickle'), 'wb') as f:
    pickle.dump( shapes, f)



