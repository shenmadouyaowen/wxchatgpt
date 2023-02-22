# wxchatgpt
及其简单的chatgpt对接微信公众号

使用<a href="https://github.com/offu/WeRoBot">werobot</a> 自动跟公众号配对

使用 <a href="https://github.com/acheong08/ChatGPT">ChatGPT</a> 自动对接chatgpt



# 安装

 `pip3 install revChatGPT`
 
 `pip3 install werobot`
 
 安装 redis ,有宝塔的直接进软件管理页面安装redis,没有的使用以下一键安装
 
 ``` 
 mkdir -p /mydata/redis/conf
touch /mydata/redis/conf/redis.conf
docker run -p 6379:6379 --name redis \
-v /mydata/redis/data:/data \
-v /mydata/redis/conf/redis.conf:/etc/redis/redis.conf \
-itd redis redis-server /etc/redis/redis.conf \
--appendonly yes

```

# 运行
 python3 wxchatbot.py
 
 域名解析到你服务器,宝塔面板网站管理页面进行反向代理,确保域名直接能访问
 
 去公众号 "服务器配置" 进行配置,填入你的token提交匹配成功即可

