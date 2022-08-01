#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :groupgrease.py
@说明    :
@时间    :2022/05/23 22:27:00
@作者    :Akira_TL
@版本    :1.0
'''


import json,platform,sys
import os

from nonebot import on_command, on_notice
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    MessageSegment, 
    GROUP_ADMIN, 
    GROUP_OWNER, 
    NoticeEvent,
    Message,
    Event, 
    Bot, )
from nonebot.permission import SUPERUSER
from ..tools.tools import debug,path_create
from nonebot.log import logger
pathdb = 'src/plugins/plugins/db'#数据文件的存储位置
file = pathdb + '/GroupInOrDecreaseNotice.json'

def debug(text):
    '''
    @说明:
        对官方debug方法的扩写,将文件地址写入debug消息方便查看日志
    @返回:
        none
    '''
    
    logger.debug('\033[94m' + __name__ + '\033[0m | ' + text)
    return


GroupMemNotice = on_notice(priority=5)
GroupNoticeswitch = on_command('进退群提醒',rule=to_me(),priority=5,block=True,permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
GroupNoticeQuery = on_command('查询进退群提醒',rule=to_me(),priority=5,block=True,permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)

@GroupMemNotice.handle() # 进退群提醒处理
async def GroupMemNotice_(bot:Bot,event:NoticeEvent):
    try:
        group_id = str(event.get_session_id()).split('_')[1]
    except IndexError:
        debug('非群聊消息')
        await GroupMemNotice.finish()
    user_id = event.get_user_id()
    user_info = await bot.get_stranger_info(user_id=int(user_id))
    head_url = f"https://q.qlogo.cn/g?b=qq&nk={user_id}&s=640"#QQ头像地址
    debug(user_info)
    try:
        await create_document()
        f = open(file,'r')
        debug(group_id)
        switch = str(json.load(f)[group_id])
        debug(switch)

        if switch == '1':
            description = json.loads(event.get_event_description().replace("'",'"'))
            if description['notice_type'] == 'group_increase':
                await GroupMemNotice.finish(
                    MessageSegment.at(user_id=user_id)+Message(f"欢迎新成员{user_info['nickname']}的加入!") + \
                    MessageSegment.image(head_url) + Message('既然来了就不要走了哦੭ ᐕ)੭*⁾⁾')
                )
            elif description['notice_type'] == 'group_decrease':
                if description['sub_type'] == 'leave':
                    await GroupMemNotice.finish(
                        MessageSegment.image(head_url) + Message(f"{user_info['nickname']}咪咪的离开了我们...")
                    )
                elif description['sub_type'] == 'kick':
                    op_user_id = description['operator_id']
                    await GroupMemNotice.finish(MessageSegment.image(head_url) +
                                            "发现超级可爱的 " + MessageSegment.at(op_user_id) + f"({op_user_id})"
                                            f" 面无表情地把 {user_info['nickname']}({user_id}) 踹了出去，当时害怕极了喵。。")
    except:
        pass

@GroupNoticeswitch.handle()#进退群提醒开关
async def GroupNoticeswitch_(event:Event):
    group_id = str(event.get_session_id()).split('_')[1]
    debug(group_id)
    try:
        with open(file,'r') as f:
            content = json.load(f)
    except FileNotFoundError:
        os.makedirs(pathdb)
        f = open(file,'w')
        content = {}
        f.write('{}')
    f.close()

    try:
        switch = content[group_id]
    except KeyError:
        switch = '0'
    
    if switch == '1':
        switch = '0'
    else:
        switch = '1'

    data = {group_id:switch}
    content.update(data)

    with open(file,'w') as f_new:
        json.dump(content,f_new)

    if switch == '1':
        await GroupNoticeswitch.finish('进退群提醒已开启')
    elif switch == '0':
        await GroupNoticeswitch.finish('进退群提醒已关闭')
    else:
        await GroupNoticeswitch.finish('进退群提醒错误,请检查日志!')


@GroupNoticeQuery.handle()#查询是否开启进退群提醒
async def GroupNoticeQuery_(event:Event):
    group_id = str(event.get_session_id()).split('_')[1]
    try:
        await create_document()
        f = open(file,'r')
        debug(group_id)
        switch = str(json.load(f)[group_id])
        debug(switch)
        if switch == '1':
            await GroupNoticeQuery.finish('已开启进退群提醒!')
        else:
            await GroupNoticeQuery.finish('未开启进退群提醒!')
    except KeyError:
        await GroupNoticeQuery.finish('未开启进退群提醒!')

async def create_document():#检查有没有数据库,没有就创建,有就pass
    try:
        import os
        os.mkdir(pathdb)
        debug('reate floder cuccesful')
    except FileExistsError:
        pass
    try:
        f = open(pathdb+'/GroupInOrDecreaseNotice.json','r')
    except FileNotFoundError:
        f = open(pathdb+'/GroupInOrDecreaseNotice.json','w')
        f.close()
        debug('create documen cuccesful')
    debug('create_document() handed')


