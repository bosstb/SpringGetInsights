#coding=utf-8
from datetime import datetime
import random
import xml.dom.minidom
#生成100个随机0,1之间的浮点数序列l
l=0.1
l = random.randint(1, 100)
l=float(l)/100
print datetime.today()

def test():
    xx = """<xml>
         <ToUserName><![CDATA[toUser]]></ToUserName>
         <FromUserName><![CDATA[fromUser]]></FromUserName>
         <CreateTime>1348831860</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[this is a test]]></Content>
         <MsgId>1234567890123456</MsgId>
         </xml>"""
    doc = xml.dom.minidom.parseString(xx)
    ToUserName = doc.getElementsByTagName("ToUserName")[0].firstChild.data
    FromUserName = doc.getElementsByTagName("FromUserName")[0].firstChild.data
    CreateTime = doc.getElementsByTagName("CreateTime")[0].firstChild.data
    MsgType = doc.getElementsByTagName("MsgType")[0].firstChild.data
    Content = doc.getElementsByTagName("Content")[0].firstChild.data
    MsgId = doc.getElementsByTagName("MsgId")[0].firstChild.data

