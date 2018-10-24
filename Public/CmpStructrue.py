# coding=utf-8

import operator
import types


class CmpStructrue:
    """
    比较data的格式，以及data内容的字段
    """

    def cmp_object(self, d1, d2):
        if type(d1) != type(d2):
            print("type is not equal")
            return False
        if type(d2) == dict:
            # print("dict: {}".format(d2))
            return self.cmp_dict(d1, d2)
        elif type(d2) == (list, tuple):
            # print("{}: {}".format(type(d2), d2))
            return self.cmp_list(d1, d2)
        else:
            return True

    def cmp_dict(self, dict1, dict2):
        if len(dict1) != len(dict2):
            # print("length is not same.{}:{}".format(len(dict1), len(dict2)))
            return False
        else:
            for k in dict1.keys():
                # print("key", k)
                if k not in dict2.keys() or not self.cmp_object(dict1[k], dict2[k]) and dict1[k] != dict2[k]:
                    return False
        return True

    def cmp_list(self, lst1, lst2):
        for i in range(0, min(len(lst1), len(lst2))):
            if not self.cmp_object(lst1[i], lst2[i]):
                return False
        if len(lst1) == len(lst2):
            return True
        # 后续元素的类型必须相同
        if len(lst1) > len(lst2):
            last_e = lst1[max(len(lst2) - 1, 0)]
            for i in range(len(lst2), len(lst1)):
                if not self.cmp_object(last_e, lst1[i]):
                    return False
        else:
            last_e = lst2[max(len(lst1) - 1, 0)]
            for i in range(len(lst1), len(lst2)):
                if not self.cmp_object(last_e, lst2[i]):
                    return False
        return True


if __name__ == '__main__':
    o1 = {'respcd': '0000', 'respmsg': 'caller error', 'data': {}}
    o2 = {'respcd': '', 'respmsg': '', 'data': {}}
    print(CmpStructrue().cmp_object(o1, o2))
