__author__ = 'eal'

from xdb.models import *
#WEKA output of xss test driver results

def csv_output(browsers,vectors,context,encoding,binary):
    tres=Test.objects.all()
    out="num"
    for v in vectors:
        for c in context:
            for e in encoding:
                out+=","+str(v.id)+"-"+str(c.id)+"-"+str(e.id)
    out+=",browser"
    out+="\n"
    for b in browsers:
        spcount=0
        tcount=0
        #generate each line
        out+=str(b.id)
        for v in vectors:
            for c in context:
                for e in encoding:
                    t=tres.filter(vector=v,browser=b,context=c,encoding=e)
                    tcount+=1
                    if t.count()==1:
                        spcount+=1
                        tr=t[0]
                        if binary:
                            if tr.result=="PASS":
                                out+=",1"
                            else:
                                out+=",0"
                        else:
                            out+=","+str(tr.result)
                    if t.count()==0:
                        if binary:
                            out+=",?"
                        else:
                            out+=",?"
        out+=",#"+str(b.id)+" "+str(b.name.replace(",","").replace(".","_").replace("/","").replace("\t","_"))+"("+("%.2f%%" % (100.0*(spcount*1.0)/(tcount*1.0)))+")"
        out+="\n"
    return out

def family_csv_output(family_set,vectors,context,encoding,binary,validity):
    tres=Test.objects.all()
    out="browser"
    tres=Test.objects.all()
    valid_browsers=[]
    if validity=="all":
        valid_browsers=Browser.objects.all()
    if validity=="valid":
        valid_browsers=Browser.objects.filter(valid_ua=True)
    if validity=="unvalid":
        valid_browsers=Browser.objects.filter(valid_ua=False)

    for v in vectors:
        for c in context:
            for e in encoding:
                out+=","+str(v.id)+"-"+str(c.id)+"-"+str(e.id)
    out+=",quality"
    out+=",family\n"
    for f in family_set:
        browsers=valid_browsers.filter(family=f)
        for b in browsers:
            spcount=0
            tcount=0
            out+="#"+str(b.id)+" "+str(b.name.replace(",","").replace(".","_").replace("/","").replace("\t","_"))
            for v in vectors:
                for c in context:
                    for e in encoding:
                        t=tres.filter(vector=v,browser=b,context=c,encoding=e)
                        tcount+=1
                        if t.count()==1:
                            tr=t[0]
                            if binary:
                                if tr.result=="PASS":
                                    out+=",1"
                                    spcount+=1
                                else:
                                    out+=",0"
                            else:
                                if tr.result=="PASS":
                                    out+=",P"
                                    spcount+=1
                                if tr.result=="SENT":
                                    out+=",S"
                                    spcount+=1
                        if t.count()==0:
                            if binary:
                                out+=",?"
                            else:
                                out+=",?"
            out+=","+("%.2f" % (100.0*(spcount*1.0)/(tcount*1.0)))
            out+=","+f.name
            out+="\n"
    return out

def stringsoutput(bset,vset,cset,eset):
    browsers={}
    for b in bset:
        bsign=""
        spcount=0
        tcount=0
        for v in vset:
            for c in cset:
                for e in eset:
                    t=Test.objects.filter(vector=v,browser=b,context=c,encoding=e)
                    tcount+=1
                    if t:
                        spcount+=1
                        t=t[0]
                        if t.result=="SENT":
                            bsign+="s"
                        if t.result=="PASS":
                            bsign+="p"
                    else:
                        bsign+="n"
        browsers[bsign]=str(b)+"("+("%.2f%%" % (100.0*(spcount*1.0)/(tcount*1.0)))+")"
    return browsers