### 20220509
---
### 树莓派wifi炸了咋办
##### 修改配置文件
位置:etc/wpa...../wpa.....config
##### 重新连接
```bash
wpa_cli -i wlan0 reconfigure
```
