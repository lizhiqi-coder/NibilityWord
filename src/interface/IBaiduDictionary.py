# coding:utf-8
import httplib
import md5
import random
import urllib

appid = '20170220000039535'
secretKey = 'pDfbYtw2Y4uBca8r1v7f'
myUrl = '/api/trans/vip/translate'

lang_auto = 'auto'
lang_Chinese = 'zh'
lang_English = 'en'
lang_French = 'fra'


def translate(question, fromLang, toLang):
    global myUrl
    global appid
    global secretKey
    httpClient = None
    q = question

    salt = random.randint(32423, 56468)

    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()

    myUrl += '?appid=' + appid \
             + '&q=' + urllib.quote(q) \
             + '&from=' + fromLang \
             + '&to=' + toLang \
             + '&salt=' + str(salt) \
             + '&sign=' + sign

    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myUrl)

        response = httpClient.getresponse()
        print response.read()
        return response
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return None


if __name__ == '__main__':
    translate('translate', lang_auto, lang_auto)

    pass
