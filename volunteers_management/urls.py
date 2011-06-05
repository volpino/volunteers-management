from django.conf.urls.defaults import patterns, include, url
from volnet.views.views import *
from django.views.generic.simple import direct_to_template

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
    url(r'^contact/$', contact),
    url(r'^about/$', about),

    url(r'^emergencies/create/$', new_emergency),
    url(r'^facebook/', include('facebookconnect.urls')),

    url(r'^volunteers/(?P<query>\d+)/$', volunteer_desc),

    url(r'^emergencies/description/', emergency_desc), #template emergencies/desc.html  link 'join' ->!!!
    url(r'^emergencies/manage/', emergency_manage), # link a emergency_close
    url(r'^emergencies/overview/$', emergency_overview), #elenco delle emergencies, per tutti
    url(r'^emergencies/myemergencies/$', my_emergencies), #elenco delle emergencies aperte da organization

    url(r'^events/create/$', new_event), #for the member
    url(r'^events/description/', event_desc), #for organization and the member and the volunteers; se sei member da qui lo puoi chiudere!
    url(r'^events/close/', event_close), #non c'e` template
    url(r'^events/myevents/$', my_events),  #for the member
    url(r'^events/overview/$', event_overview), #list of events, per l'organization
    url(r'^events/mytask/$', my_task), #for the volunteer ; c'e` dentro il tasto 'leave'

    url(r'^members/manage/', members_manage), #for the organization

    url(r'^emergencies/join/', emergency_join), # non c'e` template: la view ti redirige alla home dopo averti aggiunto al db
    url(r'^emergencies/leave/', emergency_leave),
    url(r'^emergencies/close/', emergency_close), # per organizations
    url(r'^emergencies/call_volunteers', call_volunteers) # per organizations
                       #ti manda in emergency_manage
)
