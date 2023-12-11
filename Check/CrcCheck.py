"""
* Author: 史浩然-物联网213-215256
* coding: utf-8
* Create time: 2023-11-14 16：38
* Function Explain: 本模块包含CRC校验的实现
"""
import random


def generate_polynomial(bin_bits: int) -> str:
    """
    生成CRC多项式，返回二进制数据字符串
    :param bin_bits: 生成二进制字符串的位数
    :return: 二进制数据字符串
    """
    bin_bits = bin_bits - 2
    polynomial = "1" + bin(random.randint(0, 2 ** bin_bits - 1))[2:-1].zfill(bin_bits) + "1"
    return polynomial


def generate_crc_check_digit(binary_data: str, polynomial: str) -> str:
    """
    生成CRC校验位，返回二进制数据字符串
    :param binary_data: 二进制数据字符串
    :param polynomial: CRC多项式
    :return: 二进制数据字符串
    """
    remainder = binary_division(binary_data, polynomial)
    remainder = remainder.zfill(len(polynomial) - 1)
    return remainder


def binary_division(dividend: str, divisor: str) -> str:
    """
    模二 除法
    :param dividend: 被除数
    :param divisor: 除数
    :return: 余数
    """
    # 将被除数和除数转换为列表
    dividend = list(dividend)
    divisor = list(divisor)
    # 将被除数的二进制表示左移R位
    for i in range(len(divisor) - 1):
        dividend.append('0')
    # 依次异或被除数和除数的二进制表示的每一位
    while True:
        # 去除被除数前面的0
        while True:
            if len(dividend) == 0:
                break
            elif dividend[0] == '0':
                dividend.pop(0)
            elif dividend[0] == '1':
                break
        # 判断被除数剩余位数是否小于除数位数
        if len(dividend) < len(divisor):
            return "".join(dividend)
        # 依次异或被除数和除数的二进制表示的每一位
        for i in range(len(divisor)):
            if dividend[i] == divisor[i]:
                dividend[i] = '0'
            else:
                dividend[i] = '1'


def crc_check(binary_data: str, polynomial: str) -> str:
    """
    CRC校验，返回校验结果
    :param binary_data: 二进制数据字符串
    :param polynomial: CRC多项式
    :return: 二进制数据字符串，若校验成功则返回0，否则返回余数
    """
    remainder = binary_division(binary_data, polynomial)
    if len(remainder) == 0:
        return "0"
    else:
        return remainder
