# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from fractal import make_love
import pickle
PICKLE ='svg/fractals.pickle'
SPICKLE='svg/shapes.pickle'

def index(request):
    template = loader.get_template('index.html')
    with open(PICKLE, 'rb') as f:
        fractals = pickle.load(f)
    with open(SPICKLE, 'rb') as f:
        shapes = pickle.load(f)
    context = Context({'fractals': fractals, 'shapes': shapes})
    output = ' Hello '
    return HttpResponse(template.render(context))

def shape(request):
    no=int(request.GET['n'])
    with open(SPICKLE, 'rb') as f:
        shapes = pickle.load(f)
    sh = tuple(filter(lambda x: x['no'] == no, shapes))[0]
    with open(sh['file'], 'r') as f:
        svg = f.read()
    return HttpResponse(svg)

def fractal(request):
    no=int(request.GET['n'])
    with open(PICKLE, 'rb') as f:
        fractals = pickle.load(f)
    fr = tuple(filter(lambda x: x['no'] == no, fractals))[0]
    with open(fr['file'], 'r') as f:
        svg = f.read()
    return HttpResponse(svg)

def gen(request):
    sno = int(request.GET['shape'])
    fns = [ int(i) for i in request.GET['fractals'].split('x') ]
    with open(SPICKLE, 'rb') as f:
        shapes = pickle.load(f)

    with open(PICKLE, 'rb') as f:
        fractals = pickle.load(f)
    seq = [ tuple(filter(lambda x: x['no'] == sno, shapes))[0]['file'] ]
    for no in fns:
        seq.append( tuple(filter(lambda x: x['no'] == no, fractals))[0]['file'] )
    return HttpResponse ( make_love(seq) )
