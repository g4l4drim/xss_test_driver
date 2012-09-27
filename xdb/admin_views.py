__author__ = 'eal'
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.forms import ModelForm
from django.contrib.admin.views.decorators import staff_member_required
from xdb.models import Vector, VectorFamily
from xdb.models import *
from xdb.util import *


def shazzer_import(request):
    if request.method=='POST':
        form=ShazzerForm(request.POST)
        if form.is_valid():
            vectors=shazzer_to_vectors(form.cleaned_data["url"])
            vector_desc=shazzer_vector_desc(int(form.cleaned_data["id"]))
            family=VectorFamily()
            family.name=vector_desc["description"]
            family.desc="Imported from Shazzer \nBy:"+\
                        str(vector_desc["username"])+\
                        "\nSource:\n"+str(vector_desc["vector"])
            family.save()
#TODO: Create a default suite for the import
#TODO: Automatically add model data for Context and Encoding
#TODO: Choose a default Context and a Default Encoding (quirks mode with text/html ?)

            for v in vectors:
                vect=Vector()
                vect.desc=vector_desc["description"]+\
                        "\nImported from Shazzer \nBy:"+\
                        str(vector_desc["username"])+\
                        "\nSource:\n"+str(vector_desc["vector"])
                vect.source="http://shazzer.co.uk/vector/"+shazzer_link(vector_desc)
                vect.vector=v
                vect.save()
                vect.family.add(family)
            return redirect("/admin/")
            
    else:
        form=ShazzerForm()
        return render_to_response('shazzerimport.html',{'form':form,},context_instance=RequestContext(request))

shazzer_import = staff_member_required(shazzer_import)

class ShazzerForm(forms.Form):
    url=forms.URLField()
    id=forms.IntegerField()
