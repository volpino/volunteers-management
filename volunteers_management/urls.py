from django.conf.urls.defaults import patterns, include, url
from volnet.views.views import *
from volnet.views.single_queries import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'volnet.views.views.home', name='home'),
    # url(r'^volunteers_management/', include('volunteers_management.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/$', profile),
)
