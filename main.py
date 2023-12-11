import tkinter as tk
from tkinter import ttk

from Check import ParityCheck
from Check import CrcCheck
from Check import HammingCheck
from Check import utils

parity_check_mode = "odd"
hamming_check_mode = "even"


class RFID:
    polynomial = ""  # CRC生成多项式

    def __init__(self, window: tk.Tk) -> None:
        window = window
        # 设置窗口大小和位置
        # window.geometry('800x600')
        # 设置窗口标题
        window.title('RFID数据校验')
        # 设置窗口图标
        # self.window.iconbitmap('path/to/icon')
        # 设置窗口背景颜色
        window.config(bg='#FFFFFF')

        # 创建顶部按键框架
        frame_top = tk.Frame(window, bg='#FFFFFF')
        frame_top.grid(row=0, column=0)
        # 创建底部框架
        frame_bottom = tk.Frame(window, bg='#FFFFFF')
        frame_bottom.grid(row=1, column=0)

        # 创建顶部按键界面
        self.__frame_top_button(frame_top, frame_bottom)

    def __frame_top_button(self, frame_top: tk.Frame, frame_bottom: tk.Frame) -> None:
        # 创建三个按钮
        button_parity_check = tk.Button(frame_top, text='奇偶校验', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                        command=lambda: self.__frame_parity_check(frame_bottom))
        button_parity_check.grid(row=0, column=0, padx=10, pady=10)

        button_crc_check = tk.Button(frame_top, text='CRC冗余校验', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                     command=lambda: self.__frame_crc_check(frame_bottom))
        button_crc_check.grid(row=0, column=2, padx=10, pady=10)

        button_hamming_check = tk.Button(frame_top, text='海明码校验', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                         command=lambda: self.__frame_hamming_check(frame_bottom))
        button_hamming_check.grid(row=0, column=4, padx=10, pady=10)

    def __frame_parity_check(self, frame_bottom: tk.Frame) -> None:
        # 清除框架内的内容
        for widget in frame_bottom.winfo_children():
            widget.destroy()
        # 创建内容框架
        frame_content = tk.Frame(frame_bottom, bg='#FFFFFF')
        frame_content.grid(row=0, column=0)

        # 创建数据展示框架
        frame_show = tk.LabelFrame(frame_content, text="数据展示", labelanchor="n", bg='#FFFFFF')
        frame_show.grid(row=0, column=0)
        # 创建发送框架
        frame_send = tk.LabelFrame(frame_show, text="发送数据", labelanchor="n", bg='#FFFFFF')
        frame_send.grid(row=0, column=0)
        # 创建接收框架
        frame_receive = tk.LabelFrame(frame_show, text="接收数据", labelanchor="n", bg='#FFFFFF')
        frame_receive.grid(row=0, column=1)

        # 创建按钮框架
        frame_enter = tk.Frame(frame_content, bg='#FFFFFF')
        frame_enter.grid(row=1, column=0)
        # 创建结果框架
        frame_result = tk.LabelFrame(frame_content, text="结果", labelanchor="n", bg='#ffFFFF')
        frame_result.grid(row=2, column=0)

        # 创建treeview发送窗口
        columns_send = ['序号', '数据位', '校验位']
        table_send = ttk.Treeview(
            master=frame_send,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=columns_send,  # 显示的列
            show='headings',  # 隐藏首列
        )
        table_send.heading(column='序号', text='序号', anchor='w')
        table_send.heading(column='数据位', text='数据位', anchor='w')  # 定义表头
        table_send.heading(column='校验位', text='校验位', anchor='w')  # 定义表头
        table_send.column(column='序号', width=50, anchor='w')  # 定义列
        table_send.column(column='数据位', width=100, anchor='w')  # 定义列
        table_send.column(column='校验位', width=50, anchor='w')  # 定义列
        table_send.grid(row=0, column=0, sticky='w')
        # 为table_send添加垂直滚动条
        scrollbar_send = tk.Scrollbar(frame_send, orient=tk.VERTICAL)
        scrollbar_send.grid(row=0, column=1, sticky='ns')
        table_send.config(yscrollcommand=scrollbar_send.set)
        scrollbar_send.config(command=table_send.yview)

        # 创建treeview接受窗口
        columns_receive = ['序号', '数据位', '接收校验位', '计算校验位']
        table_receive = ttk.Treeview(
            master=frame_receive,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=columns_receive,  # 显示的列
            show='headings',  # 隐藏首列
        )
        table_receive.heading(column='序号', text='序号', anchor='w')
        table_receive.heading(column='数据位', text='数据位', anchor='w')  # 定义表头
        table_receive.heading(column='接收校验位', text='接收校验位', anchor='w')
        table_receive.heading(column='计算校验位', text='计算校验位', anchor='w')
        table_receive.column(column='序号', width=50, anchor='w')  # 定义列
        table_receive.column(column='数据位', width=100, anchor='w')
        table_receive.column(column='接收校验位', width=80, anchor='w')
        table_receive.column(column='计算校验位', width=80, anchor='w')
        table_receive.grid(row=0, column=0, sticky='w')
        # 为table_receive添加垂直滚动条
        scrollbar_receive = tk.Scrollbar(frame_receive, orient=tk.VERTICAL)
        scrollbar_receive.grid(row=0, column=1, sticky='ns')
        table_receive.config(yscrollcommand=scrollbar_receive.set)
        scrollbar_receive.config(command=table_receive.yview)

        # 创建两个按钮
        button_send = tk.Button(frame_enter, text='发送数据', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                command=lambda: self.__send_data_parity(table_send))
        button_send.grid(row=0, column=0, padx=100, pady=10)
        button_receive = tk.Button(frame_enter, text='接收数据', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                   command=lambda: self.__receive_data_parity(table_receive, table_send,
                                                                              frame_result))
        button_receive.grid(row=0, column=1, padx=100, pady=10)

    def __send_data_parity(self, table: ttk.Treeview) -> None:
        # table初始化
        self.__delete(table)
        for index, binary_data in enumerate(utils.generate_data(8, 100)):
            check_digit = ParityCheck.generate_parity_check_digit(binary_data, mode=parity_check_mode)
            data = [str(index), binary_data, check_digit]
            table.insert('', tk.END, values=data)

    def __receive_data_parity(self, table_receive: ttk.Treeview, table_send: ttk.Treeview,
                              frame_end: tk.LabelFrame) -> None:
        # 数据统计
        all_count = len(table_send.get_children())  # 总共数据条数
        error_count = 0  # 错误数据条数
        error_miss_count = 0  # 未找到错误数据条数
        # table初始化
        self.__delete(table_receive)
        # 设置三种标签
        table_receive.tag_configure('error_data', foreground='blue')
        table_receive.tag_configure('error_checked', foreground='red')
        table_receive.tag_configure('error_miss', foreground='green')
        # 插入并校验数据
        obj = table_send.get_children()
        for item in obj:
            # 对数据进行模拟干扰
            send_data = list(table_send.item(item, 'values'))
            receive_data = list(table_send.item(item, 'values'))
            receive_data[1] = utils.interference_simulation(receive_data[1], 10)
            # 根据数据计算校验位
            check_digit = ParityCheck.generate_parity_check_digit(receive_data[1], 'odd')
            receive_data.append(check_digit)
            # 插入数据并给错误数据打上标签
            table_receive.insert('', tk.END, values=receive_data)
            if receive_data[1] != send_data[1]:
                error_count += 1
                table_receive.item(item, tags=("error_data",))
                if send_data[-1] != receive_data[-1]:
                    table_receive.item(item, tags=("error_checked",))
                elif send_data[-1] != receive_data[-1]:
                    error_miss_count += 1
                    table_receive.item(item, tags=("error_miss",))
        # 输出数据传输结果
        text = tk.Text(frame_end, height=6, bg='#FFFFFF', fg='#000000')
        text.grid(row=0, column=0, sticky='w')
        text.insert(tk.END, f'总共{all_count}条数据\n')
        text.insert(tk.END, f'错误{error_count}条数据\n')
        text.insert(tk.END, f'未找到{error_miss_count}条数据\n')
        # 输出传输错误率,保留两位小数
        text.insert(tk.END, f'传输错误率{(error_count / all_count * 100):.2f}%\n')

    def __frame_crc_check(self, frame_bottom: tk.Frame) -> None:
        # 清除框架内的内容
        for widget in frame_bottom.winfo_children():
            widget.destroy()
        # 创建内容框架
        frame_content = tk.Frame(frame_bottom, bg='#FFFFFF')
        frame_content.grid(row=0, column=0)

        # 创建数据展示框架
        frame_show = tk.LabelFrame(frame_content, text="数据展示", labelanchor="n", bg='#FFFFFF')
        frame_show.grid(row=0, column=0)
        # 创建发送框架
        frame_send = tk.LabelFrame(frame_show, text="发送数据", labelanchor="n", bg='#FFFFFF')
        frame_send.grid(row=0, column=0)
        # 创建接收框架
        frame_receive = tk.LabelFrame(frame_show, text="接收数据", labelanchor="n", bg='#FFFFFF')
        frame_receive.grid(row=0, column=1)

        # 创建按钮框架
        frame_enter = tk.Frame(frame_content, bg='#FFFFFF')
        frame_enter.grid(row=1, column=0)
        # 创建结果框架
        frame_result = tk.LabelFrame(frame_content, text="结果", labelanchor="n", bg='#ffFFFF')
        frame_result.grid(row=2, column=0)

        # 创建treeview发送窗口
        columns_send = ['序号', '数据位', '校验位']
        table_send = ttk.Treeview(
            master=frame_send,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=columns_send,  # 显示的列
            show='headings',  # 隐藏首列
        )
        table_send.heading(column='序号', text='序号', anchor='w')
        table_send.heading(column='数据位', text='数据位', anchor='w')  # 定义表头
        table_send.heading(column='校验位', text='校验位', anchor='w')  # 定义表头
        table_send.column(column='序号', width=50, anchor='w')  # 定义列
        table_send.column(column='数据位', width=100, anchor='w')  # 定义列
        table_send.column(column='校验位', width=50, anchor='w')  # 定义列
        table_send.grid(row=0, column=0, sticky='w')
        # 为table_send添加垂直滚动条
        scrollbar_send = tk.Scrollbar(frame_send, orient=tk.VERTICAL)
        scrollbar_send.grid(row=0, column=1, sticky='ns')
        table_send.config(yscrollcommand=scrollbar_send.set)
        scrollbar_send.config(command=table_send.yview)

        # 创建treeview接受窗口
        columns_receive = ['序号', '接受数据位', '校验结果']
        table_receive = ttk.Treeview(
            master=frame_receive,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=columns_receive,  # 显示的列
            show='headings',  # 隐藏首列
        )
        table_receive.heading(column='序号', text='序号', anchor='w')
        table_receive.heading(column='接受数据位', text='接受数据位', anchor='w')  # 定义表头
        table_receive.heading(column='校验结果', text='校验结果', anchor='w')
        table_receive.column(column='序号', width=50, anchor='w')  # 定义列
        table_receive.column(column='接受数据位', width=120, anchor='w')
        table_receive.column(column='校验结果', width=60, anchor='w')
        table_receive.grid(row=0, column=0, sticky='w')
        # 为table_receive添加垂直滚动条
        scrollbar_receive = tk.Scrollbar(frame_receive, orient=tk.VERTICAL)
        scrollbar_receive.grid(row=0, column=1, sticky='ns')
        table_receive.config(yscrollcommand=scrollbar_receive.set)
        scrollbar_receive.config(command=table_receive.yview)

        # CRC生成多项式输入框
        polynomial_text = tk.Label(frame_enter, text='CRC生成多项式（使用6位二进制，首尾位为1）：', bg='#FFFFFF',
                                   fg='#000000')
        polynomial_text.grid(row=0, column=0)
        polynomial_entry = tk.Entry(frame_enter, bg='#FFFFFF', fg='#000000')
        polynomial_entry.grid(row=0, column=1)
        polynomial_entry.insert(0, "无输入将随机生成多项式")
        # 创建两个按钮
        button_send = tk.Button(frame_enter, text='发送数据', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                command=lambda: self.__send_data_crc(table_send, polynomial_entry))
        button_send.grid(row=1, column=0, padx=100, pady=10)
        button_receive = tk.Button(frame_enter, text='接收数据', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                   command=lambda: self.__receive_data_crc(table_receive, table_send,
                                                                           frame_result))
        button_receive.grid(row=1, column=1, padx=100, pady=10)

    def __send_data_crc(self, table: ttk.Treeview, entry: tk.Entry) -> None:
        # table初始化
        self.__delete(table)
        # 生成CRC多项式
        if entry.get() == "无输入将随机生成多项式" or entry.get() == self.polynomial:
            polynomial = CrcCheck.generate_polynomial(6)
            self.polynomial = polynomial
            entry.delete(0, tk.END)
            entry.insert(0, polynomial)
        else:
            polynomial = entry.get()
            self.polynomial = polynomial
        # 生成数据并计算校验位
        for index, binary_data in enumerate(utils.generate_data(8, 100)):
            check_digit = CrcCheck.generate_crc_check_digit(binary_data, polynomial)
            data = [str(index), binary_data, check_digit]
            table.insert('', tk.END, values=data)

    def __receive_data_crc(self, table_receive: ttk.Treeview, table_send: ttk.Treeview,
                           frame_end: tk.LabelFrame) -> None:
        # 数据统计
        all_count = len(table_send.get_children())  # 总共数据条数
        error_count = 0  # 错误数据条数
        error_miss_count = 0  # 未找到错误数据条数
        # table初始化
        self.__delete(table_receive)
        # 设置三种标签
        table_receive.tag_configure('error_data', foreground='blue')
        table_receive.tag_configure('error_checked', foreground='red')
        table_receive.tag_configure('error_miss', foreground='green')
        # 插入并校验数据
        obj = table_send.get_children()
        for item in obj:
            # 对数据进行模拟干扰
            send_data = list(table_send.item(item, 'values'))
            receive_data = [send_data[0], utils.interference_simulation(send_data[1], 10) + send_data[2]]
            # 根据CRC生成多项式校验数据
            flag = CrcCheck.crc_check(receive_data[1], self.polynomial)
            receive_data.append(flag)
            # 插入数据并给错误数据打上标签
            table_receive.insert('', tk.END, values=receive_data)
            if receive_data[1] != send_data[1] + send_data[2]:
                error_count += 1
                table_receive.item(item, tags=("error_data",))
                if receive_data[-1] != "0":
                    table_receive.item(item, tags=("error_checked",))
                else:
                    error_miss_count += 1
                    table_receive.item(item, tags=("error_miss",))

        # 输出数据传输结果
        text = tk.Text(frame_end, height=6, bg='#FFFFFF', fg='#000000')
        text.grid(row=0, column=0, sticky='w')
        text.insert(tk.END, f'总共{all_count}条数据\n')
        text.insert(tk.END, f'错误{error_count}条数据\n')
        text.insert(tk.END, f'未找到{error_miss_count}条数据\n')
        # 输出传输错误率,保留两位小数
        text.insert(tk.END, f'传输错误率{(error_count / all_count * 100):.2f}%\n')

    def __frame_hamming_check(self, frame_bottom: tk.Frame) -> None:
        # 清除框架内的内容
        for widget in frame_bottom.winfo_children():
            widget.destroy()
        # 创建内容框架
        frame_content = tk.Frame(frame_bottom, bg='#FFFFFF')
        frame_content.grid(row=0, column=0)

        # 创建数据展示框架
        frame_show = tk.LabelFrame(frame_content, text="数据展示", labelanchor="n", bg='#FFFFFF')
        frame_show.grid(row=0, column=0)
        # 创建发送框架
        frame_send = tk.LabelFrame(frame_show, text="发送数据", labelanchor="n", bg='#FFFFFF')
        frame_send.grid(row=0, column=0)
        # 创建接收框架
        frame_receive = tk.LabelFrame(frame_show, text="接收数据", labelanchor="n", bg='#FFFFFF')
        frame_receive.grid(row=0, column=1)

        # 创建按钮框架
        frame_enter = tk.Frame(frame_content, bg='#FFFFFF')
        frame_enter.grid(row=1, column=0)
        # 创建结果框架
        frame_result = tk.LabelFrame(frame_content, text="结果", labelanchor="n", bg='#ffFFFF')
        frame_result.grid(row=2, column=0)

        # 创建treeview发送窗口
        columns_send = ['序号', '数据位', '海明码']
        table_send = ttk.Treeview(
            master=frame_send,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=columns_send,  # 显示的列
            show='headings',  # 隐藏首列
        )
        table_send.heading(column='序号', text='序号', anchor='w')
        table_send.heading(column='数据位', text='数据位', anchor='w')  # 定义表头
        table_send.heading(column='海明码', text='海明码', anchor='w')  # 定义表头
        table_send.column(column='序号', width=50, anchor='w')  # 定义列
        table_send.column(column='数据位', width=100, anchor='w')  # 定义列
        table_send.column(column='海明码', width=100, anchor='w')  # 定义列
        table_send.grid(row=0, column=0, sticky='w')
        # 为table_send添加垂直滚动条
        scrollbar_send = tk.Scrollbar(frame_send, orient=tk.VERTICAL)
        scrollbar_send.grid(row=0, column=1, sticky='ns')
        table_send.config(yscrollcommand=scrollbar_send.set)
        scrollbar_send.config(command=table_send.yview)

        # 创建treeview接受窗口
        columns_receive = ['序号', '海明码', '校验', '纠错结果']
        table_receive = ttk.Treeview(
            master=frame_receive,  # 父容器
            height=15,  # 表格显示的行数,height行
            columns=columns_receive,  # 显示的列
            show='headings',  # 隐藏首列
        )
        table_receive.heading(column='序号', text='序号', anchor='w')
        table_receive.heading(column='海明码', text='海明码', anchor='w')  # 定义表头
        table_receive.heading(column='校验', text='校验', anchor='w')
        table_receive.heading(column='纠错结果', text='纠错结果', anchor='w')
        table_receive.column(column='序号', width=50, anchor='w')  # 定义列
        table_receive.column(column='海明码', width=100, anchor='w')
        table_receive.column(column='校验', width=50, anchor='w')
        table_receive.column(column='纠错结果', width=150, anchor='w')
        table_receive.grid(row=0, column=0, sticky='w')
        # 为table_receive添加垂直滚动条
        scrollbar_receive = tk.Scrollbar(frame_receive, orient=tk.VERTICAL)
        scrollbar_receive.grid(row=0, column=1, sticky='ns')
        table_receive.config(yscrollcommand=scrollbar_receive.set)
        scrollbar_receive.config(command=table_receive.yview)

        # 创建两个按钮
        button_send = tk.Button(frame_enter, text='发送数据', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                command=lambda: self.__send_data_hamming(table_send))
        button_send.grid(row=0, column=0, padx=100, pady=10)
        button_receive = tk.Button(frame_enter, text='接收数据', width=10, height=2, bg='#FFFFFF', fg='#000000',
                                   command=lambda: self.__receive_data_hamming(table_receive, table_send,
                                                                               frame_result))
        button_receive.grid(row=0, column=1, padx=100, pady=10)

    def __send_data_hamming(self, table: ttk.Treeview) -> None:
        # table初始化
        self.__delete(table)
        for index, binary_data in enumerate(utils.generate_data(8, 100)):
            checked_bin = HammingCheck.generate_checked_bin(binary_data, mode=hamming_check_mode)
            data = [str(index), binary_data, checked_bin]
            table.insert('', tk.END, values=data)

    def __receive_data_hamming(self, table_receive: ttk.Treeview, table_send: ttk.Treeview,
                               frame_end: tk.LabelFrame) -> None:
        # 数据统计
        all_count = len(table_send.get_children())  # 总共数据条数
        error_count = 0  # 错误数据条数
        error_miss_count = 0  # 未找到错误数据条数
        # table初始化
        self.__delete(table_receive)
        # 设置三种标签
        table_receive.tag_configure('error_data', foreground='blue')
        table_receive.tag_configure('error_checked', foreground='red')
        table_receive.tag_configure('error_miss', foreground='green')
        # 插入并校验数据
        obj = table_send.get_children()
        for item in obj:
            receive_data = []
            # 对数据进行模拟干扰
            send_data = list(table_send.item(item, 'values'))  # 获得发送的数据
            receive_data.append(send_data[0])  # 插入序号，下标0
            receive_data.append(utils.interference_simulation(send_data[2], 10))  # 插入干扰后的数据，下标1
            # 根据数据计算校验位
            results_list = HammingCheck.hamming_check(receive_data[1], 'even')
            position = results_list[1]
            if position is not None:
                error_position = "错误位：" + str(position) + " 正确值:" + results_list[2][position - 1]
            else:
                error_position = "无错误"
            receive_data.append(results_list[0])  # 插入校验结果，下标2
            receive_data.append(error_position)  # 插入纠错结果，下标3
            # 插入数据
            table_receive.insert('', tk.END, values=receive_data)
            # 给错误数据打上标签
            if receive_data[1] != send_data[2]:
                error_count += 1
                table_receive.item(item, tags=("error_data",))
                if receive_data[-2] is False:
                    table_receive.item(item, tags=("error_checked",))
                else:
                    error_miss_count += 1
                    table_receive.item(item, tags=("error_miss",))
        # 输出数据传输结果
        text = tk.Text(frame_end, height=6, bg='#FFFFFF', fg='#000000')
        text.grid(row=0, column=0, sticky='w')
        text.insert(tk.END, f'总共{all_count}条数据\n')
        text.insert(tk.END, f'错误{error_count}条数据\n')
        text.insert(tk.END, f'未找到{error_miss_count}条数据\n')
        # 输出传输错误率,保留两位小数
        text.insert(tk.END, f'传输错误率{(error_count / all_count * 100):.2f}%\n')

    def __delete(self, table: ttk.Treeview) -> None:
        obj = table.get_children()
        for item in obj:
            table.delete(item)


if __name__ == '__main__':
    # 创建tkinter应用程序窗口
    main_window = tk.Tk()
    rfid = RFID(main_window)
    # 启动消息循环
    main_window.mainloop()
