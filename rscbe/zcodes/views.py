from django.shortcuts import render
from zcodes.models import Project
from django.contrib.auth.models import User
import jwt
from public.public import JWTSALT
from public.public import err_obj
from public.public import getUserFromJwt
from django.http import JsonResponse


def addProjectView(request):
    # 新增项目
    if request.method == 'POST':
        name = request.POST.get('name', None)
        intro = request.POST.get('intro', None)
        code = request.POST.get('code', None)
        current_jwt = request.POST.get('jwt', None)
        current_rewrite = request.POST.get('rewrite', None)
        current_user = getUserFromJwt(current_jwt)

        nameOccupied = True
        projectId = -1
        projectName = name

        if name and code and name != "" and code != "":
            if current_rewrite == "0":
                # 判断是否有重名项目
                if Project.objects.filter(title=name, user=current_user).exists():
                    nameOccupied = True
                else:
                    # 新增项目
                    current_project = Project(
                        title=name, introduction=intro, code=code, user=current_user)
                    current_project.save()
                    projectId = current_project.id
                    nameOccupied = False
            else:
                # 强制写入
                try:
                    current_project = Project.objects.get(
                        title=name, user=current_user)
                    current_project.code = code
                    current_project.introduction = intro
                    current_project.save()
                    nameOccupied = False
                except:
                    return JsonResponse(err_obj)
            return JsonResponse({
                "state": 1,
                "content": {
                    "name": projectName,
                    "id": projectId,
                    "nameOccupied": nameOccupied
                }
            })
        else:
            return JsonResponse(err_obj)
    else:
        return JsonResponse(err_obj)


def getAllProjectsView(request):
    # 获取作者的所有项目列表
    if request.method == 'POST':
        current_jwt = request.POST.get('jwt', None)
        current_user = getUserFromJwt(current_jwt)
        projects = Project.objects.filter(user=current_user)
        projectList = []
        for project in projects:
            current_intro = project.introduction
            if(current_intro == ""):
                current_intro = "没有简介哒"
            if project.state == 0:
                projectList.append({
                    "id": project.id,
                    "name": project.title,
                    "intro": current_intro,
                    "createTime": project.created_time.strftime("%Y.%m.%d"),
                })
        return JsonResponse({
            "state": 1,
            "content": {
                "projects": projectList,
            }
        })
    else:
        return JsonResponse(err_obj)


def getProjectView(request):
    # 获取相应项目
    if request.method == 'POST':
        projectId = request.POST.get('id', None)
        current_jwt = request.POST.get('jwt', None)
        current_user = getUserFromJwt(current_jwt)
        if projectId:
            try:
                current_project = Project.objects.get(
                    id=projectId, user=current_user)
                return JsonResponse({
                    "state": 1,
                    "content": {
                        "id": current_project.id,
                        "name": current_project.title,
                        "intro": current_project.introduction,
                        "code": current_project.code,
                        "createTime": current_project.created_time.strftime("%Y.%m.%d"),
                    }
                })
            except:
                return JsonResponse(err_obj)
        else:
            return JsonResponse(err_obj)
    else:
        return JsonResponse(err_obj)


def delProjectView(request):
    # 删除指定的项目
    if request.method == 'POST':
        projectId = request.POST.get('id', None)
        current_jwt = request.POST.get('jwt', None)
        current_user = getUserFromJwt(current_jwt)
        if projectId:
            try:
                current_project = Project.objects.get(
                    id=projectId, user=current_user)
                current_project.state = 1
                current_project.save()
                return JsonResponse({
                    "state": 1,
                    "content": {
                        "id": current_project.id,
                        "name": current_project.title,
                    }
                })
            except:
                return JsonResponse(err_obj)
        else:
            return JsonResponse(err_obj)
    else:
        return JsonResponse(err_obj)
