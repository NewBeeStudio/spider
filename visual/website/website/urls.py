from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
import settings

urlpatterns = patterns('',
    url(r'^view/(\d+)/(\d+)/(\d|-1)/(\d|-1)/$', 'viewQuestion.views.view', name='view'),
    # url(r'^images/images/([\w-]+)/$', 'viewQuestion.views.getImage', name='image'),
    url(r'^main/$', 'viewQuestion.views.main', name="main"),
    url(r'^deleteQuestion/(\d+)/$', 'viewQuestion.views.deleteQuestion', name="delete"),
    url(r'^excel/(\d+|-1)/(\d+|-1)/(\d|-1)/(\d|-1)/$', 'viewQuestion.views.excel', name="excel"),
    #url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()