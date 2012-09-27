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
===========================================================================

This templatetags sucks !!! it just blows up performance when rendering 
results
"""

from django import template
from xdb.models import Test

__author__ = 'eal'
register = template.Library()
def vector_result(browser,vector):
    #test result for the given vector
    t=Test.objects.filter(browser=browser,vector=vector,result="PASS")
    if t:
        return t.count()
    else:
        return "0"

def browser_result(vector,browser):
    #test result for the given vector
    t=Test.objects.filter(browser=browser,vector=vector,result="PASS")
    if t:
        return t.count()
    else:
        return "0"

register.filter('vector_result',vector_result)
register.filter('browser_result',browser_result)