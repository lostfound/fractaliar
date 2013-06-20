#!/usr/bin/python3

from sys import argv, exit, stderr
from xml.sax import make_parser, handler, SAXParseException
from xml.dom.minidom import Document, parse
from math import pi, sin,cos,sqrt, acos, asin
from time import time
import os.path.abspath
import sys
class Line:
    def __init__(s, attrs):
        xxyy = [float(attrs[k]) for k in ('x1','x2', 'y1', 'y2')]
        s.line = tuple(zip(xxyy[:2], xxyy[2:]))
        s.x1 = xxyy[0]
        s.x2 = xxyy[1]
        s.y1 = xxyy[2]
        s.y2 = xxyy[3]
        s.yflip = False
        s.xflip = False
        s.classes = attrs.get('class')

        if 'data-flipy' in attrs:
            s.yflip = True
        s.calcangle()

    def calcangle(s):
        x = s.x2-s.x1
        y = s.y2-s.y1
        s.length =  sqrt(x**2+y**2)

        s.rad = acos(float(x/s.length))
        if y < 0: 
            s.rad*=-1
        s.angle = s.rad * 180/pi

    def __repr__(s):
        return " ".join([repr(s.line[0]), repr(s.line[1]), repr(s.angle), repr(s.length)])

def multiplicate_mx(m1, m2):
    m=[0,0,0,0,0,0]
    m[0]=m1[0]*m2[0] + m1[2]*m2[1]
    m[1]=m1[1]*m2[0] + m1[3]*m2[1]
    m[2]=m1[0]*m2[2] + m1[2]*m2[3]
    m[3]=m1[1]*m2[2] + m1[3]*m2[3]
    m[4]=m1[0]*m2[4] + m1[2]*m2[5]+m1[4]
    m[5]=m1[1]*m2[4] + m1[3]*m2[5]+m1[5]
    return m

class SVGFractal(handler.ContentHandler):
    def __init__(s):
        s.path=[]
        s.is_rec = False
        s.is_main = False
        s.flines = []
        s.lines = []
        s.olines = []
        s.iam_shape=False
        s.content = None
        s.title = None

    def parseFile(s, fileName):
        s.filename = fileName
        try:
            parser = make_parser()
            parser.setContentHandler(s)
            parser.parse(fileName)
            return True

        except SAXParseException:
            return False

    def characters(s, content):
        if s.content != None:
            s.content = s.content + content

    def startElement(s, name, attrs):
        if name == 'title' and s.path[-1] == 'svg':
            s.title = {'name': attrs.get('data-name')}
            s.content = ''
        elif s.is_rec:
            if name == 'line':
                c = attrs.get('class').split()
                if 'frdef' in c:
                    s.ab = Line(attrs)
                if 'frline' in c:
                    s.flines.append( Line(attrs) )
                if 'oline' in c:
                    s.olines.append( Line(attrs) )
        elif s.is_main:
            if name == 'line':
                c = attrs.get('class').split()
                if 'frline' in c:
                    s.flines.append( Line(attrs) )
            

        elif name == 'g' and s.path[-1] == 'defs' and attrs.get('data-type') == 'fractal':
            s.rec_name = attrs.get('id')
            s.is_rec = True

        elif name == 'g' and s.path[-1] == 'defs' and attrs.get('id') == 'main':
            s.is_main = True
            s.iam_shape = True
        s.path.append(name)

    def get_rec0(s, titles, dom, layout):
        src = parse(s.filename)
        defs = src.getElementsByTagName('defs')[0]
        for g in defs.getElementsByTagName('g'):
            if sys.version_info[0] == 2:
                if g.attributes.has_key('id') and g.attributes['id'].value == s.rec_name:
                    s.put_title(titles, dom, 0, layout)
                    return g
            elif 'id' in g.attributes and g.attributes['id'].value == s.rec_name:
                s.put_title(titles, dom, 0, layout)
                return g

    def gen(s, r, node, dom, titles, z, layout=0, psc=0):
        l = sqrt( z.ab.x1**2 + z.ab.y1**2)
        rad = asin(z.ab.x1/l)
        transforms = []
        classes = []
        scales=[]
        for f in s.flines:
            classes.append(f.classes)
            a = f.rad
            scale = f.length/z.ab.length
            xrad = pi/2-(2*pi - a) - rad

            cl=l*scale
            x = f.x1 - cl*cos(xrad)
            y = f.y1 - cl*sin(xrad)
            mt = [1,0,0,1,x,y]
            ms = [scale,0,0,scale,0,0]
            mr = [cos(a),sin(a),-sin(a),cos(a),0,0]
            m = multiplicate_mx(mt, mr)
            m = multiplicate_mx(m, ms)
            if f.yflip:
                m = multiplicate_mx(m, [1,0,0,-1,0,z.ab.y1*2])
            transforms.append(m)
            scales.append(scale)

        s.put_title(titles, dom, r, layout)
        g = dom.createElement("g")
        if s.iam_shape:
            g.setAttribute("id", "fractal{0}".format(layout) )
        else:
            g.setAttribute("id", "l{1}rec{0}".format(r, layout) )

        g.setAttribute("data-recursion", "{0}".format(r) )
        g.setAttribute("data-layout", "{0}".format(layout) )

        for m,c,scale in zip(transforms, classes, scales):
            use = dom.createElement('use')
            use.setAttribute( 'class', c)
            use.setAttribute( "xlink:href", "#l{1}rec{0}".format( r-1, layout ) )
            use.setAttribute( 'transform' ,'matrix({0})'.format(','.join(["%f" % x for x in m])) )
            g.appendChild(use)
            node.appendChild(g)
            for ln in z.olines:
                line = dom.createElement('line')
                line.setAttribute( 'class', "oline")
                for n,v in zip( ['x1', 'y1', 'x2', 'y2'], [ln.x1, ln.y1, ln.x2, ln.y2] ):
                    line.setAttribute(n,str(v))
                line.setAttribute( 'stroke-width', str(1/(scale+psc)) )
                line.setAttribute( 'transform' ,'matrix({0})'.format(','.join(["%f" % x for x in m])) )
                g.appendChild(line)

        return scale+psc

    def put_title(s, titles, dom, r, layout):
        if s.title:
            title = dom.createElement('title')
            title.setAttribute('data-name', s.title['name'])
            title.setAttribute('data-recursion', str(r))
            title.setAttribute('data-layout', str(layout))
            title.appendChild( dom.createTextNode(s.title['text']) )
            titles.appendChild(title)


    def endElement(s, name):
        if name == 'title' and s.content:
            s.title['text'] = s.content
            s.content = None
        if s.is_rec and name == 'g':
            s.is_rec = None
        if s.is_main and name == 'g':
            s.is_main = None

        s.path=s.path[:-1]


def prad(s, r):
    stderr.write (' '.join([s, str( r*180/pi), '(',str(r),')','\n']))



def make_SVG():
    new = Document()
    svg = new.createElement("svg")
    svg.setAttribute('width',"600")
    svg.setAttribute('height', "600")
    svg.setAttribute('xmlns', "http://www.w3.org/2000/svg")
    svg.setAttribute('xmlns:xlink', "http://www.w3.org/1999/xlink")
    svg.setAttribute('xmlns:ev',"http://www.w3.org/2001/xml-events")
    defs = new.createElement('defs')
    svg.appendChild(defs)
    new.appendChild(svg)

    titles = new.createElement('g')
    titles.setAttribute('id',"titles")
    svg.appendChild(titles)

    g = new.createElement('g')
    g.setAttribute('id', 'main')
    rect = new.createElement('rect')
    rect.setAttribute('fill', "white")
    rect.setAttribute( 'height', "1000")
    rect.setAttribute( 'width', "1000")
    rect.setAttribute('x', '0')
    rect.setAttribute('y', '0')
    #g.appendChild(rect)
    svg.appendChild(g)
    fname = os.path.abspath ( 'static/fractals/{0}.svg'.format(time()) )
    with open(fname, "w") as f:
        new.writexml(f, newl="\n", addindent="    ", indent="    ")
    return fname

def getByID(root, tag, idv):
    for e in root.getElementsByTagName(tag):
        if sys.version_info[0] == 2:
            if e.attributes.get('id') and e.attributes['id'].value == idv:
                return e
        elif 'id' in e.attributes and e.attributes['id'].value == idv:
            return e

def removeLayout(root, layout):
    defs = root.getElementsByTagName('defs')[0]
    for e in root.getElementsByTagName('g') + root.getElementsByTagName('title'):
        if sys.version_info[0] == 2:
            if e.attributes.has_key('data-layout') and e.attributes['data-layout'].value == str(layout):
                e.parentNode.removeChild(e)
        elif 'data-layout' in e.attributes and e.attributes['data-layout'].value == str(layout):
            e.parentNode.removeChild(e)
    main = getByID(root, 'g', 'main')
    use = getByID(main, 'use', 'ff{0}'.format(layout) )
    if use:
        main.removeChild(use)

def stripFile(fname):
    with open(fname, 'r') as f:
        lines = filter(lambda x: x.strip() != '', f.readlines())
    with open(fname, 'w') as f:
        for line in lines:
            f.write(line)


def make_love(sequence, layout=0, name=None):
    if not name:
        fname = make_SVG()
    else:
        fname = name

    new = parse(fname)
    defs = new.getElementsByTagName('defs')[0]
    svg = new.getElementsByTagName('svg')[0]
    if name:
        removeLayout(new, layout)
    fractals = []

    for a in sequence:
        p = SVGFractal()
        p.parseFile(a)
        fractals.append( p )

    titles = getByID(new, 'g', 'titles')

    r = 0
    psc = 0
    for fr in reversed (fractals):
        if r == 0:
            rec0 = fr.get_rec0(titles, new, layout)
            rec0.setAttribute('id', 'l{0}rec0'.format(layout))
            rec0.setAttribute('data-layout', '{0}'.format(layout))
            defs.appendChild( rec0 )
        else:
            psc = fr.gen(r, defs, new, titles, prev_fr, layout, psc)
        prev_fr = fr
        r+=1

    g = getByID(new, 'g', 'main')
    use = new.createElement('use')
    use.setAttribute( 'stroke', "black")
    use.setAttribute( 'stroke-width',"4" )
    use.setAttribute('transform', 'translate(100,100) scale(3)' )
    use.setAttribute('xlink:href', "#fractal{0}".format(layout))
    use.setAttribute('id', "ff{0}".format(layout))
    g.appendChild(use)
    svg.appendChild(g)

    with open(fname, "w") as f:
        new.writexml(f, newl="\n", addindent="    ", indent="    ")
    stripFile(fname)
    return fname


if __name__=='__main__':
    if len(argv) < 3:
        print ("Usage:", argv[0], "shape.svg", "fractal1.svg", "...")
        exit(0)
    print (make_love(argv[1:], 0, '8.svg'))

