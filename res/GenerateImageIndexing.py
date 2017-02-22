# coding:utf-8
import os


def searchImage():
    current_dir = os.path.abspath('.')
    result = []
    for root, sub_dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.png'):
                result.append(os.path.join(root, file))

    return result


def buildIndexing(index_list, namespace):
    R_file = open('./R.py', 'w')
    buf = '#coding:utf-8\r\n'
    buf += 'class ' + namespace + ' ():'
    buf += '\r'
    for index in index_list:
        buf += '  '
        buf += os.path.basename(index).split('.')[0]
        buf += ' = '
        buf += "r'"
        buf += index
        buf += "'"
        buf += '\r\n'

    try:
        R_file.write(buf)
        R_file.close()
    except IOError:
        print 'IOError'


def start():
    image_paths = searchImage()
    print image_paths
    buildIndexing(index_list=image_paths, namespace='png')


if __name__ == '__main__':
    start()
