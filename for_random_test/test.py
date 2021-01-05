from gevent import monkey

monkey.patch_all()
import gevent
import requests
import time
from bs4 import BeautifulSoup
import sqlite3


def main():
    urls = ["http://pages.iseezju.com/bachelorsdetail/{}".format(i) for i in range(1, 3)]
    crawler_list = [Crawler(url) for url in urls]
    jobs = [gevent.spawn(crawler.run) for crawler in crawler_list]
    gevent.joinall(jobs)
    # TODO: 问题出在loop里面


class Crawler:
    def __init__(self, url):
        self.url = url

    def run(self):
        for i in range(100):
            page = self.get_page()
        self.parse_page(page.text)
        print("Finished parsing url: {}".format(self.url))

    def get_page(self):
        print("Starting get url: {}".format(self.url))
        result = requests.get(self.url)
        return result

    def parse_page(self, page):
        print("Starting parsing url: {}".format(self.url))

        soup = BeautifulSoup(page, "lxml")


if __name__ == "__main__":
    main()
