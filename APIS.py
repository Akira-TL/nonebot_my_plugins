#星座运势
import requests,json,re,os,sys
from nonebot import on_command, on_keyword, on_message, on_regex
from nonebot.adapters.onebot.v11 import (
    Event,
    Message,
    MessageSegment,
)
from nonebot.matcher import Matcher
from nonebot.params import CommandArg,ArgPlainText
from nonebot import logger


pluginname = __name__

yunshi = on_command('运势',priority=11)
@yunshi.handle()
async def yunshi_(matcher:Matcher,arg:Message = CommandArg()):
    text = arg.extract_plain_text()
    logger.debug(text)
    if text:
        matcher.set_arg(key='xinzuo',message = arg)

@yunshi.got('xinzuo',prompt='你的星座是?')
async def yunshi_got(event:Event,constellation = ArgPlainText('xinzuo')):
    logger.debug(constellation)
    url = 'https://api.iyk0.com/xzys/?msg='
    urlget = url + constellation
    logger.debug(urlget)
    r = requests.get(urlget,headers=UA)
    result:str = json.loads(r.content)['data']
    result = result.replace('\n','')
    logger.debug('result:' + result)
    result_splits = result.split(':',2)
    result_splits = [result_splits[0],] + result_splits[1].split(';')
    result = result_splits[1]
    for i in range(2,8):
        result += '\n' + result_splits[i]
    logger.debug(result_splits)
    user_id = event.get_user_id()
    await yunshi.finish(message=MessageSegment.at(user_id)\
    + Message(constellation + "座今日的运势为\n")+ Message(result)
    )


path = "src/plugins/plugins"
UA = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50'}
url2 = 'https://api.iyk0.com/mtyh/?return=json'
meitu = on_regex('美图',priority=11)
@meitu.handle()
async def meitu_(event:Event):
    html = requests.get(url2)
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
    
    await meitu.send(MessageSegment.image(file='file:///' + __file__.split('src')[0].replace('\\','/') + meitu_path + '/' + img_name))



b404 = on_keyword(['404'],priority=11)
url3 = 'https://api.iyk0.com/bili_chart'
@b404.handle()
async def b404_(event:Event):
    html = requests.get(url3)
    html = json.loads(html.content)
    logger.debug(html)
    logger.debug(html['img'])
    logger.debug(html)
    await b404.send(MessageSegment.image(html['img']))

url = 'https://tenapi.cn/acg'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'}
acg = on_regex('acg',priority=11)
@acg.handle()
async def acg_(event:Event):
    data = {
        'return':True
    }
    html = requests.get(url,data=data).url
    logger.debug(html)
    await acg.send(Message(f"[CQ:image,file={html}]"))



# weather = on_regex('天气',priority=11)
# @weather.handle()
# async def weather_(event:Event):
#     weather_url = 'https://api.iyk0.com/7rtq'
#     message = str(event.get_message())
#     logger.debug(message)
#     # logger.debug(type(event.get_message()))
#     result = re.findall('(.{2})(.天)|(.{2})(天气)',message)
#     logger.debug(result)
#     city = result[0][2]
#     date = result[0][3]
#     logger.debug(city)
#     data = {
#         'city':city
#     }
#     weather_url = weather_url + '/?city=' + city
#     logger.debug(weather_url)
#     html = requests.get(weather_url)
#     html = json.loads(html.content)
#     if date == '天气':
#         # date = re.findall('(.){10}',html['update_time'])
#         date_num = 0
#     elif date == '明天':
#         date_num = 1
#     elif date == '后天':
#         date_num = 2
#     logger.debug(html)
#     logger.debug(html['img'][date_num])
#     # html = str(html)
#     # html = 'https://tva1.sinaimg.cn/large/dae614afly1fu89lrtp2hj212w0rgkjl.jpg'
#     logger.debug(html)
#     await weather.send(MessageSegment.image(html['img']))

# xxxxx = on_regex('404',priority=11)
# xxxxx_url = 'hurl'
# @xxxxx.handle()
# async def xxxxx_(event:Event):
#     html = requests.get(xxxxx_url)
#     html = json.loads(html.content)
#     logger.debug(html)
#     logger.debug(html['img'])
#     # html = str(html)
#     # html = 'https://tva1.sinaimg.cn/large/dae614afly1fu89lrtp2hj212w0rgkjl.jpg'
#     logger.debug(html)
#     await xxxxx.send(MessageSegment.image(html['img']))
