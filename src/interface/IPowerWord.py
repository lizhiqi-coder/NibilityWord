# coding:utf-8
"""金山词霸"""
import httplib2
import json

from src.model.DetailModel import *

gUrl = 'http://dict-co.iciba.com/api/dictionary.php'
secretKey = 'C75843D78A50DD1378BADC7A8BD3995D'


def translate(question, type='json'):
    httpClient = None
    global gUrl
    myUrl = gUrl
    myUrl += '?w=' + question \
             + '&type=' + type \
             + '&key=' + secretKey
    try:
        httpClient = httplib2.Http()
        response, content = httpClient.request(myUrl)
        print content

        json_data = json.loads(content)

        result = __parse_json(json_data=json_data)
        return result

    except Exception, e:
        print e
    finally:
        pass
    return None


def __parse_json(json_data):
    _exchange = exchange(
        json_data['exchange']['word_pl'],
        json_data['exchange']['word_third'],
        json_data['exchange']['word_past'],
        json_data['exchange']['word_done'],
        json_data['exchange']['word_ing'],
        json_data['exchange']['word_er'],
        json_data['exchange']['word_est']
    )
    _symbols = []
    for js_symbol in json_data['symbols']:
        _means = []
        for item in js_symbol['parts']:
            _means.append(item['means'])
        _symbol = symbol(js_symbol['ph_en'],
                         js_symbol['ph_en_mp3'],
                         js_symbol['ph_am'],
                         js_symbol['ph_am_mp3'],
                         _means)
        _symbols.append(_symbol)

    _result = DetailModel(json_data['word_name'], _exchange, _symbols)
    return _result


if __name__ == '__main__':
    translate('girl', type='json')
