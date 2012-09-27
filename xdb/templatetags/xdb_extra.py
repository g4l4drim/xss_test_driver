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