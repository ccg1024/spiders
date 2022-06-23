# -*- coding: utf-8 -*-
"""
 File description:
 The display format of terminal.

 [+] MAGNET SPIDER
 [>] INTO SCRIPT CONSOLE!
 [<] INPUT KEY WORDS:
 [#] RESULTS
 # [ 1] xx
 # [ 2] xx
 # .... xx
 # [12] xx
 [>] OPTION WORDS: [n] next; page:1/?; [r] search new; [e] exit;
 [<] OPTION WORDS: 
 [>] BEGIN NEW SEARCH
 [<] INPUT KEY WORDS:

 @autor: ccg
 @date: 2022 02 09 3:19 下午
 @path: pythonProject-PyCharm-magnetar

"""
import spider
import argparse


# add command
parser = argparse.ArgumentParser(description='crawl magnet through xxxxxxxxxxxxxxxxxxxxxxxxxxxx')
parser.add_argument('-v', '--version', help='show the script version', action='store_true')
parser.add_argument('-w', '--word', help='search word, when run the script')
parser.add_argument('-t', '--type', help='the type of source shown, all; video; img; compress;'
                                         'music; program; document; other', choices=['all',
                                                                                     'video', 'img',
                                                                                     'compress',
                                                                                     'music',
                                                                                     'program',
                                                                                     'document',
                                                                                     'other'])
parser.add_argument('-s', '--safe', help='whether open safe search, when close, the result may '
                                         'include some porn message', action='store_true')
parser.add_argument('-o', '--order', help='choose how to sort the resources, default; time; size; '
                                          'repeat', choices=['default', 'time', 'size', 'repeat'])
args = parser.parse_args()

# information aboult scirpt
info = """[+] MAGNET SPIDER"""
version = '1.0.0'

# magnet head
magnet_head = 'magnet:?xt=urn:btih:'


# crawler api
def api_func(key_words, crawl, page=1, file_order=None, file_type=None):
    # m stands for sorting, t stands for type
    file_order = str(file_order) if file_order is not None else 'time'
    file_type = str(file_type) if file_type is not None else 'video'
    url = f'xxxxx:xxxxx.xxxxxxxx.xx/xxxxxx/xx.xxxx/xxxxxxx?q={key_words}&m={file_order}&' \
          f't={file_type}&p={page}'
 
    # obtains response source
    api_result = crawl.get(url).text
    # json_result = json.loads(api_result)

    # search_btdatas = json_result['searchBtData']
    json_result = crawl.json_crawl(api_result)
    search_btdatas = json_result['searchBtData']

    total_data = 0
    item_num = 0

    if search_btdatas is None:
        print(f'can not find anything form API for: {key_words}')
    else:
        # total number of data
        total_data = json_result['total']

        item_num = 1
        print('[#] RESULTS')
        for btdata in search_btdatas:
            print('# [{:2d}]'.format(item_num), end=' ')
            print(btdata['name'].replace('<font style=\'color:#dd4b39;\'>', '')
                  .replace('</font>', ''))

            print('# \t\t ', end='')
            print(magnet_head + btdata['hash'])
            item_num += 1

    return int(total_data), item_num - 1


# display input information
def input_control(first_word):
    """
    controller of input
    """
    if first_word is not None:
        key_words = first_word
        print(f'[>] INPUT KEY WORDS: {key_words}')
    else:
        key_words = input('[<] INPUT KEY WORDS: ')
    return key_words


def option_control(page_num, total_page):
    """
    controller of options
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
    obtains script's command
    """
    # Get controller behavior
    console_token = input("[<] OPTION WORDS: ")

    # Determine the controller command format
    while console_token not in (PRE_PAGE, NEXT_PAGE, EXIT_CONSOLE, NEW_SEARCH):
        print("[INFO] The key world should in ({}, {}, {}, {})".format(PRE_PAGE, NEXT_PAGE,
                                                                       EXIT_CONSOLE, NEW_SEARCH))
        console_token = input("[<] OPTION WORDS: ")

    return console_token


def main():
    """
    Controllor function
    """
    NEXT_PAGE = 'n'
    PRE_PAGE = 'N'
    EXIT_CONSOLE = 'e'
    NEW_SEARCH = 'r'

    # Get args of command line
    file_order = args.order
    file_type = args.type
    safe_search = args.safe
    first_word = args.word

    # Create crawler object
    crawl = spider.Crawl()
    # crawl = Crawl()

    # Add key-value pairs of request header
    tag_safe = 'on' if safe_search else 'off'
    crawl.add_headers_elem('safesearch', tag_safe)

    print(info)
    print("[>] INTO SCRIPT CONSOLE!")

    # controller input
    console_token = NEW_SEARCH
    total_page = 0
    page_num = 1
    key_words = ''
    while console_token != EXIT_CONSOLE:
        if console_token == NEW_SEARCH:
            key_words = input_control(first_word)

            # Determine whether key_words is an exit command
            if key_words.replace(' ', '') == 'exit' or key_words.replace(' ', '') == 'e':
                break

            first_word = None
            page_num = 1
            try:
                total_data, page_items = api_func(key_words, crawl, page=page_num,
                                                  file_order=file_order, file_type=file_type)

                if total_data == 0:
                    continue

                total_page = total_data // page_items
                if total_data % page_items != 0:
                    total_page += 1
            except Exception as e:
                print('[ERROR] Got some error in \'input key words\' part.')
                print(e)
                break
        console_options = option_control(page_num=page_num, total_page=total_page)

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

    print('[>] CLOSE.')


if __name__ == '__main__':
    if args.version:
        print(f'the version of magnet spider is: {version}')
    else:
        main()
