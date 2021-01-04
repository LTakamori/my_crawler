import requests
from bs4 import BeautifulSoup
import sqlite3


db_dir = "./fuck_fw.db"


class Crawler:
    def __init__(self, url_list: list, connection):
        self.url_list = url_list
        self.c = connection.cursor()
        pass

    def run(self):
        for url in self.url_list:
            page = self.get_page(url)
            print("Finished getting page: {}".format(url))
            soup = BeautifulSoup(page.text, 'lxml')
            teacher_id = int(url[41:])
            self.strategy(soup, teacher_id)
        pass

    @staticmethod
    def get_page(url: str):
        print("Starting getting page: {}".format(url))  # TODO: Here!
        return requests.get(url)

    def strategy(self, soup, teacher_id):
        self.get_and_save_teacher_info(soup, teacher_id)
        self.get_and_save_class_info(soup, teacher_id)
        self.get_and_save_comment_info(soup, teacher_id)
        pass

    def get_and_save_teacher_info(self, soup, teacher_id):
        location = soup.find('h3')
        if location is None:
            return
        teacher_info = location.parent
        teacher_name = teacher_info.h3.string
        info_table = teacher_info.find_all('p')
        rate = info_table[0].string
        rate_num = info_table[1].string
        faculty = info_table[2].string
        self.c.execute("INSERT INTO TEACHER_TABLE (TEACHER_ID, TEACHER_NAME, RATE, RATE_NUM, FACULTY)\
                            values ({},'{}','{}','{}','{}')".format(teacher_id, teacher_name, rate, rate_num, faculty))
        # TODO: might deal with out of range issue here

    def get_and_save_class_info(self, soup, teacher_id):
        class_table = soup.find("table")
        if class_table is None:
            return
        # TODO: right here!!! class table not exist but comment table exit, WTF?, find by "h4" i think
        entry_list = class_table.tbody.find_all('tr')
        for entry in entry_list:
            values = entry.find_all('td')
            class_name, class_gpa = values[0], values[1]
            self.c.execute("INSERT INTO CLASS_TABLE (TEACHER_ID, CLASS_NAME, CLASS_GPA)\
                            values ({},'{}','{}')".format(teacher_id, class_name.string, class_gpa.string))

    def get_and_save_comment_info(self, soup, teacher_id):
        tables = soup.find_all("table")
        # TODO: also here!!! class table not exist but comment table exit, WTF?, find by "h4" i think
        if tables is None:
            return
        if len(tables) == 3:
            comment_table = soup.find_all("table")[1]
        else:
            return

        entry_list = comment_table.tbody.find_all('tr')
        for entry in entry_list:
            items = entry.find_all('td')
            if len(items) != 3:
                return
            comment_time = items[0].string
            comment = self.sqliteEscape(items[1].string)
            approve_num = items[2].div.string
            # print("INSERT INTO COMMENT_TABLE (TEACHER_ID, COMMENT_TIME, CONTENT, APPROVE_NUM)\
            #                 values ({},'{}','{}',{})".format(teacher_id, comment_time, comment[:5], approve_num))
            self.c.execute("INSERT INTO COMMENT_TABLE (TEACHER_ID, COMMENT_TIME, CONTENT, APPROVE_NUM)\
                            values ({},'{}','{}',{})".format(teacher_id, comment_time, comment, approve_num))

    @staticmethod
    def sqliteEscape(keyWord):
        if keyWord:
            keyWord = keyWord.replace("/", "//")
            keyWord = keyWord.replace("'", "''")
            keyWord = keyWord.replace("[", "/[")
            keyWord = keyWord.replace("]", "/]")
            keyWord = keyWord.replace("%", "/%")
            keyWord = keyWord.replace("&", "/&")
            keyWord = keyWord.replace("_", "/_")
            keyWord = keyWord.replace("(", "/(")
            keyWord = keyWord.replace(")", "/)")
            keyWord = keyWord.replace("^", "/^")
            keyWord = keyWord.replace(")", "/)")
        return keyWord
