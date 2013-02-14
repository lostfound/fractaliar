#!/usr/bin/python3

from sys import argv, exit, stderr
from xml.sax import make_parser, handler, SAXParseException
from xml.dom.minidom import Document, parse
from math import pi, sin,cos,sqrt, acos, asin
from time import time
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

    def get_rec0(s, titles, dom):
        src = parse(s.filename)
        defs = src.getElementsByTagName('defs')[0]
        for g in defs.getElementsByTagName('g'):
            if 'id' in g.attributes and g.attributes['id'].value == s.rec_name:
                s.put_title(titles, dom, 0)
                return g

    def gen(s, r, node, dom, titles, z):
        l = sqrt( z.ab.x1**2 + z.ab.y1**2)
        rad = asin(z.ab.x1/l)
        transforms = []
        classes = []
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

        s.put_title(titles, dom, r)
        g = dom.createElement("g")
        if s.iam_shape:
            g.setAttribute("id", "fractal".format(r) )
        else:
            g.setAttribute("id", "rec{0}".format(r) )

        g.setAttribute("data-recursion", "{0}".format(r) )
        for m,c in zip(transforms, classes):
            use = dom.createElement('use')
            use.setAttribute( 'class', c)
            use.setAttribute( "xlink:href", "#rec{0}".format( r-1 ) )
            use.setAttribute( 'transform' ,'matrix({0})'.format(','.join(["%f" % z for z in m])) )
            g.appendChild(use)
            node.appendChild(g)

    def put_title(s, titles, dom, r):
        if s.title:
            title = dom.createElement('title')
            title.setAttribute('data-name', s.title['name'])
            title.setAttribute('data-recursion', str(r))
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


def make_love(sequence):
    fractals = []
    for a in sequence:
        p = SVGFractal()
        p.parseFile(a)
        fractals.append( p )
    new = Document()
    svg = new.createElement("svg")
    svg.setAttribute('width',"600")
    svg.setAttribute('height', "600")
    svg.setAttribute('xmlns', "http://www.w3.org/2000/svg")
    svg.setAttribute('xmlns:xlink', "http://www.w3.org/1999/xlink")
    svg.setAttribute('xmlns:ev',"http://www.w3.org/2001/xml-events")
    defs = new.createElement('defs')
    svg.appendChild(defs)
    titles = new.createElement('g')
    titles.setAttribute('id',"titles")
    svg.appendChild(titles)
    new.appendChild(svg)
    r = 0
    for fr in reversed (fractals):
        if r == 0:
            rec0 = fr.get_rec0(titles, new)
            rec0.setAttribute('id', 'rec0')
            defs.appendChild( rec0 )
        else:
            fr.gen(r, defs, new, titles, prev_fr)
        prev_fr = fr
        r+=1
    g = new.createElement('g')
    g.setAttribute('id', 'main')
    rect = new.createElement('rect')
    rect.setAttribute('fill', "white")
    rect.setAttribute( 'height', "1000")
    rect.setAttribute( 'width', "1000")
    rect.setAttribute('x', '0')
    rect.setAttribute('y', '0')
    g.appendChild(rect)
    use = new.createElement('use')
    use.setAttribute( 'stroke', "black")
    use.setAttribute( 'stroke-width',"4" )
    use.setAttribute('transform', 'translate(100,100) scale(3)' )
    use.setAttribute('xlink:href', "#fractal")
    use.setAttribute('id', "ff")
    g.appendChild(use)
    svg.appendChild(g)

    fname = 'static/fractals/{0}.svg'.format(time())
    with open(fname, "w") as f:
        new.writexml(f, newl="\n", addindent="    ", indent="    ")
    return fname


if __name__=='__main__':
    if len(argv) < 3:
        print ("Usage:", argv[0], "shape.svg", "fractal1.svg", "...")
        exit(0)
    print (make_love(argv[1:]))

