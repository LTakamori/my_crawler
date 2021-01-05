from gevent import monkey

monkey.patch_all()
import gevent
import requests
import time
from bs4 import BeautifulSoup
import sqlite3


def url_for(begin, end):
    return ["http://pages.iseezju.com/bachelorsdetail/{}".format(index) for index in range(begin, end)]


def main():
    urls = ["http://pages.iseezju.com/bachelorsdetail/{}".format(i) for i in range(1, 3)]
    crawler_list = [Crawler(url_for(1, 10)), Crawler(url_for(11, 10))]
    jobs = [gevent.spawn(crawler.run) for crawler in crawler_list]
    gevent.joinall(jobs)


class Crawler:
    def __init__(self, url_list):
        self.url_list = url_list

    def run(self):
        for url in self.url_list:
            page = self.get_page(url)
            self.parse_page(page.text)
            print("Finished parsing url: {}".format(url))

    def get_page(self, url):
        print("Starting get page: {}".format(url))
        result = requests.get(url)
        return result

    def parse_page(self, text):
        soup = BeautifulSoup(text, 'lxml')
