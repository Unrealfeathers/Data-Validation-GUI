"""
* Author: Unrealfeathers
* coding: utf-8
* Create time: 2023-09-18 16：00
* Function Explain: 本模块包含一些通用的工具函数
"""
import random


def generate_data(bin_bits: int, bin_number: int) -> list:
    """
    生成二进制字符串，返回二进制字符串列表
    :param bin_bits: 生成二进制字符串的位数
    :param bin_number: 生成二进制字符串的个数
    :return: 返回二进制字符串列表
    """
    num_list = []
    for i in range(bin_number):
        binary_data = bin(random.randint(0, 2 ** bin_bits - 1))
        num_list.append(binary_data[2:-1].zfill(bin_bits))
    return num_list


def is_standard_bin(bin_str) -> bool:
    """
    判断是否为标准二进制字符串
    :param bin_str: 二进制字符串
    :return: True/False
    """
    return bin_str.count('1') + bin_str.count('0') == len(bin_str)


def interference_simulation(binary_data: str, interference_intensity: int) -> str:
    """
    对传入的二进制字符串进行模拟干扰，返回干扰后的二进制字符串
    :param binary_data: 二进制字符串
    :param interference_intensity: 干扰强度，0-100
    :return: 二进制字符串
    """
    # 随机生成一个0-100的数
    flag = random.randint(0, 100)
    # 随机生成一个数据的位数
    index = random.randint(0, len(binary_data) - 1)
    # 将字符串转换为列表
    binary_list = list(binary_data)
    # 将列表中的某一位取反
    if flag < interference_intensity:
        if binary_list[index] == '0':
            binary_list[index] = '1'
        else:
            binary_list[index] = '0'
    # 将列表转换为字符串并返回
    return "".join(binary_list)
