#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :qq_auto.py
@说明    :
@时间    :2022/05/23 22:15:48
@作者    :Akira_TL
@版本    :1.0
'''


import json
import nonebot
from nonebot import on_notice, on_request
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (
    Event,
    Bot,
)

def debug(text):
    '''
    @说明:
        对官方debug方法的扩写,将文件地址写入debug消息方便查看日志
    @返回:
        none
    '''
    
    logger.debug('\033[94m' + __name__ + '\033[0m | ' + text)
    return

auto_friend = on_request(priority=5,block=False)
@auto_friend.handle()
async def auto_friend_(event:Event,bot:Bot):
    '''
    @说明:
        好友请求同意
    '''
    content = json.loads(event.get_event_description().replace("'",'"'))
    try:
        if content['request_type'] == 'friend':
            await bot.call_api('set_friend_add_request',
                                flag = content['flag'],)
    except:
        pass

# [request.friend]: {'time': 1653314361, 'self_id': 3594565331, 'post_type': 'request', 'request_type': 'friend', 'user_id': 1937369050, 'comment': '我是bot2号机', 'flag': '1653314361000000'}
#  [notice.friend_add]: {'time': 1653314774, 'self_id': 3594565331, 'post_type': 'notice', 'notice_type': 'friend_add', 'user_id': 1937369050}