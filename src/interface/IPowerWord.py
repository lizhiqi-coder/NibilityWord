# coding:utf-8
"""金山词霸"""
import httplib

# sys.path.append('..')
from src.model.DetailModel import *

myUrl = '/api/dictionary.php'
secretKey = 'C75843D78A50DD1378BADC7A8BD3995D'


def translate(question, type='json'):
    httpClient = None
    global myUrl
    myUrl += '?w=' + question \
             + '&type=' + type \
             + '&key=' + secretKey
    try:
        httpClient = httplib.HTTPConnection('dict-co.iciba.com')
        httpClient.request('GET', myUrl)
        response = httpClient.getresponse()
        print response.read()
        return DetailModel()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return None


if __name__ == '__main__':
    translate('girl', type='json')
