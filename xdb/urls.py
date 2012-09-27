from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #website index :
    url(r'^$','xdb.views.index'),
    url(r'/^$','xdb.views.index'),
    url(r'^index/$', 'xdb.views.index'),
    #vector display
    url(r'^vectors/', 'xdb.views.vectors'),
    #xss manual testing
    url(r'^xss/(?P<vector_id>\d+)/', 'xdb.views.xss'),
    #suite management and execution
    url(r'^suites','xdb.views.suites'),
    url(r'^suite/(?P<suite_id>\d+)/$','xdb.views.suite_content'),
    url(r'^suite/(?P<suite_id>\d+)/run$','xdb.views.suite_run'),
    url(r'^suite/(?P<suite_id>\d+)/results$','xdb.views.suite_results'),

    url(r'test/(?P<vector_id>\d+)/(?P<context_id>\d+)/(?P<encoding_id>\d+)/(?P<verdict>.+)?','xdb.views.test'),
    url(r'test/next','xdb.views.next_test'),
    url(r'test/resume','xdb.views.resume_test'),
    #xss includes management (external scripts loaded through src and so on
    url(r'(?P<context>(test|xss))/inc/(?P<vector_id>\d+)/(?P<context_id>\d+)/(?P<encoding_id>\d+)/payload\.(?P<type>.+)','xdb.views.inc'),

    #browser management
    url(r'^browser/(?P<action>(add|list))','xdb.views.browser'),
    #browser test result display :
    url(r'^browser/(?P<browser_id>\d+)/','xdb.views.browser_results'),
    url(r'^filter$','xdb.views.filter'),
    url(r'^familyfilter$','xdb.views.family_filter'),
    url(r'^results$','xdb.views.results'),
    url(r'^myresults$','xdb.views.my_results'),
    url(r'^all_results$','xdb.views.all_results'),

)