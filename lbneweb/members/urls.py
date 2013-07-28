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
    url(r'^collaborator/(?P<pk>\d+)/$', views.CollaboratorView.as_view(), name='collaborator'),
    url(r'^institution/(?P<pk>\d+)/$', views.InstitutionView.as_view(), name='institution'),
    url(r'^role/(?P<pk>\d+)/$', views.RoleView.as_view(), name='role'),
    url(r'^export/(?P<filename>[-\.\w]*)$', views.export, name='export'),
)
