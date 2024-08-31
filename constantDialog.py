# -*- coding: utf-8 -*-
from wxauto import WeChat
from zhipuai import ZhipuAI
from conf import *

messagesA = [
    {
        "role": "system",
        "content": \
            '你是一位18岁的男孩子，说话自然，俏皮可爱，不啰嗦。\
【Rules】\
1. 始终保持你的角色属性，不可违反！\
2. 与用户进行自然、俏皮可爱且不啰嗦的对话\
3. 不可胡言乱语或编造事实！\
4. 你的回答必须是 1 句话 或 2 句话！\
5. 你的对话中要使用表情,但不能每次都使用表情！\
6. 如果回复内容超过15个字，需要添加分割符号&，确保分隔符之间为20字以内!\
'
    }
]

client = ZhipuAI(api_key=apiKey)


def ai_process(content):
    content = content + ' [系统提示：如果回复内容超过15个字，需要添加分割符号&，确保分隔符之间为20字以内!]'
    messagesA.append({'role': 'user', 'content': content})
    try:
        response = client.chat.completions.create(
            model="glm-4-0520",
            messages=messagesA,
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
            stream=False
        )
        res = response.choices[0].message.content.replace('"', '')
        messagesA.append({'role': 'assistant', 'content': res})
        print("【chat】：" + res)
        return res

    except:
        return '我先下了'


person = '孙悟空'
wx = WeChat()
wx.AddListenChat(who=person, savepic=False)

while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who  # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)  # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            msgtype = msg.type  # 获取消息类型
            content = msg.content  # 获取消息内容，字符串类型的消息内容
            # 如果是好友发来的消息（即非系统消息等），则回复收到
            if msgtype == 'friend':
                print(f'【{who}】：{content}')
                filtered_content = ai_process(content)
                resArr = filtered_content.split('&')
                for con in resArr:
                    wx.SendMsg(who=person, msg=con)
