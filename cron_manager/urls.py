from django.conf.urls import patterns, include, url
from task.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:

                       url(r'^test/$', test),

                       #url(r'^reporting/$', reporting),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', login),
                       url(r'^login/$', login),
                       url(r'^logout/$', logout),
                       url(r'^authin/$', authin),
                       url(r'^server_list/$', server_list),
                       url(r'^add_build_list/$',add_build_list),
                       url(r'build_search',build_search),
                       url(r'delete_build',delete_build),
                       url(r'build_check',build_check),
                       url(r'build_list_check',build_list_check),
                       url(r'build_update_check', update_build_check),
                       url(r'build_server_all',build_server_all),
                       url(r'^iplookup/$', iplookup),


                       # url(r'^$', 'cron_manager.views.home', name='home'),
                       # url(r'^cron_manager/', include('cron_manager.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
                       )
