from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'lbne.views.home', name='home'),
    # url(r'^lbne/', include('lbne.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$',include('members.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^members/',include('members.urls')),
)
