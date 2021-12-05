import os
import sys
import tkinter as tk
import tkinter.messagebox as msg
from unrar import rarfile


class WinFileChecker(object):

    def __init__(self, tk_inst: tk.Tk):
        self.tk_inst = tk_inst
        self.app_path = os.path.dirname(sys.argv[0])
        #self.check_output = self.app_path + "/invalid_list.txt"
        self.init_win_layout()

    def init_win_layout(self):
        self.tk_inst.title("压缩包检测工具V1.0")
        self.tk_inst.geometry('500x600')

        self.btn = tk.Button(self.tk_inst, text="压缩包内容检测", bg="lightblue", width=30, height=1, command=self.rar_check)
        self.btn.pack(pady=15)
        self.label3= tk.Label(self.tk_inst, text="本产品只获取当前文件夹中rar压缩包的总数，\n以及检测rar中是否包含Acopr与prog、答题卡xlsx文件。\n如需更详细的检测，请进行人工判定")
        self.label3.pack(pady=1)
        self.text2=tk.StringVar()
        self.label2=tk.Label(self.tk_inst,textvariable=self.text2,fg="red",width=50,relief="sunken",bg="white",font=16)
        self.label2.pack(pady=1)

        self.text1=tk.StringVar()
        self.label1=tk.Label(self.tk_inst,textvariable=self.text1,fg="red",width=50,height=30,relief="sunken",bg="white",font=16)
        self.label1.pack()

    def rar_check(self):
        str=""
        num=0
        for rar_file in os.listdir(self.app_path):
            if rar_file.endswith("rar"):
                self.is_rar_filename(self.app_path + "/" + rar_file)
                num=num+1
                if self.is_rar_invalid(self.app_path + "/" + rar_file):
                    str=str+rar_file + "  内容有误，请重新提交\n"
                self.text1.set(str)
        self.text2.set("当前文件夹中rar压缩包数量：{}个".format(num))

        #msg.showinfo("提示", "收到rar压缩包总数：{}个".format(num))

    def is_rar_filename(self,rar_path):
        rar = rarfile.RarFile(rar_path)
        # for file in rar.filename:
        #
        # print(rar.filename)

    def is_rar_invalid(self, rar_path):
        rar = rarfile.RarFile(rar_path)
        flags = 0
        for file_info in rar.filelist:
            file_name = os.path.basename(file_info.filename)
            print(file_name)
            if (file_name.startswith("Acopr") or file_name.startswith("prog")) and file_name.endswith(".accdb"):
                flags = flags + 1
            elif file_name.endswith("xlsx") and file_name.startswith("答题卡"):
                flags=flags+1
        print(flags)
        return flags !=5


if __name__ == "__main__":
    win = tk.Tk()
    GUI = WinFileChecker(win)
    win.mainloop()
