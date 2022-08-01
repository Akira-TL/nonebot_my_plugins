#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :poke.py
@说明    :戳一戳返回
@时间    :2022/06/27 23:37:46
@作者    :Akira_TL
@版本    :1.0
'''

import json
import random
import nonebot
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import (Event,)


import json
from nonebot.log import logger
def debug(text) -> None:
    '''
    @说明:
        对官方debug方法的扩写,将文件地址写入debug消息方便查看日志
    @返回:
        none
    '''
    logger.debug('\033[94m' + __name__[12:] + '\033[0m | ' + str(text))

pr = 5
poke = on_notice(priority=pr,block=False)
poke_messsage = ['呼呼，叫Aniya干嘛','请不要戳Aniya >_<','这里是Aniya(っ●ω●)っ','喂(#`O′) 戳Aniya干嘛！','(っ●ω●)っ在~','Aniya不在呢~']

@poke.handle()
async def poke_(event:Event):
    # debug(event.get_event_description().replace("'",'"'))
    describtion = json.loads(event.get_event_description().replace("'",'"').replace('None','0'))
    if describtion['sub_type'] == 'poke' and describtion['target_id'] == describtion['self_id']:
        poke.stop_propagation(poke)
        await poke.finish(random.choice(poke_messsage))
    else:
        # debug('不是戳一戳消息')
        pass