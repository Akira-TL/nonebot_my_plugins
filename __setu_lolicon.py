import random
import time
import asyncio, os, requests, json, re,httpx

from nonebot.adapters.onebot.v11 import (
    Bot, 
    Event, 
    GroupMessageEvent, 
    GROUP_ADMIN, 
    GROUP_OWNER
    )
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.plugin import export, on_keyword
from nonebot import logger, on_command
from nonebot.permission import SUPERUSER
from .__tools import downloud_img_return_path
from tenacity import retry, stop_after_attempt, wait_random
from io import BytesIO
from typing import List
from typing import Union

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

try:
    f = open('src\plugins\plugins\db\setu_r18.json','r')
except FileNotFoundError:
    f = open('src\plugins\plugins\db\setu_r18.json','w')
    json.dump('{}',f)
f.close()

setu = on_keyword(['涩涩'],priority=11)
@setu.handle()
async def setu_(event:GroupMessageEvent,bot:Bot):
    group_id = str(event.group_id)
    f = open('src\plugins\plugins\db\setu_r18.json','r')
    content = json.load(f)
    try:
        r18 = content[str(group_id)]
    except:
        r18 = '0'
    '''先获取一下r18开启信息'''

    if not re.findall('r18|R18',str(event.message)) and r18 == '1':
        r18 = '2'
    elif re.findall('r18|R18',str(event.message)) and r18 == '1':
        r18 = '1'
    else:
        r18 = '0'
    '''查看是否开启r18并决定发送值'''

    is_have_uid = re.findall('\d{5,8}',str(event.message))# 直接用值了
    if is_have_uid:
        uid = int(is_have_uid[0])
    else:
        uid = None
    '''uid的获取和指定'''

    if re.findall('tag',str(event.message)):
        tags = str(event.message).split('tag')[-1].split(' ')[1:]
    else:
        tags = None
    '''tag的获取和指定'''

    data = {
        'r18':r18,
        'uid':uid,
        'tag':tags,
        'proxy':''
    }
    url = 'https://api.lolicon.app/setu/v2'
    api_content = requests.post(url,json = data).content
    return_value = json.loads(api_content)
    pid = return_value['data'][0]['pid']
    uid = return_value['data'][0]['uid']
    title = return_value['data'][0]['title']
    author = return_value['data'][0]['author']
    urls = return_value['data'][0]['urls']['original']
    '''获取的数据'''

    # img = downloud_img_return_path(urls)
    # msg_id = (await setu.send(MessageSegment.at(event.get_user_id()) + 
    #                 f'pidL{pid}\nuid:{uid}\n标题：{title}\n作者：{author}\n'+ 
    #                 MessageSegment.image(img)+ 
    #                 '\n**如果没有图片就是被吞了~'
    # ))['message_id']
    download_setu(urls)
    await asyncio.sleep(30)
    # await bot.call_api('delete_msg',**{
    #     'message_id':msg_id
    # })
    await setu.finish()

r18_switch = on_keyword({'/开启r18,/关闭r18'},priority=11,permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)
@r18_switch.handle()
async def _(event:GroupMessageEvent):
    group_id = str(event.group_id)
    message = str(event.message)
    f = open('src\plugins\plugins\db\setu_r18.json','r')
    content = json.load(f)
    f.close()
    try:
        content[group_id]
    except KeyError:
        data = {group_id:'0'}
        content.update(data)

    if message == '/开启r18':
        content[group_id] = '1'
    elif message == '/关闭r18':
        content[group_id] = '0'

    f_new = open('src\plugins\plugins\db\setu_r18.json','w')
    json.dump(content,f_new)
    f_new.close()

def download_setu(url) -> Union[bytes, str]:
    debug(url)
    res = requests.get(url,headers={"Referer": "https://www.pixiv.net"}, verify=False)
    if res.status_code != 200:
        raise Exception(f"http状态码:{res.status_code}")
    return res.content

async def sendsetu_forBase64(setu:str):
    """发送setu,下载后用Base64发给OPQ"""
    async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=8, max_connections=10),
                                    # proxies=proxies,
                                    # transport=transport,
                                    headers={"Referer": "https://www.pixiv.net"},
                                    timeout=10) as client:
        @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2), retry_error_callback=lambda
                retry_state: "https://cdn.jsdelivr.net/gh/yuban10703/BlogImgdata/img/error.jpg")
        async def download_setu(url) -> Union[bytes, str]:
            res = await client.get(url)
            if res.status_code != 200:
                raise Exception(f"http状态码:{res.status_code}")
            return res.content

        resp = await download_setu(setu)
        if type(resp) != str:
            await setu.send(
                MessageSegment.image(BytesIO(resp)))
            
















# r18控制
# 数目的控制
# uid的指定
# 标签的指定
# # 规格的指定
# r18