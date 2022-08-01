import json
import requests
from nonebot import on_message, matcher
from nonebot.adapters.onebot.v11 import Bot,Event
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from ..tools.tools import debug

pluginname = __name__
#chet start#
appid = '476a6e57e9e6da18b335ecce4cf02de2'
url = 'https://api.ownthink.com/bot'

async def get_(text):
    try:
        data = {
            "spoken": text,
            "appid": appid,
            "userid": "epkKfvDv"
        }
        r = requests.post(url, data=json.dumps(data))
        result = json.loads(r.content)
        message = result['data']['info']['text']
        if 'heuristic' in result['data']['info'] and result['data']['info']['heuristic']:
            for item in result['data']['info']['heuristic']:
                message += ',  ' + item
        debug(message,pluginname)
        return message
    except KeyError:
        return '获取失败'

# answer=on_message(priority=50,rule=to_me())
# @answer.handle()
async def chet_(bot:Bot,event:Event,matcher:matcher):
    if int(event.get_user_id())!=event.self_id:
        mysay = event.get_message()
        mysay = await get_(str(mysay))
        mysay = await replace_str(mysay)
        await bot.send(
            event=event,
            message=mysay
        )
    else:
        await matcher.skip()

async def replace_str(text:str):
    fix = {'小思':'Aniya','金融':''}
    for key in list(fix.keys()):
        #print(key)
        if text.find(key)>=0:
            text = text.replace(key,fix.get(key))
            #print(text)
    return text


