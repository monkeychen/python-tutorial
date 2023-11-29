import tkinter as tk
from exam_select import select_main
from exam_judge import judge_main
from exam_multichoice import multichoice_main
import os

win_open1={0:0,1:0,2:0}
def show_single_choice(win_opened=win_open1):
    # 显示单选题界面
    if not win_opened[0]:
        win_opened[0]=1
        select_main(win_opened)
    else:
        print("选择题窗口已开启")

def show_multiple_choice(win_opened=win_open1):
    # 显示多选题界面
    if not win_opened[1]:
        win_opened[1]=1
        multichoice_main(win_opened)
    else:
        print("多选题窗口已开启")

def show_judgement(win_opened=win_open1):
    # 显示判断题界面
    if not win_opened[2]:
        win_opened[2] = 1
        judge_main(win_opened)
    else:
        print("判断题窗口已开启")

def show_program_fill_1():
    # 显示程序填空题1界面
    try:
        os.startfile("程序填空题01.txt")
    except IOError:
        print("无法打开文件")

def show_program_fill_2():
    # 显示程序填空题2界面
    try:
        os.startfile("程序填空题02.txt")
    except IOError:
        print("无法打开文件")

def show_program_fill_3():
    # 显示程序填空题3界面
    try:
        os.startfile("程序填空题03.txt")
    except IOError:
        print("无法打开文件")

def show_comprehensive_1():
    # 显示综合题界面
    try:
        os.startfile("综合题01.txt")
    except IOError:
        print("无法打开文件")

def show_comprehensive_2():
    # 显示综合题界面
    try:
        os.startfile("综合题02.txt")
    except IOError:
        print("无法打开文件")

def main1():
    rootmain = tk.Tk()
    rootmain.title("考试系统V2023")
    rootmain.geometry("300x450")
    rootmain.maxsize(300,450)
    button_height=2
    button_pad=5
    btn_single_choice = tk.Button(rootmain, text="单选题", command=show_single_choice,height=button_height)
    btn_single_choice.pack(side=tk.TOP, fill=tk.X,pady=button_pad)

    btn_multiple_choice = tk.Button(rootmain, text="多选题", command=show_multiple_choice,height=button_height)
    btn_multiple_choice.pack(side=tk.TOP, fill=tk.X,pady=button_pad)

    btn_judgement = tk.Button(rootmain, text="判断题", command=show_judgement,height=button_height)
    btn_judgement.pack(side=tk.TOP, fill=tk.X,pady=button_pad)

    btn_program_fill_1 = tk.Button(rootmain, text="程序填空题1", command=show_program_fill_1,height=button_height)
    btn_program_fill_1.pack(side=tk.TOP, fill=tk.X,pady=button_pad)

    btn_program_fill_2 = tk.Button(rootmain, text="程序填空题2", command=show_program_fill_2,height=button_height)
    btn_program_fill_2.pack(side=tk.TOP, fill=tk.X,pady=button_pad)

    btn_program_fill_3 = tk.Button(rootmain, text="程序填空题3", command=show_program_fill_3,height=button_height)
    btn_program_fill_3.pack(side=tk.TOP, fill=tk.X,pady=button_pad)

    btn_comprehensive_1 = tk.Button(rootmain, text="综合题1", command=show_comprehensive_1,height=button_height)
    btn_comprehensive_1.pack(side=tk.TOP, fill=tk.X,pady=button_pad)

    btn_comprehensive_2 = tk.Button(rootmain, text="综合题2", command=show_comprehensive_2, height=button_height)
    btn_comprehensive_2.pack(side=tk.TOP, fill=tk.X, pady=button_pad)

    rootmain.mainloop()


if __name__ == '__main__':
    main1()
