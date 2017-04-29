# coding:utf-8
import os
import xml.etree.ElementTree as ET

R_file_path = './R.py'


def __search_image():
    current_dir = os.path.abspath('.')
    result = []
    for root, sub_dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.png'):
                result.append(os.path.join(root, file))

    return result


def __search_qss():
    current_dir = os.path.abspath('.')
    result = []
    for root, sub_dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.qss') or file.endswith('.css'):
                result.append(os.path.join(root, file))

    return result


def _search_html():
    current_dir = os.path.abspath('.')
    result = []
    for root, sub_dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.html'):
                result.append(os.path.join(root, file))
    return result

def __build_image_indexing(index_list, namespace):
    buf = '#coding:utf-8\r\n'
    buf += 'class ' + namespace + '():'
    buf += '\r'
    for index in index_list:
        buf += '    '
        buf += os.path.basename(index).split('.')[0]
        buf += ' = '
        buf += "r'"
        buf += index
        buf += "'"
        buf += '\r\n'

    return buf


def __build_file_indexing(index_list, namespace):
    buf = '\r'
    buf += 'class ' + namespace + '():'
    buf += '\r'
    for index in index_list:
        buf += '    '
        buf += os.path.basename(index).split('.')[0]
        buf += ' = '
        buf += "r'"
        buf += index
        buf += "'"
        buf += '\r\n'
    return buf


def __build_string_values(dict, namespace):
    R_file = open(R_file_path, 'w')

    buf = '\r'
    buf += 'class ' + namespace + '():'
    buf += '\r'

    for key in dict:
        value = dict[key]
        buf += '    '
        buf += key
        buf += ' = '
        buf += "u'"
        buf += str(value.encode('utf-8'))
        buf += "'"
        buf += '\r\n'
    return buf


def __build_int_values(dict, namespace):
    R_file = open(R_file_path, 'w')

    buf = '\r'
    buf += 'class ' + namespace + '():'
    buf += '\r'

    for key in dict:
        value = dict[key]
        buf += '    '
        buf += key
        buf += ' = '
        buf += str(value)
        buf += '\r\n'
    return buf


def __write_to_file(buf, file_path):
    R_file = open(file_path, 'w')
    try:
        R_file.write(buf)
        R_file.close()
    except IOError:
        print 'IOError'


def __parse_xml_values(file_path, main_tag):
    dict = {}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for child in root:
            if child.tag == main_tag:
                key = child.attrib['name']
                value = child.text
                dict[key] = value

    except Exception, e:
        print 'Error:can not parse xml'
    return dict


def start():
    image_paths = __search_image()

    buf = __build_image_indexing(index_list=image_paths, namespace='png')

    string_dict = __parse_xml_values('./values/strings.xml', 'string')
    buf += __build_string_values(string_dict, namespace='string')

    int_dict = __parse_xml_values('./values/dimens.xml', 'dimen')
    buf += __build_int_values(int_dict, namespace='dimen')

    qss_paths = __search_qss()
    buf += __build_file_indexing(qss_paths, namespace='qss')

    html_paths = _search_html()
    buf += __build_file_indexing(html_paths, namespace='html')
    __write_to_file(buf, R_file_path)


if __name__ == '__main__':
    start()
    print "R create succeed !"
