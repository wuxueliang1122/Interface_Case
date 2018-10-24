# coding=utf-8


class GlobalVar:
    global_dic = {}

    def __init__(self):
        global global_dic

    @ staticmethod
    def set_global_dic():
        global global_dic

    @ staticmethod
    def get_global_dic():
        global global_dic
        try:
            return global_dic
        except TypeError:
            return False



