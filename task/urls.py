from django.conf.urls import patterns, url
from task.views import *

 
urlpatterns = patterns('',
    url(r'^$', login, name='login'),
    url(r'^plan_list/$',plan_list),
    url(r'^issue_file/$',issue_file),
    url(r'^server_list/$',server_list),
    url(r'^add_server/$',add_server),
    url(r'^issue_plan/$',issue_plan),
url(r'^add_build_list/$',add_build_list),

)
