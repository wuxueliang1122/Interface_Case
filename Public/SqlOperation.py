# coding=utf-8

import pymysql


class SqlOperation:

    def __init__(self):
        self.host = '10.10.13.94'
        self.port = 3306
        self.user = 'devuser'
        self.password = 'devuser'

        try:
            # 连接数据库
            self.connection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                              charset='gbk')
            # 获取游标
            self.cursor = self.connection.cursor()
        except ConnectionError:
            print("Failed to Connect DB.")

    def close(self):
        self.cursor.close()
        self.connection.close()

    def insert_data(self, sql):
        """
        插入数据
        :param sql: sql语句，如"INSERT INTO trade (name, account, saving) VALUES ('王二狗', '13512345678', 10000)"
        :return:
        """
        # noinspection PyBroadException
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.connection.rollback()
            print("数据插入失败", e)
        else:
            self.connection.commit()
            print("数据插入成功")

    def update_data(self, sql):
        """
        修改数据
        :param sql:
        :return:
        """
        # noinspection PyBroadException
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.connection.rollback()
            print("数据修改失败", e)
        else:
            self.connection.commit()
            print("数据修改成功")

    def select_data(self, sql):
        """
        查询数据
        :param sql:
        :return:返回一行
        """
        # noinspection PyBroadException
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.connection.rollback()
            print("数据查询失败", e)
        else:
            self.connection.commit()
            print("数据查询成功")
            return self.cursor.fetchone()

    def select_data_all(self, sql):
        """
        查询数据
        :param sql:
        :return:返回所有符合查询条件的行
        """
        # noinspection PyBroadException
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.connection.rollback()
            print("数据查询失败", e)
        else:
            self.connection.commit()
            print("数据查询成功")
            return self.cursor.fetchall()

    def delete_data(self, sql):
        # noinspection PyBroadException
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.connection.rollback()
            print("数据删除失败", e)
        else:
            self.connection.commit()
            print("数据删除成功.")


if __name__ == '__main__':
    pass
