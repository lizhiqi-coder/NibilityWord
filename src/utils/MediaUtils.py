# coding:utf-8
import functools
import os
import threading
import urllib

import pygame.mixer as AudioPlayer

from src.base.Thread import WorkThread


def hashUrl(url):
    value = url.replace('/', '_').replace(':', '#')
    return value


def download(myurl, saveDir, _callback=None):
    """没有开启新的线程"""
    file_name = hashUrl(myurl)
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    savePath = os.path.join(saveDir.decode('utf-8'), file_name.decode('utf-8'))

    urllib.urlretrieve(myurl, savePath, _callback)


def localSearch(file_name, search_dir):
    dir = os.path.abspath(search_dir)
    file_path = os.path.join(dir, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return file_path
    else:
        return False


class MediaConfig():
    def __init__(self):
        self.savePath = None


class MediaLoader():
    _INSTANCE = None

    @staticmethod
    def getInstance():
        return MediaLoader()

    def __new__(cls, *args, **kwargs):
        if not MediaLoader._INSTANCE:
            try:
                threading.Lock().acquire()

                MediaLoader._INSTANCE = super(MediaLoader, cls).__new__()

            finally:
                threading.Lock().release()
        return MediaLoader._INSTANCE

    def __init__(self):
        defaultDir = os.path.abspath('./res/cache/')
        cfg = MediaConfig()
        cfg.savePath = defaultDir
        self.config(cfg)
        pass

    def config(self, conf):
        self._conf = conf
        AudioPlayer.init()
        return self

    def loadMedia(self, mediaUrl):
        self._media_url = mediaUrl
        self._media_path = None
        self.work = None
        # 三级缓存（内存，硬盘，网络），目前二级缓存（硬盘，网络）
        local_search_result = localSearch(hashUrl(self._media_url), self._conf.savePath)
        if local_search_result:  # 本地加载成功
            self._media_path = local_search_result
            self._media_url = None
        else:
            download_runable = functools.partial(download, self._media_url,
                                                 self._conf.savePath,
                                                 self._mediaDownloadCallback)

            self.work = WorkThread(download_runable)
            self.work.start()
        return self

    def _mediaDownloadCallback(self, num, size, totalsize):
        """该方法在子线程中执行"""
        percent = 100.0 * num * size / totalsize
        if percent >= 100:
            percent = 100
        if percent == 100:
            print 'download succeed'
            self._media_path = localSearch(hashUrl(self._media_url), self._conf.savePath)
        else:
            print percent

    def playAudio(self):
        if self.work and not self.work.isStopped():
            self.work.wait()

        if self._media_path:
            AudioPlayer.music.load(self._media_path)
            AudioPlayer.music.play()
