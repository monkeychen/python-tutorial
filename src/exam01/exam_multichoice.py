import tkinter as tk
from tkinter import ttk
import pyodbc
import os


def show_multiple_choice_question(event):
    global root,selected_option, selected_answers, tree, question_label, options_frame, multiple_choice_questions
    # 获取当前选中的题目行
    selected_row = tree.focus()

    # 根据选中的行获取题目的文本值
    selected_question_text = tree.item(selected_row, 'text')
    index = int(selected_question_text) - 1

    # 创建新的选项按钮（多选题可以选择多个选项）
    selected_option = [tk.IntVar(master=root) for _ in range(4)]
    # 显示题目和各个选项
    question_data = multiple_choice_questions[index]
    question_label.config(text=f"{index + 1}. {question_data[1]}", font=("SimSun", 12))  # 显示题号和题目

    # 清除之前的选项按钮
    for widget in options_frame.winfo_children():
        widget.destroy()


    for i in range(2, 6):  # 第三列到第六列是选项
        option = tk.Checkbutton(options_frame, text=f"{chr(64+i-1)}. {question_data[i]}",font=("SimSun", 10), variable=selected_option[i-2], onvalue=i-1, offvalue=0, command=lambda: update_multiple_choice_result())
        option.pack(anchor=tk.W)

        if all(option == 0 for option in selected_answers[index]):
            selected_option[i - 2].set(0)
        else:
            if i-1 in selected_answers[index]:
                selected_option[i-2].set(i-1)
        #
        # # 保留用户先前选择的选项状态
        # if i - 1 in selected_answers[index]:
        #     selected_option[i-2].set(i-1)

def update_multiple_choice_result():
    global selected_option,selected_answers, tree
    selected_answer = [var.get() for var in selected_option]
    print("selected_answer",selected_answer)
    if any(selected_answer):
        # 获取当前选中的题目行
        selected_row = tree.focus()
        # 将用户选择的答案显示在TreeView的第二列中
        tree.item(selected_row, values=("".join(dic[i+1] for i, val in enumerate(selected_answer) if val),))

        # 根据选中的行获取题目的文本值
        selected_question_text = tree.item(selected_row, 'text')
        index = int(selected_question_text) - 1
        selected_answers[index] = [i+1 for i, val in enumerate(selected_answer) if val]
        print(selected_answers)
        submit_multiple_choice_answers()  # 在此处可以立即提交用户的答案到数据库

def submit_multiple_choice_answers():
    global selected_answers, multiple_choice_questions, cursor, conn
    # 将用户选择的答案存回数据库对应题目的学生选项字段
    for i, answer in selected_answers.items():
        question_id = multiple_choice_questions[i][0]
        cursor.execute("UPDATE multiple_choice_question SET 学生选项 = ? WHERE ID = ?", ("".join(map(str, answer)), question_id))
    conn.commit()

    print("用户答案已提交至数据库！")
    with open(os.path.join(os.getcwd(), "_result_multiple_choice.py"), 'w', encoding="utf-8") as f:
        t_dic={}
        f.write("s=")
        for i, answer in selected_answers.items():
            question_id = multiple_choice_questions[i][0]
            t_dic[question_id]="".join(map(str, answer))
        f.writelines(str(t_dic))
        f.write("\nx=input()\n")
        f.write("print(s[int(x)])")

def on_window_close(win_opened):
    print("窗口关闭")
    win_opened[1]=0
    root.destroy()

def multichoice_main(win_opened):
    global selected_option, selected_answers, tree, question_label, options_frame, multiple_choice_questions, dic, conn, cursor,root

    # 连接到数据库，替换为您的数据库路径和密码
    connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.getcwd() + '\\select.mdb;PWD=mushroom1985;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # 获取多选题数据
    cursor.execute('SELECT ID, 题目, 选项a, 选项b, 选项c, 选项d, 学生选项 FROM multiple_choice_question')
    multiple_choice_questions = cursor.fetchall()
    dic = {0: "", 1: "A", 2: "B", 3: "C", 4: "D"}

    # 初始化将多选题中的学生选项先加到字典里
    selected_answers = {i: list(map(int, str(record[6]))) if record[6] else [] for i, record in
                        enumerate(multiple_choice_questions)}



    # 创建窗口并设置大小
    root = tk.Tk()
    root.title("多选题")
    root.geometry("800x500")
    window_width = 800
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")



    # 创建题号和学生选项的表格
    tree = ttk.Treeview(root, columns=('学生选项'))
    tree.heading('#0', text='题号')
    tree.column("#0",minwidth=0,width=50)
    tree.heading('学生选项', text='学生选项')
    tree.column("学生选项",minwidth=0,width=100)

    # 添加题目数据到表格中
    for i, question in enumerate(multiple_choice_questions):
        tree.insert('', 'end', text=str(i + 1), values=("".join(dic[int(item)] for item in question[6])) if question[6] else dic[0])

    tree.pack(side=tk.LEFT,fill=tk.Y)

    tree.bind('<<TreeviewSelect>>', show_multiple_choice_question)  # 绑定选中事件

    # 主题目和选项区域
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)



    question_label = tk.Label(main_frame, text="", wraplength=550, anchor="w", justify="left")
    question_label.pack()

    options_frame = tk.Frame(main_frame)
    options_frame.pack()
    root.protocol("WM_DELETE_WINDOW", lambda: on_window_close(win_opened))
    root.mainloop()


if __name__ == '__main__':
    multichoice_main()
