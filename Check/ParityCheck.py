"""
* Author: Unrealfeathers
* coding: utf-8
* Create time: 2023-09-18 16：00
* Function Explain: 本模块包含奇偶校验的实现
"""


def generate_parity_check_digit(binary_data: str, mode: str) -> str:
    """
    生成奇偶校验位，返回二进制数据字符串列表
    :param binary_data: 二进制数据字符串
    :param mode: ‘odd’-奇数校验；‘even’偶数校验
    :return: 二进制数据字符串
    """
    count = binary_data.count("1")
    # 奇数校验
    if mode == 'odd':
        if count % 2 == 1:
            return "0"
        else:
            return "1"
    # 偶数校验
    elif mode == 'even':
        if count % 2 == 0:
            return "0"
        else:
            return "1"
    else:
        raise ValueError('不支持此模式，仅支持 odd:奇数校验/even:偶数校验')


def parity_check(binary_data: str, mode: str) -> bool:
    """
    对二进制数据字符串进行奇偶校验，返回校验结果
    :param binary_data: 二进制数据字符串
    :param mode: ‘odd’-奇数校验；‘even’偶数校验
    :return: 二进制数据字符串
    """
    count = binary_data.count('1')
    # 奇数校验
    if mode == 'odd':
        if count % 2 == 1:
            return True
        else:
            return False
    # 偶数校验
    elif mode == 'even':
        if count % 2 == 0:
            return True
        else:
            return False
    else:
        raise ValueError('不支持此模式，仅支持 odd:奇数校验/even:偶数校验')
