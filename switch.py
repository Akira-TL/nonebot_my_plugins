import re
import nonebot
from nonebot import on_command
from nonebot.rule import regex
from nonebot.adapters.onebot.v11 import Event

import os,json
from nonebot.log import logger
def debug(text) -> None:
    '''
    @说明:
        对官方debug方法的扩写,将文件地址写入debug消息方便查看日志
    @返回:
        none
    '''
    logger.debug('\033[94m' + __name__[12:] + '\033[0m | ' + str(text))

pro = 5
switch = on_command('debug',rule=regex('(开启|关闭)(.*)'),priority=pro,block=True)
@switch.handle()
async def switch_(event:Event):
    msg = str(event.get_message())
    debug(msg)
    plugin_name = re.findall('debug开启(.*)',msg)[0]
    if not plugin_name:
        plugin_name = re.findall('debug关闭(.*)',msg)[0]
    if '开启' in msg:
        mod = 1
    elif '关闭' in msg:
        mod = 0
    os.makedirs('src/plugins/plugins/db',exist_ok=True)
    try:
        f = open('src/plugins/plugins/db/debugconfig.json','r+')
        f.close()
    except:
        with open('src/plugins/plugins/db/debugconfig.json','w') as f:
            f.write('{}')
        debug('进入了except')
    with open('src/plugins/plugins/db/debugconfig.json','r') as f:
        content = json.load(f)
        data = {plugin_name:mod}
        content.update(data)
    with open('src/plugins/plugins/db/debugconfig.json','w') as f:
        json.dump(content,f)
    
