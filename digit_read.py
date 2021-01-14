# coding=utf-8
import sys

# str = input()
# print(str)
import re

class digit_reader:
    """
    read the digit under 10^12 in Chinuse way
    1 split an integer every four digits from the tail by str indexing, to loop it as a 4 digits number.
    2 pad every cut if the cut is shorter than 4 digits.
    3 read the 4-digit number in a full way
    4 collapse the reading result in case it contains 零万-style parts and the heading/tailing 零。
    """
    def __init__(self):
        self.dict_10 = {str(key): value for key, value in zip(range(10), ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'])}
        self.units = ['兆', '亿', '万', '']

    def split(self, x):
        """
        split long number every 4 digits from the tail. Adding the tailing '@' to facilitate the indexing
        x='1234567890'
        x+='@''
        cut =  ['12','3456','7890']
        units = ['亿','万','']
        :param x: int
        :return: str
        """
        x = str(x)
        x += '@'
        cut = [x[-i - 4:-i] for i in range(1, len(list(x)), 4)]
        cut.reverse()
        units = self.units[-len(cut):]

        return cut, units


    def pad_4(self, x):
        """
        pad number under 10000 into a 4-digit number, to facilitate indexing and standard ops.
        :param x: int
        :return: str
        """
        l = len(list(str(x)))
        if l >= 4:
            x = str(x)
        else:
            x = '0' * (4 - l) + str(x)
        return x


    def read_4_digit(self, x):
        """
        read 4-digit number
        x=1234
        read_x='一千二百三十四'
        x=12
        read_x = '零千零百一十二'
        :param x: ini
        :return: str
        """
        x = self.pad_4(x)
        x_list = list(x)
        digit_read = [self.dict_10.get(i) for i in x_list]
        read_x = ('{0[0]}' + '千' + '{0[1]}' + '百' + '{0[2]}' + '十' + '{0[3]}').format(digit_read)

        return read_x


    def read_full(self, x):
        """
        read long number in a full and exhaustive way
        :param x: int
        :return: str
        """
        cut, units = self.split(x)
        read_result = ''.join([self.read_4_digit(c) + u for c, u in zip(cut, units)])

        return read_result

    def read_compact(self, x):
        """
        solve some corner cases.
        :param x: int
        :return: str
        """
        result = self.read_full(x)
        result = re.sub('零[千百十]{1}', '零', result) # 零十，零百，零千 should be 零
        result = re.sub(r'零*([兆亿万]{1})', r'\1', result) # splitting unit should not be appended with 零
        result = re.sub('零+','零',result) # repeated 零 from multiple source should be only one
        result = re.sub('^零|零$','',result) # trim heading and tailing 零
        result = re.sub('^一十','十',result) # special case for 10-19. No heading 一
        return result


def main():
    input=2,10,12,22, 1001, 10000000,10000010, 10000001,1010101,1234567890
    reader=digit_reader()
    _ = [print('='*20+'\n'+
               'question:'+str(i)+'\n'+
               reader.read_full(i)+'\n'+
               'answer:'+reader.read_compact(i)) for i in input]


if __name__=='__main__':
    main()







