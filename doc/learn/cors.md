### 20220508
---
### django跨域解决方案

#### 下载库文件
```bash
pip install django-cors-headers
```

#### 配置设置文件
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]
```
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```
middleware必须放在开头

```python 
# 允许所有域名跨域(优先选择)
CORS_ORIGIN_ALLOW_ALL = True

# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True
```

#### 一般csrf也只能关掉，到目前没找出解决办法
把midware中csrf那一行注释掉
