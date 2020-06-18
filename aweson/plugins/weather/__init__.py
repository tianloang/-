from nonebot import on_command, CommandSession,typing
from nonebot import on_natural_language, NLPSession
from .data_source import get_weather_of_city
import json
import nonebot
import requests
from urllib import request
from urllib import parse
import urllib.request
from http import cookiejar
import re

bot = nonebot.get_bot()


@on_command(' ')
async def weather(session: CommandSession):
    city = session.get('￥')
    weather_report = await get_weather_of_city(city)
    await session.send(weather_report)


@bot.on_message('group')
async def handle_group_message(ctx: typing):
    print(ctx['message'])
    #
    # or ctx['group_id'] == 713985759
    if ctx['group_id'] == '' or ctx['group_id'] == '' or ctx['group_id'] == '' :
        flag = False
        if ctx['group_id'] == 713985759:
            flag = True
        data = ctx['message']
        data1 = str("111") + str(data) + str("111")
        tkl = ''
        countent = ''
        countent1 = ''
        countent2 = ''
        print(re.findall(r'\(+([0-9a-zA-Z])+\)',data1).__len__() > 0)
        print(str(data1).find('$'))
        if '$' in data1:
            countent = '$'
            countent1 = '$'
            countent2 = '$'
            print('$')
        elif '￥' in data1:
            countent = '￥'
            countent1 = '￥'
            countent2 = '￥'
            print('￥')
        elif 'https://u.jd.com/' in data1:
            newtext = getJd(str(data))
            print(newtext)
            if flag:
                msg1 = str(newtext).split('微博')
                await bot.send_group_msg(group_id=707433430, message=msg1[0].strip())
            else:
                await bot.send_group_msg(group_id=707433430, message=newtext)
            return
        elif re.findall(r'\(+([0-9a-zA-Z])+\)',data1).__len__() > 0:
            countent = '000'
            countent1 = '('
            countent2 = '）'
        else:
            if flag:
                msg1 = str(data).split('微博')
                await bot.send_group_msg(group_id=707433430, message=msg1[0].strip())
            return

        if countent != '000':
            tkl = data1.split(countent)
            tkl = str(countent1) + str(tkl[1]) + str(countent2)
        else:
            tkl = re.search(r'\(+([0-9a-zA-Z])+\)', data1).group()
            print(tkl)

        s = getUrl(tkl, str(tkl[0]))
        if s.find('解析失败') != -1:
            msg1 = str(data).split('微博')
            await bot.send('[CQ:share,url={1},title={2},content={3},image={}]')
            await bot.send_group_msg(group_id=707433430, message=msg1[0].strip())
            print(ctx['message'])
        else:
            stripped_msg = str(data).replace(tkl, s, 1)
            print(stripped_msg)
            msg1 = str(stripped_msg).split('微博')
            await bot.send_group_msg(group_id=707433430, message=msg1[0].strip())
        getHelpInfo();


def getHelpInfo():
    # if sessionCtx['message_type']=='group':
        # info=f"[CQ:at,qq={sessionCtx['user_id']}]{split}{info}"
        strs = '[CQ:share,url={},title={'+str('去你妈的')+'},content={'+str('去你妈的')+'},image={'+str('https://img-blog.csdnimg.cn/20190828114954141.jpg?x-oss-process=image/resize,m_fixed,h_64,w_64')+'}]'
        bot.send_group_msg(group_id=713985759, message=strs,auto_escape=False)

        # bot.send('[CQ:share,url={1},title={2},content={3},image={}]')
        #  return info


def getJd(text) :
    urls = Find(text);
    newText = text
    for url in urls :
        newurl = jdGet(url)
        newText = newText.replace(url,newurl)
    return newText



def jdGet(url):
    URL_ROOT = r'https://qwd.jd.com/cps/zl?content='
    url1 = str(url).replace(':', '%3A')
    url2 = str(url1).replace('/', '%2F')
    # https%3A%2F%2Fu.jd.com%2FdHysbB
    URL_ROOT = URL_ROOT + url2
    value = {
        'content': url2,
    }
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {
        'Cookie': 'app_id = 161;login_mode=2;jxjpin=jd_5c3cfa6b86648;tgt=AAJd1n6RAEAoN3Gs12CqHKRFdJuGHI0RH_473_uj0BVyI54FRmJmu6-n5xEodfQq63TVn0-4ClEP7kN-2ln_wFWTO510EElU;'
    }

    data1 = urllib.parse.urlencode(value).encode('UTF8')
    session = requests.session()
    requ = session.get(URL_ROOT,  headers=headers)
    res = requ.text
    rest = json.loads(res)
    if rest['errCode'] == "0":
        return rest['skuInfos'][0]["unionUrl"]
    else:
        return url;


def Find(string):
        # findall() 查找匹配正则表达式的字符串

        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        return url
#



def getUrl(key,text):
    top1 = r'https://www.taokouling.com/';
    cj = cookiejar.CookieJar()
    urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)).open(top1)
    for item in cj:
        print(item)
    URL_ROOT = r'https://www.taokouling.com/user/login/'
    value = {
        'username': '437709122',
        'password': '********',
        'remember': 'true'
    }
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }

    data = urllib.parse.urlencode(value).encode('UTF8')
    req = urllib.request.Request(URL_ROOT, data, headers)

    urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)).open(req)
    for item in cj:
        print(item)

    url = r'https://www.taokouling.com/index/tbtkltoitemid/';

    head = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.taokouling.com/index/tbtkltoitemid'
    }
    val1 = {
        'tkl': key,
        'zdgy': 'false',
        'pid': '',
        'tkltitle': '',
        'tklpic': '',
        'tkluserid': '',
        'tgdl': 'false'
    }
    data1 = urllib.parse.urlencode(val1).encode('UTF8')
    session = requests.session()
    requ = session.post(url, data=data1, headers=head, cookies=cj)
    res = requ.text
    rest = json.loads(res)
    if rest['msg'].find('解析失败') != -1:
        print(rest['msg'])
        return rest['msg']

    val2 = {
        'apikey': 'PkvgyNCTqJ',
        'itemid': rest['data']['itemid'],
        'siteid': '1081300027',
        'uid': '2031542714',
        'adzoneid': '109743800215'
    }
    data1 = urllib.parse.urlencode(val2).encode(encoding='UTF8')
    response = urllib.request.urlopen(' https://api.taokouling.com/tkl/TbkPrivilegeGet', data1).read()
    rest = json.loads(response)
    myurl = rest['result']['data']['coupon_click_url']
    print(myurl)
    textArr = [];
    if (text.count("\r\n") > 1):
        textArr = text.split('\r\n')[1]
    else:
        textArr = [text]

    head = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.taokouling.com/index/tbtkltoitemid'
    }
    val1 = {
        'tkl': key,
        'zdgy': 'false',
        'pid': '',
        'tkltitle': '',
        'tklpic': '',
        'tkluserid': '',
        'tgdl': 'false'
    }
    data1 = urllib.parse.urlencode(val1).encode('UTF8')
    session = requests.session()
    requ = session.post('https://www.taokouling.com/index/tktaokouling/', data=data1, headers=head, cookies=cj)
    res = requ.text
    rest = json.loads(res)



    val3 = {
        'tklpic': ' https://gw.alicdn.com/tfs/TB1c.wHdh6I8KJjy0FgXXXXzVXa-580-327.png',
        'tkltype': 0,
        'url': myurl,
        'tkltitle': '优惠大酬宾',
        'tgdl':''
    }
    data3 = urllib.parse.urlencode(val3).encode(encoding='UTF8')
    session = requests.session()
    requ = session.post('https://www.taokouling.com/index/tktaokouling/', data=data3, headers=head, cookies=cj)
    res = requ.text
    list_json = json.loads(res)
    docid = ''
    for item in list_json['data']:
        docid = item['tkl']
    return docid
