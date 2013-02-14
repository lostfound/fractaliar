#!/usr/bin/python3
from xml.dom.minidom import Document, parse
from os import listdir
import os.path
import pickle

SDIR = '../svg'
FDIR='../svg/fractals'
CDIR='svg/fractals'
SHDIR="../svg/shapes"
SHCDIR="svg/shapes"
fractals = []
shapes = []
fr_files = listdir(FDIR)
for n,fname in enumerate( fr_files):
    doc = parse(os.path.join(FDIR, fname))
    title = doc.getElementsByTagName('title')[0]
    fractal_name = title.attributes['data-name'].value
    fractal_title= title.firstChild.data
    fractal = {'name': fractal_name, 'title': fractal_title, 'file': os.path.join(CDIR, fname), 'no': n}
    fractals.append(fractal)
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
with open(os.path.join(SDIR, 'shapes.pickle'), 'wb') as f:
    pickle.dump( shapes, f)



