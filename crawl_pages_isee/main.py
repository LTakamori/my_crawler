from gevent import monkey
monkey.patch_all()

import gevent
import sqlite3
import time

from crawler import Crawler

db_dir = "./fuck_fw.db"


def main():
    time1 = time.time()
    connection = sqlite3.connect(db_dir)
    crawler_list = [Crawler(url_for(1, 1000), connection), Crawler(url_for(1001, 2000), connection),
                    Crawler(url_for(2001, 3000), connection), Crawler(url_for(3001, 4000), connection),
                    Crawler(url_for(4001, 5024), connection)]
    c = connection.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS TEACHER_TABLE
             (TEACHER_ID INT,
              TEACHER_NAME TEXT,
              RATE TEXT,
              RATE_NUM TEXT,
              FACULTY TEXT);''')
    c.execute('''CREATE TABLE IF NOT EXISTS CLASS_TABLE
                 (TEACHER_ID INT,
                  CLASS_NAME TEXT,
                  CLASS_GPA TEXT);''')
    c.execute('''CREATE TABLE IF NOT EXISTS COMMENT_TABLE
             (TEACHER_ID INT,
              COMMENT_TIME TEXT,
              CONTENT TEXT,
              APPROVE_NUM INT);''')
    jobs = [gevent.spawn(crawler.run) for crawler in crawler_list]  # This can do, use run instead of run()
    gevent.joinall(jobs)
    connection.commit()
    connection.close()
    time2 = time.time()
    print("The total amount of time is: {}".format(time2 - time1))


def url_for(begin, end):
    return ["http://pages.iseezju.com/bachelorsdetail/{}".format(index) for index in range(begin, end)]


if __name__ == "__main__":
    main()
