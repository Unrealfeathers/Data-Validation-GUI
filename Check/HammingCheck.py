"""
* Author: Unrealfeathers
* coding: utf-8
* Create time: 2023-09-18 16：00
* Function Explain: 本模块包含汉明码校验的实现
"""
import Check.utils as utils
import Check.ParityCheck as ParityCheck


def get_check_bits_num(data_bits: int) -> int:
    """
    获取海明码校验位数
    :param data_bits: 二进制数据位数
    :return: 校验位数
    """
    check_bits = 1  # 校验位数
    while data_bits > (2 ** check_bits - check_bits - 1):
        check_bits += 1
    return check_bits


def generate_checked_bin(bin_str: str, mode: str) -> str:
    """
    生成海明码校验位，返回加入校验位的二进制字符串
    :param bin_str: 二进制数据字符串
    :param mode: ‘odd’-奇数校验；‘even’偶数校验
    :return: 二进制字符串
    """
    # 检测输入是否为标准二进制字符串
    if not utils.is_standard_bin(bin_str):
        raise ValueError("输入错误, 仅支持标准二进制字符串！")
    # 检测校验模式是否正确
    if mode != "odd" and mode != "even":
        ValueError("输入的校验模式有误！")
    # 将二进制字符串转换为列表
    bin_list = list(bin_str)
    length = len(bin_list)

    # 获取校验位位数
    check_bits = get_check_bits_num(length)
    # 将校验位插入列表
    for num in range(0, check_bits):
        index = 2 ** num - 1
        bin_list.insert(index, -1)
    length = len(bin_list)

    # 根据模式进行分类校验
    # 遍历检验组：第n组,从第(2^n)-1位开始，储存2^n位，再隔2^n位，再储存2^n位，直到遍历完整个字符串
    for num in range(0, check_bits):
        xor_list = []  # 子校验组储存列表
        start_index = 2 ** num - 1  # 子检查组的起始位
        check_num = 2 ** num  # 子检查组的的位数
        step = 2 ** (num + 1)  # 第一次遍历时的步长

        # 第一次遍历：从第(2^n)-1位开始，获得下一个隔2^n位的子检查组的index，实际间隔是2^(n+1)
        for index in range(start_index, length, step):
            # 第二次遍历：从每个子检查组的起始位开始，储存2^n位
            for i in range(0, check_num):
                if index + i >= length:
                    break
                else:
                    xor_list.append(str(bin_list[index + i]))
        # 使用偶数校验获得校验位的值
        check_bit = ParityCheck.generate_parity_check_digit("".join(xor_list[1:]), mode=mode)
        # 将对应校验位的值进行替换
        bin_list[start_index] = check_bit

    return "".join(bin_list)


def hamming_check(bin_str: str, mode: str) -> list:
    """
    对海明码进行校验，返回列表，第一个元素为True/False，第二个元素为错误位置,第三个元素为纠错结果
    :param bin_str: 二进制字符串，包含海明码和校验位
    :param mode: 'odd'-奇数校验；'even'偶数校验
    :return: 错误位置列表，如果没有错误，返回空列表
    """
    # 检测输入是否为标准二进制字符串
    if not utils.is_standard_bin(bin_str):
        raise ValueError("输入错误, 仅支持标准二进制字符串！")
    # 检测校验模式是否正确
    if mode != "odd" and mode != "even":
        ValueError("输入的校验模式有误！")
    # 获取二进制字符串长度
    bin_list = list(bin_str)
    length = len(bin_str)

    # 获取校验位数
    data_bits = 1
    while data_bits + get_check_bits_num(data_bits) != length:
        data_bits += 1
    check_bits = get_check_bits_num(data_bits)

    # 获取校验位
    data_bits_list = []  # 存储校验位
    for num in range(0, check_bits):
        index = 2 ** num - 1
        value = bin_str[index]
        data_bits_list.append(value)

    # 根据校验位判断是否有错误
    G_list = []
    error_positions = []  # 错误位置
    # 遍历检验组：第n组,从第(2^n)-1位开始，检查2^n位，再隔2^n位，再检查2^n位，直到检查完整个字符串
    for num in range(0, check_bits):
        xor_list = []  # 子校验组储存列表
        start_index = 2 ** num - 1  # 子检查组的起始位
        check_num = 2 ** num  # 子检查组的的位数
        step = 2 ** (num + 1)  # 第一次遍历时的步长

        # 第一次循环：从第(2^n)-1位开始，获得下一个隔2^n位的子检查组的index，实际间隔是2^(n+1)
        for index in range(start_index, length, step):
            # 第二次循环：从每个子检查组的起始位开始，检查2^n位
            for i in range(0, check_num):
                if index + i >= length:
                    break
                else:
                    xor_list.append(str(bin_list[index + i]))
        # 使用偶数校验获得子校验位的校验值
        check_bit = ParityCheck.generate_parity_check_digit("".join(xor_list), mode=mode)
        # 按照G2-G1-G0的顺序，将校验值插入列表
        G_list.insert(0, check_bit)
    # 将错误数据位的位置由二进制转换为十进制
    position = int("".join(G_list), 2)
    if position != 0:
        # 添加校验结果
        error_positions.append(False)
        # 添加错误位下标
        error_positions.append(position)
        # 添加纠错结果
        bin_list = list(bin_str)
        if bin_list[position - 1] == "0":
            bin_list[position - 1] = "1"
        else:
            bin_list[position - 1] = "0"
        error_positions.append("".join(bin_list))
        return error_positions
    else:
        error_positions.append(True)
        # 添加错误位下标
        error_positions.append(None)
        # 添加纠错结果
        error_positions.append(None)
        return error_positions


if __name__ == '__main__':
    binary = "0111011011"  # 假设这是一个经过海明码编码的字符串
    checked_bin = generate_checked_bin(binary, "odd")
    print("源数据：{},海明码:{}".format(binary, checked_bin))

    checked_bin = "1011011"
    results = hamming_check(checked_bin, "odd")
    print("海明码:{},校验结果:{},错误位置:{},纠错结果:{}".format(checked_bin, results[0], results[1], results[2]))
