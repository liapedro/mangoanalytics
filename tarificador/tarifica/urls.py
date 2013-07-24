from django.conf.urls import patterns, url
from tarifica import views

urlpatterns = patterns('',
   url(r'^setupprovider/(?P<asterisk_id>\d+)$', views.setupAddProviderInfo, name = 'setupprovider'),
   url(r'^setupchangeprovider/(?P<id>\d+)$', views.setupChangeProviderInfo, name = 'setupchangeprovider'),
   url(r'^setupchangebundles/(?P<id>\d+)$', views.setupChangeBundles, name = 'setupchangebundles'),
   url(r'^viewbundles/(?P<id>\d+)$', views.viewBundles, name = 'viewbundles'),
   url(r'^setupbasetariffs/(?P<asterisk_id>\d+)$', views.setupAddBaseTariffs, name = 'setupbasetariffs'),
   #url(r'^setupbundles/', views.setupAddBundles, name = 'setupbundles'),
   url(r'^setupbundles/(?P<id>\d+)$', views.setupAddBundles, name = 'setupbundles'),
   url(r'^deleteprovider/(?P<id>\d+)$', views.deleteProvider, name = 'deleteprovider'),
   url(r'^deletebundle/(?P<id>\d+)$', views.deleteBundle, name = 'deletebundle'),
   url(r'^thanks$', views.thanks, name = 'gracias'),
   url(r'^contact$',views.thanks, name = 'contacto'),
   url(r'^dashboardtroncales$', views.dashboardTrunks, name = 'dashboardtroncales')
   url(r'^dashboard$', views.generalDashboard, name = 'generaldashboard')
)