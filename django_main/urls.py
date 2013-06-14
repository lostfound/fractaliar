from django.conf.urls import patterns, include, url
from web import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^fractal$', views.fractal, name='fractal'),
    url(r'^shape$', views.shape, name='shape'),
    url(r'^gen$', views.gen, name='gen'),
    # Examples:
    # url(r'^$', 'fractarial.views.home', name='home'),
    # url(r'^fractarial/', include('fractarial.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
