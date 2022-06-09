from django.contrib.auth.models import User
import jwt

err_obj = {
    'state': 9
}

JWTSALT = "32rfghGwsssvez2"

def getUserFromJwt(current_jwt):
    # 根据jwt获取user
    try:
        return User.objects.get(id=jwt.decode(
            current_jwt, JWTSALT, algorithms="HS256")['user_id'])
    except:
        return None