# coding:utf-8
import httplib
import md5
import urllib
import random

appid = ''
secretKey = ''
httpClient = None
myUrl = '/api/trans/vip/translate'
q = 'android'
fromLang = 'en'
toLang = 'zh'

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
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()


def translate(question, fromLang, toLang):
    return None


if __name__ == '__main__':
    pass
