from django.conf.urls import patterns, url
from report import views

urlpatterns = patterns('',
    #url(r'^auto/$', views.report_auto, name='report_auto'),
    url(r'^adhoc/$', views.report_adhoc, name='report_adhoc'),
    url(r'^impact_config/$', views.report_impact_config, name='report_impact_config'),
)
