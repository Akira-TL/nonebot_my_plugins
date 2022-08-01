#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :shadule.py
@说明    :
@时间    :2022/05/23 16:16:57
@作者    :Akira_TL
@版本    :1.0
'''


from os import makedirs
import re, nonebot, time, sqlite3, sys
from matplotlib.pyplot import tick_params
from nonebot import get_bot, on_command, on_message, on_regex, require
from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.params import CommandArg, Arg, ArgStr, RawCommand
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupMessageEvent,
    Message,
)
from numpy import true_divide

scheduler = require('nonebot_plugin_apscheduler').scheduler

def debug(text) -> None:
    '''
    @说明:
        对官方debug方法的扩写,将文件地址写入debug消息方便查看日志
    @返回:
        none
    '''
    
    logger.debug('\033[94m' + __name__[12:] + '\033[0m | ' + str(text))
    return

# month = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'十一':11,'十二':12}
days = [31,28,31,30,31,30,31,31,30,31,30,31]
weekdays = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'天':7,'日':7}
weekdays_back = ['一','二','三','四','五','六','日']
pro = 10

notice_cycle = on_regex(r'(今天|明天|后天|下周.|这周.|\d+月\d+日|每月\d+号|每周.|每天)(早上|上午|下午|晚上|\d+点\d+分|\d+点|\d+分钟后|)提醒我',priority=pro,rule=to_me())
@notice_cycle.handle()
async def notice_cycle_(event:Event):
    '''
    @说明:
        新建任务,任务规则为:"(今天|明天|后天|下周.|这周.|\d+月\d+日|每月\d+号|每周.|每天)(早上|上午|下午|晚上|\d+点\d+分|\d+点|\d+分钟后)提醒我"
    @返回:
        无
    '''
    
    msg = str(event.get_message())
    date = re.findall(r'今天|明天|后天|下周.|这周.|\d+月\d+日|每月\d+号|每周.|每天',msg)[0]
    timef = re.findall(r'早上|上午|下午|晚上|\d+点\d+分|\d+点|\d+分钟后',msg)
    debug(timef)
    debug(date)
    notice = msg.split(r'提醒我')[-1]
    tm = time.localtime()
    user_id = event.get_user_id()
    year = tm.tm_year
# 定义初始变量
    if '今天' in date:
        day = tm.tm_mday
        mon = tm.tm_mon
        mod = 0
    elif date == '明天':
        day = tm.tm_mday + 1
        mon = tm.tm_mon
        mod = 0
    elif date == '后天':
        day = tm.tm_mday + 2
        mon = tm.tm_mon
        mod = 0
    elif '这周' in date:
        day = tm.tm_mday + weekdays[re.findall('这周(.)',date)[0]] - tm.tm_wday - 1
        mon = tm.tm_mon
        mod = 0
    elif '下周' in date:
        day = tm.tm_mday + 7 + weekdays[re.findall('下周(.)',date)[0]] - tm.tm_wday - 1
        mon = tm.tm_mon
        mod = 0
    elif '每月' in date:
        day = re.findall('\d+',date)[0]
        mon = tm.tm_mon
        mod = 1
        if day < tm.tm_mday:
            mon += 1
    elif '每周' in date:
        day_of_week = weekdays[re.findall('每周(.)',date)[0]] - 1
        if day_of_week <= tm.tm_wday:
            next_ = 7 - (tm.tm_wday - day_of_week)
        else:
            next_ = day_of_week - tm.tm_wday
        day = tm.tm_mday + next_
        mon = tm.tm_mon
        mod = 2
    elif '每天' in date:
        day = tm.tm_mday + 1
        mon = tm.tm_mon
        mod = 3
    elif re.findall('\d+',date):
        date = re.findall('\d+',date)
        debug(date)
        mon = int(date[0])
        day = int(date[1])
        mod = 0
    else:
        mon = tm.tm_mon
        day = tm.tm_mday
        mod = 0
# 将周期提醒的内容分开并打好模式(mod)标记
    if len(timef) == 0:
        hour = 8
        minute = 0
    elif timef[0] == '早上' or timef[0] == '上午':
        hour = 8
        minute = 0
    elif timef[0] == '下午':
        hour = 14
        minute = 0
    elif timef[0] == '晚上':
        hour = 19
        minute = 0
    elif '点' in timef[0]:
        timef = re.findall('\d+',timef[0])
        debug(timef)
        hour = int(timef[0])
        minute = int(timef[-1])
        if len(timef) == 1:
            minute = 0
    else:
        timef = re.findall('\d+',timef[0])
        minute = tm.tm_min + int(timef)
# 定义时间
    while minute  >= 60 or hour >= 24 or day >= days[mon-1] or mon >= 13:
        if minute > 59:
            minute -= 60
            hour += 1
        if hour > 23:
            hour = hour - 24
            day += 1
        if day > days[(mon-1)%12]:
            day -= days[(mon-1)%12]
            mon += 1
        if mon > 12:
            mon -= 12
            year += 1
# 修正时间日期

    time_send = time.mktime(time.strptime(f'{year}-{mon}-{day}-{hour}-{minute}','%Y-%m-%d-%H-%M'))
    logger.debug(f'设置日期为{year}-{mon}-{day}-{hour}-{minute}')
    try:
        f = open('src/plugins/plugins/db/NoticeTimeData.db','r')
        f.close()
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
    except FileNotFoundError:
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
        b.execute('''create table notice(time real,id text,notice text,mod int)''')
    b.execute(f'''insert into notice (time,id,notice,mod) values('{time_send}','{user_id}','{notice}','{mod}')''')
    b.close()
    a.commit()
    a.close()

@scheduler.scheduled_job("cron" , minute = '*/1')
async def found_every_minutes():
    '''
    @说明:
        每隔一分钟检查一次表格是否可以提醒
    @返回:
        无
    '''
    
    debug("已检查一次任务列表")
    bot = get_bot()
    try:
        f = open('src/plugins/plugins/db/NoticeTimeData.db','r')
        f.close()
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
    except FileNotFoundError:
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
        b.execute('''create table notice(time real,id text,notice text,mod int)''')
    # a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
    # b = a.cursor()
    b.execute('''select * from notice''')
    try:
        content = b.fetchmany()[0]
        while content:
            now = time.localtime(time.time())
            sd_time = time.localtime(float(content[0]))
            if  now.tm_year == sd_time.tm_year and now.tm_mon == sd_time.tm_mon and\
                now.tm_mday == sd_time.tm_mday and now.tm_hour == sd_time.tm_hour and\
                now.tm_min == sd_time.tm_min:
                if content[3] == 0:
                    await bot.call_api( api='send_private_msg',
                                        user_id=content[1],
                                        message=content[2])
                    sql = 'delete from notice where time = ?'
                    b.execute(sql,(f'{content[0]}',))
                elif content[3] == 1:
                    await bot.call_api( api='send_private_msg',
                                        user_id=content[1],
                                        message=content[2])
                    time_send = time.mktime(time.strptime(f'{content.tm_year}-{content.tm_mon + days[content.tm_mon - 1]}\
                        -{content.tm_mday}-{content.tm_hour}-{content.tm_min}','%Y-%m-%d-%H-%M'))
                    sql = 'update notice set time = ? where time == ?'
                    b.execute(sql,(f'{time_send}',f'{content[0]}'))
                elif content[3] == 2:
                    await bot.call_api( api='send_private_msg',
                                        user_id=content[1],
                                        message=content[2])
                    time_send = time.mktime(time.strptime(f'{content.tm_year}-{content.tm_mon}\
                        -{content.tm_mday + 7}-{content.tm_hour}-{content.tm_min}','%Y-%m-%d-%H-%M'))
                    sql = 'update notice set time = ? where time == ?'
                    b.execute(sql,(f'{time_send}',f'{content[0]}'))
                elif content[3] == 3:
                    await bot.call_api( api='send_private_msg',
                                        user_id=content[1],
                                        message=content[2])
                    time_send = time.mktime(time.strptime(f'{content.tm_year}-{content.tm_mon}\
                        -{content.tm_mday + 1}-{content.tm_hour}-{content.tm_min}','%Y-%m-%d-%H-%M'))
                    sql = 'update notice set time = ? where time == ?'
                    b.execute(sql,(f'{time_send}',f'{content[0]}'))
            content = b.fetchmany()[0]
    except IndexError:
        b.close()
        a.commit()
        a.close()

notice_delete_all = on_command('删除所有',priority=pro,block=True)
@notice_delete_all.handle()
async def notice_delete_(event:Event,msg = RawCommand()):
    user_id = event.get_user_id()
    if '每月' in msg:
        mod = 0
    elif '每周' in msg:
        mod = 1
    elif '每日' in msg:
        mod = 2
    else:
        mod = -1
    try:
        f = open('src/plugins/plugins/db/NoticeTimeData.db','r')
        f.close()
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
    except FileNotFoundError:
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
        b.execute('''create table notice(time real,id text,notice text,mod int)''')
    if mod != -1:
        b.execute(f'''select * from notice where id = "{user_id}" and mod = {mod} ''')
        content = b.fetchall()
        for notice in content:
            b.execute(f'''delete from notice where time = {notice[0]}''')
        debug(f'删除模式{mod}')
    elif mod == -1:
        b.execute(f'''select * from notice where id = "{user_id}" ''')
        content = b.fetchall()
        for notice in content:
            b.execute(f'''delete from notice where time = {notice[0]}''')
            debug('删除所有') 
    b.close()
    a.commit()
    a.close()
    await notice_delete_all.finish('OK')

notice_delete = on_command('删除',priority=pro,block=True)
@notice_delete.handle()
async def notice_delete_(event:Event,matcher:Matcher,arg = CommandArg()):
    if arg:
        try:
            arg = re.findall('\d{6}',str(arg))[0]
            matcher.set_arg('arg',arg)
        except:
            await matcher.send('id错误,请输入正确的id')
    else:
        user_id = event.get_user_id()
        try:
            f = open('src/plugins/plugins/db/NoticeTimeData.db','r')
            f.close()
            a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
            b = a.cursor()
        except FileNotFoundError:
            a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
            b = a.cursor()
            b.execute('''create table notice(time real,id text,notice text,mod int)''')
        b.execute('''select * from notice order by time''')
        b.execute(f'''select * from notice where id = '{user_id}' ''')
        content = b.fetchall()
        text = ''
        send_msg = ''
        l = 25
        if content:
            for notice in content:
                mod = notice[3]
                if mod == 0:
                    text = '-'*l + '\n消息:{}\nid:{}\n类型为:一次任务\n'.format(notice[2],str(notice[0])[4:10])
                elif mod == 1:
                    text = '-'*l + '\n消息:{}\nid:{}\n类型为:每月任务\n'.format(notice[2],str(notice[0])[4:10])
                elif mod == 2:
                    text = '-'*l + '\n消息:{}\nid:{}\n类型为:每周任务\n'.format(notice[2],str(notice[0])[4:10])
                elif mod == 3:
                    text = '-'*l + '\n消息:{}\nid:{}\n类型为:每日任务\n'.format(notice[2],str(notice[0])[4:10])
                send_msg += text
            await matcher.send(send_msg[l+1:-1])
        else:
            await matcher.send('没有任务,无需删除')
            matcher.set_arg('arg','-1')
        b.close()
        a.commit()
        a.close()



@notice_delete.got('arg','请发送id')
async def notice_delete_(matcher:Matcher,arg = ArgStr('arg')):
    if '-1' in arg:
        await matcher.finish()
    else:
        try:
            f = open('src/plugins/plugins/db/NoticeTimeData.db','r')
            f.close()
            a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
            b = a.cursor()
        except FileNotFoundError:
            a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
            b = a.cursor()
            b.execute('''create table notice(time real,id text,notice text,mod int)''')
        b.execute('''select * from notice''')
        content = b.fetchall()
        for notice in content:
            tm = str(notice[0])[4:10]
            debug(tm)
            if tm == arg:
                # sql = 'delete from notice where time = ?'
                b.execute(f'delete from notice where time = {notice[0]}')
                await matcher.send('删除完成')
        b.close()
        a.commit()
        a.close()


# 读取操作
notice_read = on_regex('(我|\d+|[CQ:at,qq=\d+]|)(的|.*)(一次性|每月|每周|每日|每天|)任务列表',priority = pro)
@notice_read.handle()
async def notice_read_(event:Event):
    '''
    @说明:
        查询任务列表,规则为:"(我|\d+|[CQ:at,qq=\d+]|)(的|)(一次性|每月|每周|每日|每天|)任务列表"
    @返回:
        无
    '''
    
    msg = str(event.get_message())
    find_user = re.findall('(我|\d+)',msg)
    find_date = re.findall('(一次性|每月|每周|每日|每天)',msg)
    try:
        if find_user[0] == '我':
            find_user = event.get_user_id()
        else:
            find_user = find_user[0]
    except:
        find_user = event.get_user_id()
    try:
        if find_date[0] == '一次性':
            find_date = 0
        elif find_date[0] == '每月':
            find_date = 1
        elif find_date[0] == '每周':
            find_date = 2
        elif find_date[0] == '每日' or find_date[0] == '每天':
            find_date = 3
    except:
        find_date = -1
# 语句分段转义
    try:
        f = open('src/plugins/plugins/db/NoticeTimeData.db','r')
        f.close()
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
    except FileNotFoundError:
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
        b.execute('''create table notice(time real,id text,notice text,mod int)''')
    b.execute('''select * from notice order by id''')
    b.execute(f'''select * from notice where id={find_user} ''')
    content = b.fetchall()
    send_msg = ''
    text = ''
    l = 25
# 打开数据库并初始化
    for notice in content:
        time_ = time.localtime(notice[0])
        mod = notice[3]
        rule = mod == find_date or find_date == -1
        if mod == 0 and rule:
            text = '-'*l + '\n将于{}月{}日 {:0>2d}:{:0>2d}\n发送消息:{}\n模式为:一次提醒任务\n'.format(time_.tm_mon,time_.tm_mday,time_.tm_hour,time_.tm_min,notice[2])
        elif mod == 1 and rule:
            text = '-'*l + '\n将于每月{}日 {:0>2d}:{:0>2d}\n发送消息:{}\n模式为:每月提醒任务\n'.format(time_.tm_mday,time_.tm_hour,time_.tm_min,notice[2])
        elif mod == 2 and rule:
            text = '-'*l + '\n将于每周{} {:0>2d}:{:0>2d}\n发送消息:{}\n模式为:每周提醒任务\n'.format(weekdays_back[time_.tm_wday],time_.tm_hour,time_.tm_min,notice[2])
        elif mod == 3 and rule:
            text = '-'*l + '\n将于每天 {:0>2d}:{:0>2d}\n发送消息:{}\n模式为:每日提醒任务\n'.format(time_.tm_hour,time_.tm_min,notice[2])
        if find_date != -1:
            send_msg += text[:-11]
            '''
            @说明:
                因为指定了模式,因此不需要说明模式.
            '''
        else:
            send_msg += text
    if send_msg:
        await notice_read.finish(send_msg[l+1:-1])
    b.close()
    a.commit()
    a.close()
    await notice_read.finish('任务列表为空')

notice_check = on_command('检查所有任务',priority=pro)
@notice_check.handle()
async def notice_check_():
    try:
        f = open('src/plugins/plugins/db/NoticeTimeData.db','r')
        f.close()
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
    except FileNotFoundError:
        a = sqlite3.connect('src/plugins/plugins/db/NoticeTimeData.db')
        b = a.cursor()
        b.execute('''create table notice(time real,id text,notice text,mod int)''')
    b.execute('''select * from notice''')
    content = b.fetchall()
    for notice in content:
        tm = notice[0]
        if tm < time.time() :
            await notice_check.send(f'将删除任务{notice[3]}\nid:{notice[2]}\nmod:{notice[3]}')
            b.execute(f'''delete from notice where time = {tm} ''')
    b.close()
    a.commit()
    a.close()
    await notice_check.finish('删除完成')