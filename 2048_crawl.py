"""
@author: william
@time: xxx/xx/xx

description:
-----------
crawl magnet link according to search keyword.
"""
import spider
import re
import os

PAGE_URL = ''
PROFIX_URL = ''


def search_info(url: str = "", keywords: str = "") -> list:
    """
    Search keyword information from the page which url indicating.

    : param url      : the searching page url. Default is None.
    : param keywords : the keywords which use to search. use space to split
    :                : multi-key. Default is None.
    """
    assert url != "", "Maybe need to put a url."
    # initial return obj
    res_list = []

    print("Begin Crawl: ", url)
    # get the main web content
    crawler = spider.Crawl()
    html_content = crawler.get(url).content
    table_html = crawler.xpath__(html_content, '//div[@class="t z"]/table//tbody')
    tr_xpath_list = crawler.xpath__(table_html[0], 'tr')

    # get the name list and link list of anime info
    name_list = []
    link_list = []
    for tr_xpath in tr_xpath_list[8:-2]:
        # print(etree.tostring(tr_xpath))
        link_tag = crawler.xpath__(tr_xpath, 'td[2]/a')
        if len(link_tag) > 0:
            link_tag = link_tag[0]
            name_list.append(crawler.xpath__(link_tag, "text()")[0])
            link_list.append(crawler.xpath__(link_tag, "@href")[0])
        else:
            print("[E] Got empty xpath")

    # using re to match special item
    pat_str = r'.*?'

    keywords_list = keywords.split(" ") if keywords is not None \
        and keywords != "" else []
    if len(keywords_list) > 0:
        for item in keywords_list:
            pat_str += item + ".*?"
    pattern = re.compile(pat_str)

    name_len = len(name_list)
    matched_list = []
    matched_idx = []
    for idx in range(name_len):
        match_res = re.match(pattern, name_list[idx])
        if match_res is not None:
            matched_list.append(match_res.group(0))
            matched_idx.append(idx)

    for idx in matched_idx:
        # get special image page for reading
        target_page_url = PROFIX_URL + link_list[idx]

        target_html = crawler.get(target_page_url).content
        img_div = crawler.xpath__(target_html, '//div[@id="read_tpc"]')[0]
        # get img html list: tag -> ignore_js_op
        img_html_list = crawler.xpath__(img_div, 'ignore_js_op/img')

        img_url_list = []
        for img_html in img_html_list:
            # get img url
            img_url = crawler.xpath__(img_html, '@src')[0]
            img_url_list.append(img_url)

        # the type of return obj is list(dict())
        item_dict = {'img_name': name_list[idx], 'img_urls': img_url_list}
        res_list.append(item_dict)

    return res_list


def save_info(source_obj: list, save_path: str = "source") -> None:
    assert isinstance(source_obj, list), "the 'source_obj' must be a list."

    # instance a crawl
    crawler = spider.Crawl()

    # if save_path is not exist, create.
    if not os.path.exists(save_path):
        print("create dirctory {} in current path.".format(save_path))
        os.makedirs(save_path)

    for source_dict in source_obj:
        # generate store path of anime
        anime_path = save_path + "/" + source_dict['img_name']

        # make sure path exist
        if not os.path.exists(anime_path):
            print("begin crawl anime: ", source_dict['img_name'])
            os.makedirs(anime_path)
        else:
            keyword = input("anime {} is already exist, need rewrite?[y/n]".format(
                source_dict['img_name']))
            if keyword == "y":
                print("redonwload anime: ", source_dict['img_name'])
            else:
                continue

        # download anime
        img_name = 0
        img_numbers = len(source_dict['img_urls'])
        for img_link in source_dict['img_urls']:
            with open(anime_path + "/" + str(img_name) + ".png", "wb") as file_handle:
                file_handle.write(crawler.get(img_link).content)

            img_name += 1
            print('\r' + "downloading...[{}/{}]".format(img_name, img_numbers), end='')


if __name__ == "__main__":
    info = search_info(PAGE_URL.format(str(1)), "")
    save_info(info, "./source/img")
    
