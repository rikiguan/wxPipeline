import time
from wxauto import WeChat
from zhipuai import ZhipuAI
from conf import *


client = ZhipuAI(api_key=apiKey)

# 获取微信窗口对象
wx = WeChat()
# 输出 > 初始化成功，获取到已登录窗口：xxxx
listen_list = [
    '孙悟空',
    '猪八戒'
]

# 定义处理函数，替换敏感词
def process_keyword1(content):
    # 在此处处理content，返回替换后的内容
    return content.replace('敏感词1', '替换词1')

def process_keyword2(content):
    # 在此处处理content，返回替换后的内容
    return content.replace('敏感词2', '替换词2')

def ai_process(content):
    response = client.chat.completions.create(
        model="glm-4-0520",  # 填写需要调用的模型编码
        messages=[
            {"role": "user", "content": "你是一名高情商的感情大师，你会把我发给女朋友的句子优化的更加活泼得体[要求：直接返回句子内容]句子内容是："+content}
        ],
    )
    res = response.choices[0].message.content.replace('"', '')
    print(res)
    return res

# 定义关键词触发的函数字典
keyword_functions = {
    '敏感词1': process_keyword1,
    '敏感词2': process_keyword2,
}

# 定义关键词过滤替换函数
def filter_keywords(content):
    keywords_simple = {
        '[动画表情]': '',
        '哈': '',
        '草': '哈哈哈'
    }
    # 逐个替换关键词
    for keyword, replacement in keywords_simple.items():
        content = content.replace(keyword, replacement)

    for keyword, func in keyword_functions.items():
        if keyword in content:
            content = func(content)

    return content

for i in listen_list:
    wx.AddListenChat(who=i, savepic=True)

# 持续监听消息，并且收到消息后回复“收到”
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who  # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)  # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            msgtype = msg.type  # 获取消息类型
            content = msg.content  # 获取消息内容，字符串类型的消息内容
            print(f'【{who}】：{content}')

            # 调用关键词过滤替换函数
            filtered_content = filter_keywords(content)

            if(filtered_content == ''):
                continue
            # 如果是好友发来的消息（即非系统消息等），则回复收到
            if msgtype == 'friend':
                filtered_content = ai_process(filtered_content)
                wx.SendMsg(who=listen_list[~listen_list.index(who)], msg=filtered_content)
    #time.sleep(wait)
