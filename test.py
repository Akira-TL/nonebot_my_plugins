import re
import nonebot
from nonebot.params import CommandArg,RawCommand
from nonebot.adapters.onebot.v11 import Message,GroupMessageEvent,PrivateMessageEvent,Event
from nonebot import on_command,get_driver
from nonebot.log import logger
from nonebot.config import Config

def debug(text:str):
    '''
    @说明:
        对官方debug方法的扩写,将文件地址写入debug消息方便查看日志
    @返回:
        none
    '''
    logger.debug('\033[95m' + __name__[12:-6] + '\033[0m | ' + str(text))

a = on_command('test',priority=10)
@a.handle()
async def _(event:Event,args:Message = CommandArg(),raw = RawCommand()):
    # debug(event.get_session_id())
    # debug(re.findall('(\d+)',event.get_session_id()))
    debug(nonebot.get_bot().self_id)
    
    a.stop_propagation(a)
