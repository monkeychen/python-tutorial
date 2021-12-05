import xlrd
import os
import sys
#读取excel文件
cwd=os.getcwd()

with open(sys.argv[1]+"\第一题选择题得分.csv","w+") as f:
    f.write("学号姓名,选择题1,选择题2,选择题3,选择题4,选择题5,选择题6,选择题7,选择题8,选择题9,选择题10\n")


for dirs in os.listdir(cwd):
    path1=os.path.join(cwd,dirs)

    if os.path.isdir(path1):
        if os.path.exists(path1+"\答题卡21.xlsx"):
            with open(sys.argv[1]+"\第一题选择题得分.csv", "a+") as f:
                print(123)
                wb = xlrd.open_workbook(path1+"\答题卡21.xlsx")  # 打开Excel文件
                sheet = wb.sheet_by_name('Sheet1')  # 通过excel表格名称(rank)获取工作表

                dat = []  # 创建空list
                # sheet.nrows #循环读取表格内容（每次读取一行数据）

                cells = sheet.row_values(2)  # 每行数据赋值给cells
                for i in range(1, 11):
                    data = str(cells[i]).strip()  # 因为表内可能存在多列数据，0代表第一列数据，1代表第二列，以此类推
                    dat.append(data)  # 把每次循环读取的数据插入到list

                strdaan = "BACCBBABAB"
                daan = ",".join(strdaan).split(",")
                print("答案",daan)

                jifen = list(map(lambda x, y: x == y, dat, daan))
                print("计分",jifen)
                every_got = [2 if i == True else 0 for i in jifen]
                print(every_got)
                # select_got = jifen.count(True)
                # print(select_got)

                every_got.insert(0,dirs)
                # every_got.append(select_got)
                str1=",".join(list(map(str,every_got)))
                f.write(str1)
                f.write("\n")

