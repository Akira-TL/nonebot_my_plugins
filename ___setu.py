import random
import time
import asyncio, os, requests, json

from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.plugin import export, on_keyword
from nonebot import logger

cd_time = 10
last_send = time.time()
path = "src/plugins/plugins"
UA = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50'}


export = export()
export.name = 'setu插件'
export.usage = '''变态！才不给你看呢！！！'''

urls_2 = [
    'https://api.mtyqx.cn/api/random.php',
    'https://api.mtyqx.cn/tapi/random.php',
    'https://www.dmoe.cc/random.php',
    'https://api.btstu.cn/sjbz/api.php?lx=dongman',
    'https://iw233.cn/API/Random.php'
]

urls_3 = [
    'https://api.iyk0.com/cos',
    'https://api.btstu.cn/sjbz/api.php?lx=meizi',
    'https://api.iyk0.com/mtyh/?return=json'
]

setu = on_keyword({'setu','涩图','瑟图','色图','sese','涩涩','色色','瑟瑟'},priority=50,block=True)
@setu.handle()
async def xians_r(bot: Bot, event: Event):
    global last_send
    msg = event.get_plaintext()
    if last_send + cd_time > time.time():
        wait_msg = [
            '已经没了啦，真的没了啦~',
            '喂？警察叔叔，这里有一群变态......',
            '你说什么？风太大我看不清~',
            '身体是革命的本钱哦~',
            '再，再发就要被封号啦！',
            '我已经……一滴都没了……',
            '变！变态！',
            '妈妈快看，那里有个变态！',
            '富强、民主、文明、和谐',
            '自由、平等、公正、法治',
            '爱国、敬业、诚信、友善'
        ]
        await setu.finish(Message(wait_msg[random.randint(0,len(wait_msg)-1)]))
    if ('2'  in msg) or ('二' in msg):
        url = urls_2[random.randint(0,len(urls_2)-1)]
    elif ('3' in msg) or ('三' in msg):
        url = urls_3[random.randint(0,len(urls_3)-1)]
    elif 'debug' in msg:
        urls = urls_2 + urls_3
        url = urls[random.randint(0,len(urls)-1)]
        logger.debug(url)
        # await setu.send(url)
    else:
        urls = urls_2 # + urls_3
        url = urls[random.randint(0,len(urls)-1)]
    logger.debug(url)
    if url == 'https://api.iyk0.com/mtyh/?return=json':
        msg_id = await mtyh(url)
    else:
        msg_id = (await bot.send(event = event,message = Message(f"[CQ:image,file={url},cache=0,id=40000]")))['message_id']
    last_send = time.time()
    await asyncio.sleep(60)
    await setu.send('看完了吗，再等你30秒我就撤回了哦~')
    await asyncio.sleep(30)
    await bot.call_api('delete_msg',**{
        'message_id':msg_id
    })
    await setu.finish()

async def mtyh(url):
    html = requests.get(url)
    img_url = json.loads(html.content)['imgurl']
    logger.debug('img_url:' + img_url)
    img = requests.get(img_url,headers=UA)
    img_name = img_url.split('/')[-1]
    logger.debug(img_name)
    meitu_path = path + '/pictures/meitu'
    try:
        os.makedirs(meitu_path)
        logger.debug('文件夹已新建')
    except:
        logger.debug('文件夹已存在')
        pass

    with open(meitu_path + '/' + img_name,'wb') as f:
        f.write(img.content)
        f.close()
        logger.debug('img downlouded!')
        logger.debug(__file__.split('src')[0].replace('\\','/'))
    
    msg_id = (await setu.send(MessageSegment.image(file='file:///' + __file__.split('src')[0].replace('\\','/') + meitu_path + '/' + img_name)))['message_id']
    return msg_id
        # 这里记得加file:///
        # 这里记得加file:///
        # 这里记得加file:///
        # 重要的事情说三遍！！！