#coding=utf-8
from django.db import models


#   身份认证

class Identification(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
#    access_token = models.CharField(max_length=255)
    authority = models.CharField(max_length=255)
    def __unicode__(self):
        return self.username

#   agent 执行用户
class Server_user(models.Model):
    username = models.CharField(max_length=50)
    sudo = models.CharField(max_length=50)
    def __unicode__(self):
        return self.username

class Build_job(models.Model):
     jobsname = models.CharField(max_length=200)
     env = models.CharField(max_length=50)
     fullname = models.CharField(max_length=100)
     builddate = models.CharField(max_length=50)
     status = models.CharField(max_length=50)
     def __unicode__(self):
        return self.jobsname

class Up_oline(models.Model):
     update = models.CharField(max_length=200)
     upuser = models.CharField(max_length=50)
     checkuser = models.CharField(max_length=100)
     def __unicode__(self):
        return self.update

class Up_server(models.Model):
     update = models.CharField(max_length=200)
     servername = models.CharField(max_length=200)
     configexit = models.CharField(max_length=50)
     configfinish = models.CharField(max_length=50)
     issuefinish = models.CharField(max_length=100)
     tagfinish = models.CharField(max_length=100)
     mergefinish = models.CharField(max_length=100)
     doublecheckfinish = models.CharField(max_length=100)
     remark = models.CharField(max_length=500)
     def __unicode__(self):
        return self.servername


class Server(models.Model):
    server_name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.update