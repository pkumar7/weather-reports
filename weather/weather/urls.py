from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weather.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^report', include('report.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
