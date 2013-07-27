from django.conf.urls import patterns, include, url

from members import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'lbne.views.home', name='home'),
    # url(r'^lbne/', include('lbne.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)
