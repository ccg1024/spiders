"""
  Encapsulate some of your own commonly used crawler code.
  
  EXAMPLE
  -------
  >>> crawl = Crawl()
  >>> crawl.get('https://www.baidu.com')

"""
import json
import os
from typing import Any
import requests
from lxml import etree
from requests.exceptions import RequestException


class Crawl:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159\
                          Safari/537.36"
        }

    def get_headers(self) -> dict:
        """
        The default headers only have user-agent key-value pairs.

        RETURN:

        Returns the headers object in the crawler object

        """
        return self.headers

    def add_headers_elem(self, key, value) -> None:
        """
        Add headers key-value pairs.

        ARGS:

        param key   : string object
        param value : string object

        """
        self.headers[key] = value
        print(f'[I] Add elem \'{key}\':\'{value}\'')

    def change_headers(self, headers):
        """
        Modify the headers object.

        ARGS:

        param headers: new request headers

        """
        self.headers = headers
        print('[I] Replace headers successfully.')

    def make_new_session(self):
        """
        Close the current session.

        """
        self.session.close()
        print('[I] Create a new session object')

    def get(self, url, **kwargs):
        """
        Get function of requests module.

        ARGS:

        param url    : website of resources
        param kwargs : the others key-value pairs of get function

        RETURN:

        response

        """
        try:
            res = requests.get(url, headers=self.headers, **kwargs)
            return res
        except RequestException as error_handle:
            print(error_handle)
            return None
        # return requests.get(url, headers=self.headers, **kwargs)

    def post(self, url, **kwargs):
        """
        Post function of requests module.

        RETURN:

        response

        """
        try:
            res = requests.post(url=url, headers=self.headers, **kwargs)
            return res
        except RequestException as error_handle:
            print(error_handle)
            return None
        # return requests.post(url, headers=self.headers, **kwargs)

    @staticmethod
    def _xpath(doc: Any, xpath: str = None):
        """ Perform xpath analysis on the acquired data. """
        assert doc is not None, 'the param \'doc\' should not be None.'
        assert isinstance(doc, [str, bytes]), '[W] Can not recognize the type of param \'doc\''
        assert isinstance(xpath, str), 'the param \'xpath\' should be str.'

        if isinstance(doc, str):
            etree_obj = etree.fromstring(doc)
        elif isinstance(doc, bytes):
            etree_obj = etree.HTML(doc)
        else:
            etree_obj = doc
        # return result
        return etree_obj.xpath(xpath)

    def json_crawl(self, doc: str = None, url: str = None, _key: str = None):
        """
        For crawling and formatting json data. it can receive dde string object returned by 
        Response, or it can get the json data through the 'url'.
        
        ARGS:

        param doc  : format json data from string. if not empty, the 'doc' param will be processed
                   : first and the value of 'url' param will be ignored. Default=None
        param url  : the url address for crawling json data. the address will be searched only when
                   : the 'doc' param is None. Default=None
        param _key : after formatting json data, the '_key' param will be use when just need one
                   : key-value pairs data of json. Default=None

        """
        json_result = None
        if doc is not None:
            json_result = json.loads(doc)
        elif url is not None:
            response = self.get(url)
            json_result = json.loads(response.text)

        if _key is not None:
            return json_result[_key]
        return json_result

    @staticmethod
    def save(contents, file_prefix: str = 'saved', file_suffix: str = '.jpg', file_dir: str = './',
            mode: str = 'wb', is_url: bool = False):
        """
        Store the obtained content in a file.

        ARGS:
        
        param contents     : the content stored in the file, or the URL to get the content, used with
                           : 'is_url' param
        param file_prefix  : stored filename prefix. Default=saved
        param file_suffix  : stored filename suffix. Default=.jpg
        param file_dir     : the folder path where the file is stored. Default=./
        param mode         : the mode in which the file is stored
        param is_url       : determines whether the 'contents' param is a URL. Default=False

        """

        assert contents is not None, 'param \'contents\' should not be None.'
        if is_url:
            pass
        if file_dir != './' and not os.path.exists(file_dir):
            os.mkdir(file_dir)
        file_name = file_prefix + file_suffix
        file_path = file_dir + file_name

        # write file
        with open(file_path, mode) as file_handle:
            file_handle.write(contents)

        print('saving file: {} to {} successfully.'.format(file_name, file_path))

    def __call__(self) -> Any:
        """
        when the object of class Crawl is used as a function, this inner function will be use.

        """
        print("using the inner function \'__call__()\'")
        pass
