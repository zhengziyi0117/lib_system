from ctypes import create_unicode_buffer
from os import lstat
from sqlite3 import Cursor
import pymysql


class SqlApi(object):
    """
    a class provides apis to gui
    """

    def __init__(self) -> None:
        """
        connect mysql and create cursor to execute sql
        """
        # 数据库连接,根据本地mysql数据库实际修改
        self.db = pymysql.connect(host="localhost", user="root", passwd="1111", database="libarary_system")
        # 创建游标对象,给后面方法使用
        self.cursor = self.db.cursor()
        # # 创建books表和user表,可以用sql文件代替
        # create_table_books = """CREATE TABLE `books`(
        #                         `bid` int NOT NULL AUTO_INCREMENT,
        #                         `bookname` varchar(255) NOT NULL,
        #                         PRIMARY KEY (`bid`)
        #                         );"""
        # create_table_user = """CREATE TABLE `user`(
        #                        `id` int NOT NULL AUTO_INCREMENT,
        #                        `username` varchar(255) NOT NULL,
        #                        `bookid` int NOT NULL DEFAULT 1,
        #                        PRIMARY KEY (`id`)
        #                        );"""
        # self.cursor.execute(create_table_books)
        # self.cursor.execute(create_table_user)
        # self.cursor.execute("ALTER TABLE `books` AUTO_INCREMENT=2")

    # sql语句函数，便于重复调用
    def __select_person_num_by_bookid(self, bookid: int):
        self.cursor.execute("SELECT count(*) FROM `user` WHERE `bookid` = {}".format(bookid))
        tup = self.cursor.fetchall()
        return tup[0][0]

    def __select_book_num_by_bookid(self, bookid: int):
        self.cursor.execute("SELECT count(*) FROM `books` WHERE `bid` = {}".format(bookid))
        tup = self.cursor.fetchall()
        return tup[0][0]

    def __select_bookid_by_username(self, username: str) -> int:
        self.cursor.execute("SELECT `bookid` FROM `user` WHERE `username` = '{}'".format(username))
        tup = self.cursor.fetchall()
        if tup:
            try:
                return tup[0][0]
            except IndexError:
                print("不存在该书")

    def register(self, name: str):
        """
        register

        You must register before borrow books
        """
        person = self.cursor.execute("SELECT count(*) FROM `user` WHERE `username` = '{}'".format(name))
        if person:
            print("您已注册")
        else:
            self.cursor.execute("INSERT INTO `user` (`username`, `bookid`) VALUES ('{}', 1)".format(name))
            print("注册成功")

    def query_books(self, bookname: str):
        """
        search books from the database

        :param: - bookname part of the book's name that you want to search
        :return: a book tuple (tuple[tuple[Any, ...], ...]) that contains bookname and bookid
        """
        if bookname is None:
            print("书名不能为空")
        # 预防sql注入
        if "--" in bookname or "or" in bookname:
            print("请重新输入")
        self.cursor.execute("SELECT * FROM `books` WHERE `bookname` LIKE '%{}%'".format(bookname))
        books = self.cursor.fetchall()
        if len(books) == 0:
            print("抱歉为找到您想要的书")
        print(books)

    def borrow_book(self, username: str, bookid: int):
        """
        borrow book

        :param: - username book borrower
        :param: - bookid bookid query from the query api
        """
        # 预防sql注入
        if not isinstance(bookid, int):
            print("请输入一个int")
        # 预防sql注入
        if "--" in username or "or" in username:
            print("请重新输入")
        book_num = self.__select_book_num_by_bookid(bookid)
        person_num = self.__select_person_num_by_bookid(bookid)
        bookid_person_has = self.__select_bookid_by_username(username)

        if bookid_person_has and bookid_person_has > 1:
            print("一个人只能借一本书哦")
        if not book_num or bookid == 1:
            print("输入bookid不存在,请重新输入")
        if person_num:
            print("抱歉该书已被他人借走")
        else:
            self.cursor.execute("UPDATE `user` SET `bookid` = {} WHERE `username` = '{}'".format(bookid, username))
            self.db.commit()
            book = self.__select_bookid_by_username(username)
            if book != 1:
                print("借书成功,请30天内归还")
            else:
                print("借书失败,请联系管理员")

    def return_book(self, username: str):
        """
        give back book

        :param: - username the book returner
        """
        # 预防sql注入
        if "--" in username or "or" in username:
            print("请重新输入")

        self.cursor.execute("UPDATE `user` SET `bookid` = 1 WHERE username = '{}'".format(username))
        self.db.commit()
        if self.__select_bookid_by_username(username) == 1:
            print("还书成功")
        else:
            print("还书失败,请联系管理员")

    def close(self):
        self.cursor.close()
        self.db.close()


# 调用示例,注意调用完后调用close方法关闭连接
# sqlApi = SqlApi()
# sqlApi.return_book("小芳")
# sqlApi.close()


