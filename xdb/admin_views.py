"""
 XSS Test Driver : cross browser XSS Vector Testing Tool
    Copyright (C) 2012  Erwan ABGRALL

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
