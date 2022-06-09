from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    title = models.CharField(default="新建项目", max_length=20, blank=False)
    introduction = models.TextField("介绍", max_length=1000, blank=True)
    state = models.IntegerField(default=0)  # 状态:0云存，1删除
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField(default="", blank=False)
    goodNum = models.IntegerField(default=0)

    def __str__(self):
        return(str(self.id)+",标题:"+self.title+",作者:"+self.user.username+",状态码:"+str(self.state)+",修改时间:"+str(self.created_time))
