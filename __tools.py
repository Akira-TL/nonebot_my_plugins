import os, json, requests
from nonebot import logger

UA = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50'}

def downloud_img_return_path(url:str) -> str:
    try:
        img_path = 'src/plugins/plugins/pictures'
        logger.debug(url)
        img = requests.get(url,headers={"Referer": "https://www.pixiv.net"}).content
        img_name = url.split('/')[-1]
        try:
            os.makedirs(img_path)
            logger.debug('文件夹已新建')
        except:
            logger.debug('文件夹已存在')
            pass

        with open(img_path + '/' + img_name,'wb') as f:
            f.write(img)
            f.close()
        logger.debug('file:///' + img_path + '/' + img_name)
        return 'file:///' + img_path + '/' + img_name
    except:
        logger.debug('file:///' + img_path + '/' + img_name)
        return 'file:///src/plugins/plugins/pictures/404.png'