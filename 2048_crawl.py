"""
@author: william
@time: xxx/xx/xx

description:
-----------
crawl magnet link according to search keyword.
"""
import spider
from requests import Response
from lxml import etree


PAGE_URL = 'https://bbs.cp500111.com/2048/thread.php?fid-28-page-{}.html'


def search_info(url: str = None, keywords: str = None) -> Response:
    """
    Search keyword information from the page which url indicating.

    : param url      : the searching page url. Default is None.
    : param keywords : the keywords which use to search. use space to split
    :                : multi-key. Default is None.
    """
    assert url is not None, "Maybe need to put a url."
    crawler = spider.Crawl()
    html_content = crawler.get(url).content
    table_html = crawler._xpath(html_content, '//div[@class="t z"]/table//tbody')
    tr_xpath_list = crawler._xpath(table_html[0], 'tr')
    for tr_xpath in tr_xpath_list[8:-2]:
        # print(etree.tostring(tr_xpath))
        link_tag = crawler._xpath(tr_xpath, 'td[2]/a')
        if len(link_tag) > 0:
            link_tag = link_tag[0]
            print(crawler._xpath(link_tag, "text()"))
            print(crawler._xpath(link_tag, "@href"))
        else:
            print("[E] Got empty xpath")


if __name__ == "__main__":
    search_info(PAGE_URL)
    
