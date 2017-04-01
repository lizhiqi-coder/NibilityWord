# NiubilityWord
* 跨平台词典翻译工具
* 模仿金山词霸查词工具条
* 针对经常需要看英文文档的英语渣渣而设计

###结构框架:
* 资源管理 RCreator.py
* 页面管理
* 网络接口管理
* 数据管理

###tips:
* pyqt样式官方为qss,实际上可以直接使用css,IDEA会有自动补全提示,非常方便
* 本地离线词典使用使用lingoes词典文件

##安装环境：
* python2.7
* pyqt or pyside
* pygame(用于音频播放)
* multiprocessing (用于实现守护进程)
* pyhook(window平台快捷键设置)

##参考资料：
* 本地离线词典使用lingoes格式:http://www.cnblogs.com/SuperBrothers/archive/2012/11/24/2785971.html
* lingoes词典文件(ld2,ldx)解析:https://github.com/librehat/kdictionary-lingoes
* https://github.com/pingjiang/opendict
* https://github.com/PurlingNayuki/lingoes-extractor
* python操作字节流:http://www.jianshu.com/p/5a985f29fa81
