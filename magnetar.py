# -*- coding: utf-8 -*-
"""
 文件描述:
 终端显示方式
 [+] MAGNET SPIDER
 [>] INTO SCRIPT CONSOLE!
 [>] INPUT KEY WORDS:
 [INFO] 2022-02-22 xxx
 [#] RESULTS
 # [ 1] xx
 # [ 2] xx
 # [12] xx
 [>] OPTION WORDS: [n] next;
 [$]:
 [>] BEGIN NEW SEARCH
 [>] INPUT KEY WORDS:
 @作者: ccg
 @日期: 2022 02 09 3:19 下午
 @路径: pythonProject-PyCharm-magnetar
"""
import spider
import json
import argparse

parser = argparse.ArgumentParser(description='crawl magnet through api: https://api.magnetar.cc')
parser.add_argument('-v', '--version', help='show the script version', action='store_true')
parser.add_argument('-w', '--word', help='search word, when run the script')
parser.add_argument('-t', '--type', help='the type of source shown, all; video; img; compress; music;'
                                         'program; document; other', choices=['all', 'video', 'img', 'compress',
                                                                              'music', 'program', 'document',
                                                                              'other'])
parser.add_argument('-s', '--safe', help='whether open safe search, when close, the result may include some porn '
                                         'message', action='store_true')
parser.add_argument('-o', '--order', help='choose how to sort the resources, default; time; size; repeat',
                    choices=['default', 'time', 'size', 'repeat'])
args = parser.parse_args()

info = """[+] MAGNET SPIDER"""
version = '1.0.0'

# magnet head
magnet_head = 'magnet:?xt=urn:btih:'


def api_func(key_words, crawl, page=1, file_order=None, file_type=None):
    # m 代表排序方式，t 代表类型
    file_order = str(file_order) if file_order is not None else 'time'
    file_type = str(file_type) if file_type is not None else 'video'
    url = f'https://api.magnetar.cc/search/v2.index/search?q={key_words}&m={file_order}&t={file_type}&p={page}'
    # 得到请求结果
    api_result = crawl.get(url).text
    json_result = json.loads(api_result)

    search_btdatas = json_result['searchBtData']

    total_data = 0
    item_num = 0

    if search_btdatas is None:
        print(f'can not find anything form API for: {key_words}')
    else:
        # 资源总数
        total_data = json_result['total']
        
        item_num = 1
        print('[#] RESULTS')
        for btdata in search_btdatas:
            print('# [{:2d}]'.format(item_num), end=' ')
            print(btdata['name'].replace('<font style=\'color:#dd4b39;\'>', '').replace('</font>', ''))
            
            print('# \t\t ', end='')
            print(magnet_head + btdata['hash'])
            item_num += 1

    return int(total_data), item_num - 1


def input_control(first_word):
    """
    输入控制器
    :return:
    """
    if first_word is not None:
        key_words = first_word
        print(f'[>] INPUT KEY WORDS: {key_words}')
    else:
        key_words = input('[>] INPUT KEY WORDS: ')
    return key_words


def option_control(page_num, total_page):
    """
    选项控制器
    :return:
    """
    # option control
    console_options = "page:{}/{};  [r] search new;  [e] exit;".format(page_num, total_page)
    if page_num < total_page:
        console_options = '[n] next;  ' + console_options
    if page_num > 1:
        console_options = '[N] pre;  ' + console_options
    print('[>] OPTION WORDS: ' + console_options)
    return console_options


def get_console_token(PRE_PAGE, NEXT_PAGE, EXIT_CONSOLE, NEW_SEARCH):
    """
    获取脚本行为命令
    :return:
    """
    # 获取控制器行为
    console_token = input("[<] OPTION WORDS: ")

    # 判断控制器命令格式
    while console_token not in (PRE_PAGE, NEXT_PAGE, EXIT_CONSOLE, NEW_SEARCH):
        print("[INFO] The key world should in ({}, {}, {}, {})".format(PRE_PAGE, NEXT_PAGE,
                                                                       EXIT_CONSOLE, NEW_SEARCH))
        console_token = input("[<] OPTION WORDS: ")

    return console_token


def main():
    """
    控制台方法
    """
    NEXT_PAGE = 'n'
    PRE_PAGE = 'N'
    EXIT_CONSOLE = 'e'
    NEW_SEARCH = 'r'

    # 获取命令行参数
    file_order = args.order
    file_type = args.type
    safe_search = args.safe
    first_word = args.word

    # 创建爬虫对象
    crawl = spider.Crawl()
    # crawl = Crawl()

    # 添加请求头元素
    tag_safe = 'on' if safe_search else 'off'
    crawl.add_headers_elem('safesearch', tag_safe)

    print(info)
    print("[>] INTO SCRIPT CONSOLE!")
    # 控制台输入
    console_token = NEW_SEARCH
    total_page = 0
    page_num = 1
    key_words = ''
    while console_token != EXIT_CONSOLE:
        if console_token == NEW_SEARCH:
            # 封装进了函数
            # if first_word is not None:
            #     key_words = first_word
            #     first_word = None
            #     print(f'[>] INPUT KEY WORDS: {key_words}')
            # else:
            #     key_words = input('[>] INPUT KEY WORDS: ')
            key_words = input_control(first_word)
            first_word = None
            page_num = 1
            try:
                total_data, page_items = api_func(key_words, crawl, page=page_num, file_order=file_order,
                                                  file_type=file_type)
                
                if total_data == 0:
                    continue
                    
                total_page = total_data // page_items
                if total_data % page_items != 0:
                    total_page += 1
            except Exception as e:
                print('[ERROR] Got some error in \'input key words\' part.')
                print(e)
                break
        # # option control --- 封装进来函数
        # console_options = "page:{}/{};  [r] search new;  [e] exit;".format(page_num, total_page)
        # if page_num < total_page:
        #     console_options = '[n] next;  ' + console_options
        # if page_num > 1:
        #     console_options = '[N] pre;  ' + console_options
        # print('[>] OPTION WORDS: ' + console_options)
        console_options = option_control(page_num=page_num, total_page=total_page)

        # # 获取控制器行为  --- 封装进函数
        # console_token = input("[<] OPTION WORDS: ")
        #
        # # 判断控制器命令格式
        # while console_token not in (PRE_PAGE, NEXT_PAGE, EXIT_CONSOLE, NEW_SEARCH):
        #     print("[INFO] The key world should in ({}, {}, {}, {})".format(PRE_PAGE, NEXT_PAGE,
        #                                                                    EXIT_CONSOLE, NEW_SEARCH))
        #     console_token = input("[$]:")
        console_token = get_console_token(PRE_PAGE, NEXT_PAGE, EXIT_CONSOLE, NEW_SEARCH)

        # make action
        if console_token == NEXT_PAGE and page_num < total_page:
            print('')
            page_num += 1
            api_func(key_words, crawl, page=page_num, file_order=file_order, file_type=file_type)
        elif console_token == PRE_PAGE and page_num > 1:
            print('')
            page_num -= 1
            api_func(key_words, crawl, page=page_num, file_order=file_order, file_type=file_type)
        elif console_token == EXIT_CONSOLE:
            break
        elif console_token == NEW_SEARCH:
            print("[>] BEGIN NEW SEARCH")
        else:
            print("[INFO] The option word should be shown above.")
            print('[>] OPTION WORDS: ' + console_options)
        pass

    print('[<] CLOSE.')


if __name__ == '__main__':
    if args.version:
        print(f'the version of magnet spider is: {version}')
    else:
        main()
