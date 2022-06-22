"""
@author: william
@time: xxx/xx/xx

description:
-----------
crawl magnet link according to search keyword.
"""
import spider
from requests import Response


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
    print(html_content)


if __name__ == "__main__":
    search_info(PAGE_URL)
    
