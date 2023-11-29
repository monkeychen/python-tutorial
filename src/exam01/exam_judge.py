import tkinter as tk
from tkinter import ttk
import pyodbc
import os


def show_judge_question(event):
    global selected_option, selected_answers, tree, question_label, options_frame, judge_questions

    # 获取当前选中的题目行
    selected_row = tree.focus()

    # 根据选中的行获取题目的文本值
    selected_question_text = tree.item(selected_row, 'text')
    index = int(selected_question_text) - 1

    # 显示题目
    question_data = judge_questions[index]
    question_label.config(text=f"{index + 1}. {question_data[1]}", font=("SimSun", 12))  # 显示题号和题目

    # 清除之前的选项按钮
    for widget in options_frame.winfo_children():
        widget.destroy()

    # 创建新的选项按钮（判断题只有对和错）
    for i in range(2):  # 0代表对，1代表错
        option = tk.Radiobutton(options_frame, text=dic[i+1], variable=selected_option, font=("SimSun", 12),value=i+1, command=update_judge_result)
        option.pack(anchor=tk.W)

        # 保留用户先前选择的选项状态
        if selected_answers.get(index) is not None:
            selected_option.set(selected_answers[index])
        else:
            selected_option.set(0)

def update_judge_result():
    global selected_option, selected_answers, tree, judge_questions

    selected_answer = selected_option.get()
    if selected_answer:
        # 获取当前选中的题目行
        selected_row = tree.focus()
        # 将用户选择的答案显示在TreeView的第二列中
        tree.item(selected_row, values=(dic[selected_answer],))

        # 根据选中的行获取题目的文本值
        selected_question_text = tree.item(selected_row, 'text')
        index = int(selected_question_text) - 1
        selected_answers[index] = selected_answer
        print(selected_answers)
        submit_judge_answers()  # 在此处可以立即提交用户的答案到数据库

def submit_judge_answers():
    global selected_answers,judge_questions, conn, cursor

    # 将用户选择的答案存回数据库对应题目的学生选项字段
    for i, answer in selected_answers.items():
        question_id = judge_questions[i][0]
        cursor.execute("UPDATE judge_question SET 学生选项 = ? WHERE ID = ?", (answer, question_id))
    conn.commit()

    print("用户答案已提交至数据库！")
    with open(os.path.join(os.getcwd(),"_result_judge.py"),'w',encoding="utf-8") as f:
        f.write("s='X"+"".join(map(str,selected_answers.values()))+"'\n")
        f.write("x=input()\n")
        f.write("print(s[int(x)])")

def on_window_close(win_opened):
    print("窗口关闭")
    win_opened[2]=0
    root.destroy()

def judge_main(win_opened):
    global selected_option, selected_answers, tree, question_label, options_frame, judge_questions, dic, conn, cursor,root

    # 连接到数据库，替换为您的数据库路径和密码
    connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.getcwd() + '\\select.mdb;PWD=mushroom1985;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # 获取判断题数据
    cursor.execute('SELECT ID, 题目, 正确答案, 学生选项 FROM judge_question')
    judge_questions = cursor.fetchall()
    dic = {0: "", 1: "对", 2: "错"}

    # 初始化将判断题中的学生选项先加到字典里
    selected_answers = {i: int(record[3]) if record[3] else 0 for i, record in enumerate(judge_questions)}


    # 创建窗口并设置大小
    root = tk.Tk()
    root.title("判断题")
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
    for i, question in enumerate(judge_questions):
        tree.insert('', 'end', text=str(i + 1), values=(dic[int(question[3] if question[3] else 0)]))

    tree.pack(side=tk.LEFT,fill=tk.Y)

    tree.bind('<<TreeviewSelect>>', show_judge_question)  # 绑定选中事件

    # 主题目和选项区域
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    question_label = tk.Label(main_frame, text="", wraplength=600, anchor="w", justify="left")
    question_label.pack()

    selected_option = tk.IntVar(master=root)
    options_frame = tk.Frame(main_frame)
    options_frame.pack()

    root.protocol("WM_DELETE_WINDOW", lambda: on_window_close(win_opened))
    root.mainloop()


if __name__ == '__main__':
    judge_main()
