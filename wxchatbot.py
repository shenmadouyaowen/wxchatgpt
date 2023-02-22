import werobot
from revChatGPT.V1 import Chatbot
import multiprocessing
import time
import redis
redis_url="127.0.0.1"
redis_pwd=""

def redis_conn():
    try:
        pool = redis.ConnectionPool(host=redis_url, port=6379, decode_responses=True, socket_connect_timeout=5, password=redis_pwd)
        r = redis.Redis(connection_pool=pool)
        r.get('conn_test')
        print('✅redis连接成功')
        return r
    except:
        print("⚠️redis连接异常")

def timeout_function(p, timeout,session):
    # 等待子进程完成或超时
    p.join(timeout)
    if p.is_alive():
        # 执行超时函数，并返回超时数据
        return 'success'
    else:
        # 子进程完成，返回子进程结果
        #session['content']=p.exitcode
        print(p.exitcode)
        print("进程超时")
        return "进程超时"


#此处填微信公众号token ,可以自定义
robot = werobot.WeRoBot(token='tokenhere')
#自定义本地程序端口
robot.config.update(
    HOST='0.0.0.0',
    PORT=8108
)
#填入access_token,在https://chat.openai.com/api/auth/session 获取
chatbot = Chatbot(config={
    "access_token":"填入获取到的<access_token>"
    })  
#revChatGPT 根据问题获取chatgpt答案
#text 问题
#把内容放入redis

def getchatpgt(message):
    prev_text = ""
    for data in chatbot.ask(
    message.content,
    ):
        msg = data["message"][len(prev_text) :]
        #print(message, end="", flush=True)
        prev_text = data["message"]
    #print("结果:"+prev_text)
    r.set(message.source,prev_text)
    return prev_text


@robot.text
def first(message, session):
    #检查之前是否提问过
    if "chatgpt" in message.content and  r.get(message.source) != "":
        content=r.get(message.source)
        r.set(message.source,"")
        #r.set('content',"")
        return content
    #发送chatgpt 直接返回
    elif "chatgpt" in message.content and r.get(message.source)=="":
        return "你好！我就是 ChatGPT，一个由 OpenAI 训练的大型语言模型。有什么我可以帮助你的吗？"

    p = multiprocessing.Process(target=getchatpgt,args=(message,))
    p.start()
    result = timeout_function(p, 4,session)  # 设置函数执行的时间限制为 4秒钟
    if 'success' in result:
        #r.set(message.source,message.source)
        return '我正在思考,请等待15s左右输入chatgpt 获取问题答案'
    
        #session['content']=result
    #print('timeout_function结果：', result)
    #print('结果：', session['content'])
    return r.get(message.source)
if __name__ == '__main__':
    r = redis_conn()
    robot.run()
