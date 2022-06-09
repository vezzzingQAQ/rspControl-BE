### 20220508
---
### 关于JWT
JsonWebToken

由三个部分组成：
header,payload,signature

##### 安装
```bash
pip install pyjwt
```
##### 调用
```python
JWTSALT = "aJ7@gT0$hJ6&iX0^dG0$gN4[cJ3`iG"

# 登录
...
# 用户名密码都对
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}
# 构造payload
payload = {
    'user_id': user.id,
    'username': user.username,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)  # 超时时间
}
jwt_result = jwt.encode(payload=payload, key=JWTSALT,
                        algorithm="HS256", headers=headers)

response = JsonResponse({"ret": 0, "jwt": jwt_result})
```
校验登录
```python
def checkLogIn(request, cjwt):
    global JWTSALT
    try:
        jwt.decode(cjwt, JWTSALT, algorithms="HS256")
        return JsonResponse({"ret": 0})
    except:
        response = JsonResponse({"ret": 1})
        return response
```
前端存储cookie
```js
...//登陆成功
//添加cookie
let cdate = new Date();
cdate.setDate(cdate.getDate() + 14);
let expireDate = cdate.toGMTString();
document.cookie = `jwt=${data.jwt};expires=${expireDate};path=/`;
```
前端读取cookie校验登录
```js
function checkLogIn(functionSucces, functionFail = () => {
    //添加cookie，记录当前URL
    let cdate = new Date();
    cdate.setDate(cdate.getDate() + 1);
    let expireDate = cdate.toGMTString();
    document.cookie = `purl=${window.location};expires=${expireDate};path=/`;
    //页面跳转
    jumpPage("./../logreg/login.html");
}) {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "http://121.40.159.180:4998/api/users/checkLogIn/" + getCookie("jwt").value + "/");
    xhr.send();
    console.log("http://121.40.159.180:4998/api/users/checkLogIn/" + getCookie("jwt").value + "/");
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            if (xhr.status >= 200 && xhr.status < 300) {
                let data = JSON.parse(xhr.response)
                let result = data.ret;
                if (result == 0) {//成功
                    functionSucces();
                } else {//没有登录
                    functionFail();
                }
            } else {
                console.error(xhr.status);
            }
        }
    }
}
```