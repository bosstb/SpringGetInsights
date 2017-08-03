# coding: utf-8
#遗留问题：IP会变：54.193.59.55

import os
from datetime import datetime
from datetime import timedelta
import json
from flask import Flask,redirect
from flask import render_template
from flask_sockets import Sockets
import random
from views.todos import todos_view
from flask import request
import leancloud
import requests
import xml.dom.minidom
import datetime
import time
import base64
from flask import make_response
from flask import send_file, send_from_directory
# leancloud.init("fVBfU2NNnuRwhFLlrzIMy0ni-gzGzoHsz", "DXazg5nL3TfvtP3p3ad1zNVe")


app = Flask(__name__)
sockets = Sockets(app)
# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')
#微信公众号定义
appSecret = 'ba8cfd77977f3f9a57eccaa1b00c7903'
appId = 'wxe9b54103e44bd336'
lastTitle = ''


class NewsRecord(leancloud.Object):
    pass


class RealtimeScore(leancloud.Object):
    pass


@app.route('/', methods=["GET", "POST"])
def index():
    data = []
    limit = request.args.get("limit")
    pageId = request.args.get("pageid")
    type = request.args.get("type")
    if pageId == "" or pageId == None:
        return "请设置PageId参数"
    if type == "" or type == None:
        return "请设置PageId参数"
    token = "EAACEdEose0cBAByFmp2PYmuRPdA4jk24ed4k2dzLuzgBK0ii72SI9I9c83gFWOZCBvxAc8iZCtY3sQLBqP3oOhCpq4g9kwd0NU9gfkez6hi1X1ktoTPE7yaAtaqFhn4TOUznuvxLDCu7J8MH16UcXRh0ZA0KFg3xKZCoXw6ZBKvUF7ZB50N9kKGPZAwiAMGVm0ZD"
    if type == "post":
        if limit == 0 or limit == None:
            return "请设置Limit参数"
        r = requests.get(
            "https://graph.facebook.com/v2.10/" + pageId + "/feed?access_token=" + token +"&limit=" + str(limit))
        content_json = json.loads(r.text)
        for item in content_json.get("data"):
            created_time = item.get("created_time")
            message = item.get("message")
            id = item.get("id")
            # r = requests.get("https://graph.facebook.com/v2.10/" + id + "/insights?metric=post_impressions,post_impressions_unique,post_impressions_paid,"
            #                                                                  "post_impressions_paid_unique,post_impressions_fan,post_impressions_fan_unique,post_impressions_fan_paid,"
            #                                                             "post_impressions_fan_paid_unique,post_impressions_organic,post_impressions_organic_unique,"
            #                                                             "post_impressions_viral,post_impressions_viral_unique,post_impressions_by_story_type,post_impressions_by_story_type_unique,"
            #                                                             "post_impressions_by_paid_non_paid,post_impressions_by_paid_non_paid_unique,"
            #                                                             "post_consumptions,	post_consumptions_unique,post_consumptions_by_type,post_consumptions_by_type_unique,post_engaged_users,post_negative_feedback,post_negative_feedback_unique,post_negative_feedback_by_type,post_negative_feedback_by_type_unique,post_engaged_fan,post_fan_reach,page_story_adds,"
            #                                                             "page_story_adds_by_age_gender_unique,page_story_adds_by_city_unique,page_story_adds_by_country_unique,&access_token=" + token + "&limit=10")
            r = requests.get(
                "https://graph.facebook.com/v2.10/" + id + "/insights?metric=post_impressions_unique,post_video_views_organic,post_video_views_paid,share,like,comment,other clicks,link clicks,video play,photo view,hide_all_clicks,hide_clicks&access_token=" + token + "&limit=10")
            print r.text
            post_json = json.loads(r.text)
            paras = []
            paras.append(id)
            paras.append(message)
            for para in post_json.get("data"):
                paras.append(str(para.get("values")[0].get("value")))
            data.append(paras)
        import xlwt
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i in range(len(data)):
            for j in range(len(data[i])):
                booksheet.write(i, j, data[i][j])
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                booksheet.write(i, j, col)
        workbook.save('d:\grade.xls')
        response = make_response(send_file("d:\grade.xls"))
        response.headers["Content-Disposition"] = "attachment; filename=data.xls;"
        return response
    elif type == "page":
        r = requests.get(
            "https://graph.facebook.com/v2.10/" + pageId + "/insights?metric=page_fan_adds_unique,page_fan_removes_unique,page_engaged_users,page_views_logged_in_total,page_posts_impressions_unique,page_video_views&access_token=" + token + "&limit=" + str(limit))
        content_json = json.loads(r.text)
        data = []
        for item in content_json.get("data"):
            i = item.get("values")
            values = []
            for value in i:
                values.append(value.get("end_time") + ',' + str(value.get("value")))
            data.append(values)
        import xlwt
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i in range(len(data)):
            for j in range(len(data[i])):
                booksheet.write(i, j, data[i][j])
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                booksheet.write(i, j, col)
        workbook.save('d:\grade.xls')
        response = make_response(send_file("d:\grade.xls"))
        response.headers["Content-Disposition"] = "attachment; filename=data.xls;"
        return response
    else:
        return "Unkown Type"


# def PushTest():
#     content_json = json.loads(
#         '[{"id":"5QyqDq1HmU_","title":"İçişleri Bakanı Soylu: Terör örgütünün şehir yapılanması tamamen çökertildi"},{"id":"5Qyr4qSnOLI","title":"Kılıçdaroğlu: Kutuplaşma kaygı verici"},{"id":"5Qyy2Xt1wrD","title":"Amazon CEO’su dünyayı kurtarma provası yaptı"},{"id":"5QywT2J1raV","title":"İFF’den SABAH ve atv’ye teşekkür"},{"id":"5QyrNeOXzlg","title":"Garnizon komutanına FETÖ gözaltısı"}]')
#     for item in content_json:
#         print item
#         sourceId = item.get('id')
#         title = item.get('title')
#         print sourceId+title


@app.route('/time')
def timea():
    return str(datetime.now())


@app.route('/wechatapi', methods=["GET", "POST"])
def wechat():
    #请求内容类型判断
    if request.method == 'GET':
        args = request.args
        signature = args.get('signature')
        timestamp = args.get('timestamp')
        nonce = args.get('nonce')
        echostr = args.get('echostr')
        if echostr != None:
            print echostr
            return echostr
        else:
            print 'None'
            return 'None'
    elif request.method =='POST':
        args = request.get_data()
        doc = xml.dom.minidom.parseString(args)
        doc = xml.dom.minidom.parseString(args)
        ToUserName = doc.getElementsByTagName("ToUserName")[0].firstChild.data
        FromUserName = doc.getElementsByTagName("FromUserName")[0].firstChild.data
        #print FromUserName
        CreateTime = doc.getElementsByTagName("CreateTime")[0].firstChild.data
        MsgType = doc.getElementsByTagName("MsgType")[0].firstChild.data
        msg = doc.getElementsByTagName("Content")[0].firstChild.data
        MsgId = doc.getElementsByTagName("MsgId")[0].firstChild.data
        if msg.find('RLU:') >= 0:
            Todo = leancloud.Object.extend('RealtimeScore')
            todo = Todo.create_without_data('58ef1b27827459005245ade6')
            # 这里修改 location 的值
            todo.set('rightOption', msg.split(',')[1])
            todo.set('leftOption', msg.split(',')[0].replace('RLU:', ''))
            todo.save()
            return '<xml><ToUserName>' + FromUserName + '</ToUserName>' + '<FromUserName>' + ToUserName + '</FromUserName>' + '<CreateTime>' + \
        str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0] + '</CreateTime>' + '<MsgType><![CDATA[text]]></MsgType>' + \
        '<Content><![CDATA[OKOK]]></Content></xml>'
        content_json = json.loads(getPushContent(msg))
        pushInfo = ''
        count = 0
        for item in content_json:
            count += 1
            sourceId = item.get('id')
            title = item.get('title').replace('"', '').replace('\n', '')
            content = item.get('content').replace('"', '').replace('\n', '')
            newsRecord = NewsRecord()
            newsRecord.set('Id', sourceId)
            newsRecord.set('title', title)
            newsRecord.set('content', content)
            newsRecord.save()
            if msg == 'Push':
                publishedTime = str(item.get('publishedTime')).replace('+0000', '').replace('T', ' ')
            else:
                publishedTime = item.get('publishedTime')

            if msg.find('topic') >= 0:
                pushInfo = pushInfo + '|||' + 'TITLE:' + title + '|||' + content + 'CONTENT:'
            else:
                pushInfo = pushInfo + '|||' + '<a href="https://compaign.newsgrapeapp.com/news/' + \
                           sourceId + '">' + title + '(' + publishedTime + ')</a>' + '|||' + \
                '<a href="http://haberpush.leanapp.cn/wechatapi/' + sourceId + '">Push</a>'
                if msg != 'Push' and count > 5:
                    break

        replyStr = '<xml><ToUserName>' + FromUserName + '</ToUserName>' + '<FromUserName>' + ToUserName + '</FromUserName>' + '<CreateTime>' + \
        str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0] + '</CreateTime>' + '<MsgType><![CDATA[text]]></MsgType>' + \
        '<Content><![CDATA[' + pushInfo + ']]></Content></xml>'
        print replyStr.encode('utf-8')
        return replyStr.encode('utf-8')


def getPushToken():
        r = requests.get(
            'https://api.newsgrapeapp.com/auth/token?udid=123456&platform=WEB&pcid=123')
        return r.text


def getPushContent(msg):
    # 取Token:
    BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的父目录绝对路径
    #print BASE_DIR
    file_path = os.path.join(BASE_DIR, 'static', 'token.txt')  # 获取C文件夹中的的Test_Data文件
    f = open(file_path, 'r')
    token = ''
    token = f.read()
    headers = {'Authorization': 'Bearer ' + token}
    f.close
    if msg == 'Push':
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/news', headers=headers)
    elif msg.find('topic,') >= 0:
        r = requests.post('https://api.newsgrapeapp.com/v1/topic/news?topicId=' + str(msg).split(',')[1], headers=headers)
    elif msg.find('user,') >= 0:
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/usergroupnews?id=' + str(msg).split(',')[1] + '&score=' + str(msg).split(',')[2],
                          headers=headers)
        print 'https://api.newsgrapeapp.com/v1/custompush/usergroupnews?id=' + str(msg).split(',')[1] + 'score=' + str(msg).split(',')[2]
    else:
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/search?title=' + msg, headers=headers)
    while r.text.find('"error":"Unauthorized"') >= 0:
        token = getPushToken()
        f = open(file_path, 'w')
        token = json.loads(token).get('accessToken')
        f.write(token)
        f.close()
        headers = {'Authorization': 'Bearer ' + token}
        r = requests.get('https://api.newsgrapeapp.com/v1/custompush/news', headers=headers)

    return r.text


    #获取接入Token
def getAccessToken():
    r = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appId + 'secret=' + appSecret)
    return r.text


@app.route('/wechatapi/<sourceId>', methods=['POST', 'GET'])
def push(sourceId):
    query = leancloud.Query(NewsRecord)
    query.equal_to('Id', sourceId)
    query_list = query.find()
    title = query_list[0].get('title')
    content = query_list[0].get('content')
    global lastTitle
    if request.method == 'GET' and lastTitle != title:
        mkdir_str = '{"platform":"all","audience":"all","notification":{"alert":{"title":"' + title + '","body":"' + title + '"},"android":{},"ios":{"extras":{ \
                "news_id":"' + sourceId + '"}}}}'
        mkdir_url = "https://api.jpush.cn/v3/push"
        user = base64.encodestring("789dd28284380ec8a5137432:35ba7cba0791d95ad4586120").replace('\n', '')
        headder = {"Content-Type": "application/json", "Content-Length": str(len(mkdir_str)), "Authorization": 'Basic ' + user}
        r = requests.post(mkdir_url, data=mkdir_str.encode('utf-8'), headers=headder)
    lastTitle = title
    return r.text






@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


if __name__ == '__main__':
    app.run('0.0.0.0')

