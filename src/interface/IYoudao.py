# coding:utf-8

import httplib2
import json

ghost = 'http://fanyi.youdao.com/openapi.do'
gkey = '2002774412'
gkeyfrom = 'niubility-word'
gversion = '1.1'

OK = 0
TEXT_TOO_LOG = 20
CAN_NOT_TRANSLATE = 30
NOT_SUPPORT_LANG = 40
INVALID_KEY = 50
NO_RESULT = 60


def translate(question, type='json'):
    global ghost
    myUrl = ghost
    myUrl += '?keyfrom=' + gkeyfrom \
             + '&key=' + gkey \
             + '&type=data' \
             + '&doctype=' + type \
             + '&version=' + gversion \
             + '&q=' + question
    try:
        httpClient = httplib2.Http()
        response, content = httpClient.request(myUrl)
        print content
        json_data = json.loads(content)
        if json_data['errorCode'] == OK:
            result = _parseJson(json_data)
            return result
        else:
            return json_data['errorCode']

    except Exception, e:
        print e


def _parseJson(json_data):
    query = json_data['query']
    translation = json_data['translation']
    phones = {}
    phones['phonetic'] = json_data['phonetic']
    phones['uk'] = json_data['uk-phonetic']
    phones['us'] = json_data['us-phonetic']

    explains = json_data['explains']  # 列表
    web = {}
    for item in json_data['web']:
        key = item['key']
        value = item['value']
        web[key] = value

    return DictResult(query, translation, phones, explains, web)


class DictResult():
    def __init__(self, query, translation, phones, explains, web=None):
        self.query = query
        self.translation = translation
        self.phones = phones
        self.explains = explains
        self.web = web


if __name__ == '__main__':
    translate(u'invalid')
