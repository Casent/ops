# Create your views here.
# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import *
import os, shutil, subprocess
import threading
import time
import json
import re
import urllib2
import ssl
import jenkins



#   html测试页面
def test(request):
    return render_to_response("base.html")


class myThread(threading.Thread):
    def __init__(self, order):
        threading.Thread.__init__(self)
        self.order = order

    def run(self):
        status = self.order
        return status


#   获取所有用户
def auth_id():
    ua = Identification.objects.all()
    userlist = []
    for i in ua:
        userlist.append(i.username)
    return userlist


#   登录页面
def login(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username in userall:
        response = HttpResponseRedirect('/server_list/')
        return response
    return render_to_response("login.html")


#   用户认证
def authin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        response = HttpResponseRedirect('/server_list/')
        prod_name = []
        server = jenkins.Jenkins("http://jks.nonobank.com/jenkins/", username=username,
                                 password=password)
        try:
            print(server.jobs_count())
        except jenkins.JenkinsException:
            return render_to_response('login.html', {'login_err': 'Wrong username or password'})
        if Identification.objects.filter(username=username):
            Identification.objects.filter(username=username).delete()
        Identification.objects.create(username=username, password=password)
        response.set_cookie('username', username, 36000)
        prod_jobs = server.get_job_info_regex('^02')
        for i in prod_jobs:
            prod_name.append(i["name"].split("_")[1])
        for j in prod_name:
            if Server.objects.filter(server_name=j):
                pass
            else:
                Server.objects.create(server_name=j)
        return response


#   退出
def logout(req):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    return response


#   构建列表
def server_list(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    prod_jobs_name = []
    up_date = Up_oline.objects.all()
    return render_to_response("server_list.html", locals())


#   添加构建
def add_build_list(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    if request.method == 'POST':
        build_date = request.POST.get('date', '')
        project_env = request.POST.get('project_env', '')
        buidl_jobs = request.REQUEST.getlist("build_group")
        for i in buidl_jobs:
            print(i, build_date, project_env)

            if Build_job.objects.filter(jobsname=i, builddate=build_date, env=project_env):
                pass
            elif project_env == "prod":
                Build_job.objects.create(jobsname=i, env=project_env, fullname="02_" + i + "_upload_to_PROD",
                                         builddate=build_date)
                Up_server.objects.create(update=build_date, servername=i)

            else:
                Build_job.objects.create(jobsname=i, env=project_env, fullname="01_" + i + "_upload_to_PRE",
                                         builddate=build_date)
        if Up_oline.objects.filter(update=build_date):
            pass
        else:
            Up_oline.objects.create(update=build_date)
        jobs_l = Build_job.objects.filter(env=project_env, builddate=build_date)
        return render_to_response("server_list.html", locals())
    job_name = []
    prod_jobs_name = []
    prod_name = []
    j = 0
    prod_jobs = Server.objects.all()
    for i in prod_jobs:
        prod_name.append(i.server_name)
    prod_name.sort()
    for i in prod_name:
        prod_jobs_name.append(i)
        prod_jobs_name.sort()
        # print(prod_jobs_name)
        j = j + 1
        if j == 6:
            j = 0
            job_name.append(prod_jobs_name)
            job_name.sort()
            prod_jobs_name = []
    job_name.append(prod_jobs_name)
    job_name.sort()
    return render_to_response("add_build_list.html", locals())


#   构建搜索
def build_search(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    if request.method == 'POST':
        build_date = request.POST.get('editable', '')
        project_env = request.POST.get('project_env', '')
        jobs_l = Build_job.objects.filter(env=project_env, builddate=build_date)
        up_date = Up_oline.objects.all()
        return render_to_response("server_list.html", locals())


#   删除构建
def delete_build(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    if request.method == 'GET':
        server_id = request.GET.get('server_id', '')
        build_date = request.GET.get('date', '')
        project_env = request.GET.get('env', '')
        server_name = request.GET.get('server', '')
        Build_job.objects.filter(id=server_id).delete()
        if project_env == "prod":
            Up_server.objects.filter(update=build_date, servername=server_name).delete()
        jobs_l = Build_job.objects.filter(env=project_env, builddate=build_date)
        return render_to_response("server_list.html", locals())


#   构建检查列表
def build_list_check(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    if request.method == 'GET':
        update = request.GET.get('update', '')
        build_list = Up_server.objects.filter(update=update)
        upoline = Up_oline.objects.filter(update=update)
        return render_to_response("build_check_list.html", locals())


#   构建检查
def build_check(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    build_all = Up_oline.objects.all()
    return render_to_response("build_check.html", locals())


#   提交已经确认的构建
def update_build_check(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    if request.method == 'POST':
        update = request.POST.get('update', '')
        server_message = request.POST.get('server_message', '')
        value = request.POST.get('value', '')
        server = server_message.split('*')[0]
        message = server_message.split('*')[1]
        if message == "configexit":
            Up_server.objects.filter(update=update, servername=server).update(configexit=value)
        elif message == "configfinish":
            Up_server.objects.filter(update=update, servername=server).update(configfinish=value)
        elif message == "issuefinish":
            Up_server.objects.filter(update=update, servername=server).update(issuefinish=value)
        elif message == "tagfinish":
            Up_server.objects.filter(update=update, servername=server).update(tagfinish=value)
        elif message == "mergefinish":
            Up_server.objects.filter(update=update, servername=server).update(mergefinish=value)
        elif message == "doublecheckfinish":
            Up_server.objects.filter(update=update, servername=server).update(doublecheckfinish=value)
        elif message == "remake":
            print("remake")
            Up_server.objects.filter(update=update, servername=server).update(remark=value)
        elif message == "up_user":
            Up_oline.objects.filter(update=update).update(upuser=value)
        elif message == "check_user":
            Up_oline.objects.filter(update=update).update(checkuser=value)
        else:
            pass
        rjson = json.dumps({"result": "true"})
        return HttpResponse(rjson, content_type="application/json")


#   构建
def build_server_all(request):
    username = request.COOKIES.get('username', '')
    userall = auth_id()
    if username not in userall:
        return render_to_response("login.html")
    if request.method == 'POST':
        build_date = request.POST.get('server_date', '')
        project_env = request.POST.get('server_env', '')
        build_jobs = request.POST.getlist("server_list")
        user_auth = Identification.objects.filter(username=username)
        password = ""
        for i in user_auth:
            password = i.password
        server = jenkins.Jenkins("http://jks.nonobank.com/jenkins/", username=username, password=password)
        if project_env == "pre":
            param = {"branchName": "develop"}
            for i in build_jobs:
                try:
                    myThread(server.build_job("00_" + i + "_download_code", param)).start()
                except Exception as error_message:
                    return render_to_response("error.html", locals())
                Build_job.objects.filter(env=project_env, builddate=build_date, jobsname=i).update(status="1")
        else:
            num = {"RollBackNum": ""}
            for i in build_jobs:
                try:
                    server.enable_job("02_" + i + "_upload_to_PROD")
                    myThread(server.build_job("02_" + i + "_upload_to_PROD", num)).start()
                    server.disable_job("02_" + i + "_upload_to_PROD")
                except Exception as error_message:
                    return render_to_response("error.html", locals())
                Build_job.objects.filter(env=project_env, builddate=build_date, jobsname=i).update(status="1")
        jobs_l = Build_job.objects.filter(env=project_env, builddate=build_date)
        return render_to_response("server_list.html", locals())


def iplookup(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
    return render_to_response("search_ip.html", locals())
