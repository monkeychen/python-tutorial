import tkinter as tk
from tkinter import ttk
import pyodbc
import os

def show_question(event):
    global selected_option, selected_answers, tree, question_label, options_frame, questions

    selected_row = tree.focus()
    selected_question_text = tree.item(selected_row, 'text')
    index = int(selected_question_text) - 1

    question_data = questions[index]
    question_label.config(text=f"{index + 1}. {question_data[1]}", font=("SimSun", 12))

    for widget in options_frame.winfo_children():
        widget.destroy()

    for i in range(2, 6):
        option = tk.Radiobutton(options_frame, text=f"{chr(64+i-1)}. {question_data[i]}", font=("SimSun", 12), variable=selected_option, value=i-1, command=update_result)
        option.pack(anchor=tk.W)
        print(selected_answers)
    if selected_answers.get(index) is not None:
        selected_option.set(selected_answers[index])
    else:
        selected_option.set(0)

def update_result():
    global selected_option, selected_answers, tree, questions

    selected_answer = selected_option.get()
    if selected_answer:
        selected_row = tree.focus()
        tree.item(selected_row, values=(dic[selected_answer],))

        selected_question_text = tree.item(selected_row, 'text')
        index = int(selected_question_text) - 1
        selected_answers[index] = selected_answer
        submit_answers()

def submit_answers():
    global selected_answers, questions, cursor, conn

    for i, answer in selected_answers.items():
        question_id = questions[i][0]
        cursor.execute("UPDATE question SET 学生选项 = ? WHERE ID = ?", (answer, question_id))
    conn.commit()
    print("用户答案已提交至数据库！")
    with open(os.path.join(os.getcwd(),"_result_select.py"),'w',encoding="utf-8") as f:
        f.write("s='X"+"".join(map(str,selected_answers.values()))+"'\n")
        f.write("x=input()\n")
        f.write("print(s[int(x)])")


def on_window_close(win_opened):
    print("窗口关闭")
    win_opened[0]=0
    root.destroy()


def select_main(win_opened):
    global selected_option, selected_answers, tree, question_label, options_frame, questions, dic, conn, cursor,root
    #检测是否已经存在一个单选窗口，存在则把窗口带到前台
    # if hasattr(select_main,'root') and select_main.root:
    #     select_main.root.lift()
    #     return

    root = tk.Tk()
    root.title("单选题")
    root.geometry("800x500")
    window_width = 800
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # select_main.root=root

    connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+os.getcwd()+'\\select.mdb;PWD=mushroom1985;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute('SELECT ID, 题目, 选项a, 选项b, 选项c, 选项d, 学生选项 FROM question')
    questions = cursor.fetchall()
    dic={0:"",1:"A",2:"B",3:"C",4:"D"}

    selected_answers = {i: int(record[6]) if record[6] else 0 for i, record in enumerate(questions)}

    tree = ttk.Treeview(root, columns=('学生选项'))
    tree.heading('#0', text='题号')
    tree.column("#0", minwidth=0, width=50)
    tree.heading('学生选项', text='学生选项')
    tree.column("学生选项", minwidth=0, width=100)
    tree.pack(side=tk.LEFT, fill=tk.Y)
    tree.bind('<<TreeviewSelect>>', show_question)
    for i ,question in enumerate(questions):
        tree.insert('','end',text=str(i+1),values=(dic[int(question[6]) if question[6] else 0]))
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    question_label = tk.Label(main_frame, text="", wraplength=500, anchor="w", justify="left")
    question_label.pack()

    selected_option = tk.IntVar(master=root)
    options_frame = tk.Frame(main_frame)
    options_frame.pack()
    root.protocol("WM_DELETE_WINDOW", lambda :on_window_close(win_opened))
    root.mainloop()

if __name__ == "__main__":
    select_main()