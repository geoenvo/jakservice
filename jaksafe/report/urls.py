from django.conf.urls import patterns, url
from report import views

urlpatterns = patterns('',
    url(r'^auto/$', views.report_auto, name='report_auto'),
    url(r'^adhoc/$', views.report_adhoc, name='report_adhoc'),
    url(r'^flood/$', views.report_flood, name='report_flood'),
    url(r'^impact_config/$', views.report_impact_config, name='report_impact_config'),
    url(r'^assumptions_config/$', views.report_assumptions_config, name='report_assumptions_config'),
    url(r'^aggregate_config/$', views.report_aggregate_config, name='report_aggregate_config'),
    url(r'^boundary_config/$', views.report_boundary_config, name='report_boundary_config'),
    url(r'^exposure_config/$', views.report_exposure_config, name='report_exposure_config'),
    url(r'^global_config/$', views.report_global_config, name='report_global_config'),
    url(r'^login/$', views.report_login, name='report_login'),
    url(r'^logout/$', views.report_logout, name='report_logout'),
)
