import nonebot
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Event, Message
from nonebot.log import logger

msg_prior:Message = ''
msg_next:Message = ''
last_msg:Message = ''
_1 = on_message(block=False,priority=12)
@_1.handle()
async def _1_(event:Event):
    global msg_next,msg_prior,last_msg
    msg_prior = msg_next
    msg_next = event.get_message()
    if(msg_next == msg_prior):
        logger.debug(f"前一个消息为:{msg_prior}\n{'#'*29}后一个消息为:{msg_next}\n{'#'*29}last_msg:{last_msg}")
        if(last_msg != msg_next):
            _1.stop_propagation(_1)
            last_msg = msg_next
            await _1.finish(Message(msg_next))