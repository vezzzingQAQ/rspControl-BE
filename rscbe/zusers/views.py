from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import jwt
import datetime
from public.public import JWTSALT
from public.public import err_obj

def actionRegisterView(request):
    current_validCode = '020v23'
    # 用户注册
    if request.method == 'POST':
        userName = request.POST.get('userName', None)
        passWord = request.POST.get('passWord', None)
        validCode = request.POST.get('validCode', None)

        para_userNameValid = False
        para_validCodeValid = False

        if User.objects.filter(username=userName):
            pass
        else:
            if userName:
                if len(userName) != 0:
                    para_userNameValid = True

        if validCode != current_validCode:
            para_validCodeValid = False
        else:
            para_validCodeValid = True

        if(para_userNameValid and para_validCodeValid):
            current_user = User.objects.create_user(
                username=userName, password=passWord)
            current_user.save()

        return JsonResponse({
            "state": 1,
            "content": {
                "userNameValid": para_userNameValid,
                "validCodeValid": para_validCodeValid,
                "userName": userName,
            }
        })
    else:
        return JsonResponse(err_obj)


def actionLoginView(request):
    global JWTSALT
    # 用户登录
    if request.method == 'POST':
        userName = request.POST.get('userName', None)
        passWord = request.POST.get('passWord', None)

        para_isLogin = False
        para_jwt = None

        if User.objects.filter(username=userName):
            current_user = authenticate(username=userName, password=passWord)
            print(current_user)
            if current_user:
                if current_user.is_active:
                    # login(request, current_user)
                    para_isLogin = True
                    # jwt加密
                    jwt_headers = {
                        'typ': 'jwt',
                        'alg': 'HS256'
                    }
                    # 构造payload
                    jwt_payload = {
                        'user_id': current_user.id,
                        'username': current_user.username,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # 超时时间
                    }
                    para_jwt = jwt.encode(payload=jwt_payload, key=JWTSALT,
                                          algorithm="HS256", headers=jwt_headers)

        return JsonResponse({
            "state": 1,
            "content": {
                "isLogin": para_isLogin,
                "userName": userName,
                "jwt": para_jwt
            }
        })
    else:
        return JsonResponse(err_obj)


def _checkJWT(current_jwt):
    global JWTSALT
    # 检查jwt
    try:
        print(current_jwt)
        jwt.decode(current_jwt, JWTSALT, algorithms="HS256")
        return True
    except:
        return False


def checkIsLogin(request):
    # 检查是否登录
    if request.method == 'POST':
        para_isLogin = False
        current_jwt = request.POST.get('jwt', None)
        if _checkJWT(current_jwt):
            para_isLogin = True
        return JsonResponse({
            "state": 1,
            "content": {
                "isLogin": para_isLogin
            }
        })
    else:
        return JsonResponse(err_obj)


def getUserName(request):
    # 获取用户名
    if request.method == 'POST':
        para_isLogin = False
        para_userName = None
        current_jwt = request.POST.get('jwt', None)
        if _checkJWT(current_jwt):
            para_isLogin = True
            current_user = User.objects.get(id=jwt.decode(
                current_jwt, JWTSALT, algorithms="HS256")['user_id'])
            para_userName = current_user.username
        return JsonResponse({
            "state": 1,
            "content": {
                "isLogin": para_isLogin,
                "userName": para_userName
            }
        })
    else:
        return JsonResponse(err_obj)
