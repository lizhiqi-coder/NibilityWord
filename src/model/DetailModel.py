# coding:utf-8


class exchange:
    """单词变换形态"""

    def __init__(self,
                 word_pl='',
                 word_third='',
                 word_past='',
                 word_done='',
                 word_ing='',
                 word_er='',
                 word_est=''):
        self.word_pl = word_pl
        self.word_third = word_third
        self.word_past = word_past
        self.word_done = word_done
        self.word_ing = word_ing
        self.word_er = word_er
        self.word_est = word_est


class symbol:
    def __init__(self, ph_en, ph_en_mp3, ph_am, ph_am_mp3, part_means):
        self.ph = {'ph_en': [ph_en, ph_en_mp3],
                   'ph_am': [ph_am, ph_am_mp3]}
        self.part_means = part_means  # dict


class DetailModel:
    def __init__(self, word_name, exchange, symbols):
        self.word_name = word_name
        self.exchange = exchange
        self.symbols = symbols  # list


class DictResult():
    def __init__(self, query, translation, phones, explains, web=None):
        self.query = query
        self.translation = translation
        self.phones = phones
        self.explains = explains
        self.web = web
