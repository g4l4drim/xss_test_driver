from xdb import weka
from xdb.models import Vector, Browser, WebContext, Encoding, Test

__author__ = 'eal'


def data1():
    """all browsers, all vectors, utf8 & win1251, html5 and quirck modes
    """
    bset=Browser.objects.all()
    vset=Vector.objects.all()
    cset=WebContext.objects.all()[:2]
    eset=Encoding.objects.all()[:2]
    strset=weka.stringsoutput(bset,vset,cset,eset)
    return strset

def data2():
    """all browsers, all vectors, utf8 , quirck mode
    """
    bset=Browser.objects.all()
    vset=Vector.objects.all()
    cset=WebContext.objects.all()[:1]
    eset=Encoding.objects.all()[:1]
    strset=weka.stringsoutput(bset,vset,cset,eset)
    return strset

def data3():
    """all browsers, all vectors, utf8, quirck
    and html5 corresponding to the initial tests
    """
    bset=Browser.objects.all()
    vset=Vector.objects.all()
    cset=WebContext.objects.all()[:2]
    eset=Encoding.objects.all()[:1]
    strset=weka.stringsoutput(bset,vset,cset,eset)
    return strset

def browser_export_allb_allv_utf8_quirck_html5_90plus():
    top90b=[1,2,3,4,5,6,7,8,9,11,15,16,17,18,19,21,23,24,25,27,28,29,31,32,37,39,40,46,48,51,52,53,55,56,57,58,59,60,62,63,64,65,66,68,69,70,73,74,75,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,103,104,105,106,107]
    bset=Browser.objects.all().filter(id__in=top90b)
    vset=Vector.objects.all()
    cset=WebContext.objects.all()[:2]
    eset=Encoding.objects.all()[:1]
    strset=weka.stringsoutput(bset,vset,cset,eset)
    return strset

def browser_export_allb_allv_utf8_win1252_quirck_html5_90plus():
    top90b=[3,4,18,73,79,80,82,83,84,86,87,89,90,91,92,93,94,95,96,97,98,99,100,101,103,104,105,106]
    bset=Browser.objects.all().filter(id__in=top90b)
    vset=Vector.objects.all()
    cset=WebContext.objects.all()[:2]
    eset=Encoding.objects.all()[:1]
    strset=weka.stringsoutput(bset,vset,cset,eset)
    return strset

def check_duplicate(strset):
    #TODO code duplicate checking function
    return False