from gevent import monkey
import gevent
import requests
import time
from bs4 import BeautifulSoup
import sqlite3

monkey.patch_all()


def main():
    # urls = ["http://pages.iseezju.com/bachelorsdetail/{}".format(i) for i in range(1, 10)]
    # jobs = [gevent.spawn(get_page, url) for url in urls]
    # gevent.joinall(jobs)
    conn = sqlite3.connect('./test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS CLASS_GPA
                  (class text, gpa text)''')
    url = "http://pages.iseezju.com/bachelorsdetail/1"
    r = get_page(url)
    soup = BeautifulSoup(r.text, 'lxml')
    tables = soup.find_all('table')
    # print(len(tables))
    class_table = tables[0]
    entry_list = class_table.tbody.find_all('tr')
    for entry in entry_list:
        values = entry.find_all('td')
        class_name, class_gpa = values[0], values[1]
        # print("{}: {}".format(class_name.string, class_gpa.string))
        c.execute("INSERT INTO CLASS_GPA (class, gpa)\
                  values ('{}','{}')".format(class_name.string, class_gpa.string))
    a = c.execute("SELECT class, gpa from class_gpa")
    for item in a:
        print("{}: {}".format(item[0], item[1]))
    conn.commit()
    conn.close()


def get_page(url: str):
    print("Starting get url: {}".format(url))
    result = requests.get(url)
    print(result)
    return result


if __name__ == "__main__":
    main()
