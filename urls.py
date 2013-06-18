from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xssdb.views.home', name='home'),
    # url(r'^xssdb/', include('xssdb.foo.urls')),
    url(r'^admin/shazzerimport/$', 'xss_test_driver.xdb.admin_views.shazzer_import'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #website index :
    url(r'^', include('xdb.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
