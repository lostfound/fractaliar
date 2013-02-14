#!/usr/bin/python3

from sys import argv, exit, stderr
from xml.sax import make_parser, handler, SAXParseException
from xml.dom.minidom import Document, parse
from math import pi, sin,cos,sqrt, acos, asin
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

class SVGParser(handler.ContentHandler):
    def __init__(s):
        s.path=[]
        s.is_rec = False
        s.is_main = False
        s.flines = []
        s.lines = []

    def parseFile(s, fileName):
        s.filename = fileName
        try:
            parser = make_parser()
            parser.setContentHandler(s)
            parser.parse(fileName)
            return True

        except SAXParseException:
            return False

    def startElement(s, name, attrs):
        if s.is_rec:
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
                    s.lines.append( Line(attrs) )
            

        elif name == 'g' and s.path[-1] == 'defs' and attrs.get('data-type') == 'fractal':
            s.rec_name = attrs.get('id')
            s.is_rec = True

        elif name == 'g' and s.path[-1] == 'defs' and attrs.get('id') == 'main':
            s.is_main = True
        s.path.append(name)

    def createSVG(s, outfile, r = 1):
        src = parse(s.filename)
        new = Document()
        svg = src.getElementsByTagName('svg')[0]
        new.appendChild(svg)
        defs = new.getElementsByTagName('defs')[0]
        #rec0 = new.getElementById(s.rec_name)
        #print (rec0.appendChil)
        
        title = svg.getElementsByTagName('title')[0]
        if 'data-type' in title.attributes and title.attributes['data-type'].value == 'shape':
            s.shapegen(defs, new )
        else:
            s.gen(r, defs, new )
        svg = new.getElementsByTagName('svg')[0]
        #svg.appendChild(rect)
        #svg.setAttribute('width', "1000")
        #svg.setAttribute('height', "1000")
        #use = new.createElement('use')
        #use.setAttribute("xlink:href", "#fractal")
        #use.setAttribute("stroke-width", "4")
        #use.setAttribute("transform", "translate(100,-300) scale(8)")
        #use.setAttribute("stroke", "black")
        #use.setAttribute("stroke-width", "2")
        #svg.appendChild(use)

        with open(outfile, "w") as f:
            new.writexml(f, newl="\n", addindent="    ", indent="    ")

    def gen(s, r, node, dom):
        l = sqrt( s.ab.x1**2 + s.ab.y1**2)
        rad = asin(s.ab.x1/l)
        transforms = []
        classes = []
        for f in s.flines:
            classes.append(f.classes)
            a = f.rad
            scale = f.length/s.ab.length
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
                m = multiplicate_mx(m, [1,0,0,-1,0,s.ab.y1*2])
            transforms.append(m)

        for n in range(1, r+1):
            g = dom.createElement("g")
            g.setAttribute("id", "{1}{0}".format(n, s.rec_name) )
            g.setAttribute("data-recursion", "{0}".format(n) )
            for m,c in zip(transforms, classes):
                use = dom.createElement('use')
                use.setAttribute( 'class', c)
                use.setAttribute( "xlink:href", "#{1}{0}".format( n-1 if n>1 else '', s.rec_name ) )
                use.setAttribute( 'transform' ,'matrix({0})'.format(','.join(["%f" % z for z in m])) )
                g.appendChild(use)
            node.appendChild(g)
                
    def shapegen(s, node, dom):
        g = dom.createElement("g")
        g.setAttribute("id", "fractal")
        transforms = []
        for f in s.lines:
            a = f.rad
            scale = f.length/s.ab.length
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
                m = multiplicate_mx(m, [1,0,0,-1,0,s.ab.y1*2])
            transforms.append(m)

        for m in transforms:
            use = dom.createElement('use')
            use.setAttribute( "xlink:href", "rec0" )
            use.setAttribute( 'transform', "matrix({0})".format(','.join(["%f" % z for z in m])) )
            g.appendChild(use)
        node.appendChild(g)



    def endElement(s, name):
        if s.is_rec and name == 'g':
            s.is_rec = None
        if s.is_main and name == 'g':
            s.is_main = None

        s.path=s.path[:-1]


def prad(s, r):
    stderr.write (' '.join([s, str( r*180/pi), '(',str(r),')','\n']))

if __name__=='__main__':
    if len(argv) != 3:
        print ("Usage:", argv[0], "svgfile.svg", "out.svg")
        exit(0)
    p = SVGParser()
    p.parseFile(argv[1])
    p.createSVG(argv[2], 1)



