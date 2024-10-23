# 介绍
hackergame 邮件API，python实现

按照 https://github.com/ustclug/hackergame/blob/b3a63e67270dc7b1b11491d8692d30caa54d847f/frontend/auth_providers/external.py#L24C5-L24C5 的 API 规范，提供邮件网关 API

# 使用说明

安装依赖之后，配置main.py中的配置，然后运行即可

目前测试似乎在ssl可以使用，tls无法使用，待后续更新


# ssl证书问题

更新服务器证书
```shell
sudo apt-get update
sudo apt-get install ca-certificates
```