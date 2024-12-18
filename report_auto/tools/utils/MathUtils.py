#!/usr/bin/env python
# @desc : 
__coding__ = "utf-8"
__author__ = "xxx team"

import numpy as np


# 数字x除以1000，结果截取小数点后一位
def truncate_to_one_decimal_place(x) -> float:
    if x < 10:
        s = f"{x}"
    else:
        # 将数字转换为字符串，并确保它至少有一位小数
        s = f"{x / 1000:.2f}"

    # 截取小数点后的一位数字
    truncated = float(s[:s.index('.') + 2])
    return truncated


def scale_and_truncate(x, max_value):
    if max_value >= 1000:
        x = x / 1000  # 如果最大值大于等于1000，则缩放
    return round(x, 1)  # 保留整数


# bit4,二进制的第4位
def getBit4(decimal_number: np.float64) -> str:
    # 取整数部分
    integer_part = int(np.floor(decimal_number))

    # 将整数部分转换为二进制并去除前缀 '0b'
    binary_representation = bin(integer_part)[2:]

    # 如果二进制表示不足5位，则补0
    binary_representation = binary_representation.zfill(5)

    # 获取第5位的值（从右到左计数）
    fifth_bit = binary_representation[4]  # 修正索引为4，因为Python索引从0开始

    return str(fifth_bit)


# bit4,二进制的第5位
def get_fifth_bit(decimal_number: int) -> str:
    binary_str = bin(decimal_number)[2:].zfill(5)

    # 从右边开始获取第5位（bit4），即索引为4的位置
    if len(binary_str) > 4:
        return binary_str[-5]
    else:
        return '0'  # 如果二进制字符串不足5位，则返回'0'


# bit2,二进制的第3位
def get_third_bit(decimal_number: int) -> str:
    binary_str = bin(decimal_number)[2:].zfill(3)

    # 从右边开始获取第3位（bit2），即索引为2的位置
    if len(binary_str) > 2:
        return binary_str[-3]
    else:
        return '0'  # 如果二进制字符串不足3位，则返回'0'


# bit2，二进制的第3位
def getBit2(decimal_number: np.float64) -> str:
    # 取整数部分
    integer_part = int(np.floor(decimal_number))

    # 将整数部分转换为二进制并去除前缀 '0b'
    binary_representation = bin(integer_part)[2:]

    # 如果二进制表示不足3位，则补0
    binary_representation = binary_representation.zfill(3)

    # 获取第2位的值（从右到左计数）
    second_bit = binary_representation[-3]

    return str(second_bit)


# bit0, 二进制的第0位
def getBit0(decimal_number: int) -> str:
    # 将十进制数转换为二进制字符串，并去掉前缀 "0b"
    binary_string = bin(decimal_number)[2:]

    # 返回二进制字符串的最低位（即最后一位）
    return binary_string[-1]


# 相对差值
def relative_difference_chip(num1: float, num2: float) -> int:
    if num1 == 0.0 and num2 != 0:
        return num2
    elif num1 == 0.0:
        return num1

    if num2 is None:
        num2 = 0

    r_num = (num1 - num2) / num1
    r_num_percentage = round(r_num * 100, 2)
    return abs(int(r_num_percentage))


# 差值
def difference_chip(num1: float, num2: float) -> int:
    if num2 is None:
        num2 = 0
    r_num = (num1 - num2)
    return int(r_num)

# 测试函数
# values = [40, 111, 168, 251, 252]
# for value in values:
#     print(f"十进制数 {value} : {get_third_bit(value)}")
