# coding:utf-8

import json

import httplib2

from src.model.DetailModel import DictResult

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
    # question = question.encode('utf-8')
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
            print 'result error code is:', json_data['errorCode']

        return None
    except Exception, e:
        print 'youdao exception', e


def _parseJson(json_data):
    query = json_data['query']
    translation = json_data['translation']

    phones = {}
    explains = []
    web = {}

    try:
        basic = json_data['basic']
        explains = basic['explains']  # 列表

        for item in json_data['web']:
            key = item['key']
            value = item['value']
            web[key] = value

        phones['phonetic'] = (basic['phonetic'], None)
        phones['uk'] = (basic['uk-phonetic'], None)
        phones['us'] = (basic['us-phonetic'], None)

    except Exception, e:
        print 'youdao json exception ', e

    return DictResult(query, translation, phones, explains, web)


if __name__ == '__main__':
    translate('invalid')
