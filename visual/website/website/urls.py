from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^view/(\d+)/(\d+)/$', 'viewQuestion.views.view', name='view'),
    # url(r'^image/([\w-]+)/$', 'viewQuestion.views.getImage', name='image'),
    url(r'^main/$', 'viewQuestion.views.main', name="main"),
    url(r'^deleteQuestion/(\d+)/$', 'viewQuestion.views.deleteQuestion', name="delete"),
    #url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
)
