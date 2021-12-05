import os
import argparse
import shutil
from datetime import datetime
import datetimeutils
from openpyxl import load_workbook
from unrar import rarfile


class Answer(object):
    score_conf = {
        "single_choice": 2,
        "multi_choice": 2,
        "judgment": 1,
        "programme_fill": 3,
        "complex": 3
    }

    def __init__(self, single_choice=None, multi_choice=None, judgment=None):
        self.single_choice = single_choice
        self.multi_choice = multi_choice
        self.judgment = judgment
        self.programme_fill = []
        self.complex = []


class Student(object):

    def __init__(self, sid, name, answer: Answer = None, std_answer: Answer = None, valid=True):
        self.sid = sid
        self.name = name
        self.answer = answer
        self.score = 0
        self.std_answer = std_answer
        self.valid = valid
        self.answer_dir_path = None

    def calc_score(self):
        if self.answer is None:
            self.valid = False
            return
        for q_type in Answer.score_conf.keys():
            tmp_std_ans_values = getattr(self.std_answer, q_type)
            tmp_ans_values = getattr(self.answer, q_type)
            if len(tmp_ans_values) != len(tmp_std_ans_values):
                self.valid = False
                return
            for i in range(0, len(tmp_std_ans_values)):
                # TODO
                pass


class ExamAssistant(object):
    root_dir = os.getcwd()

    def __init__(self):
        self.args = self.parse_cli_args()
        self.root_dir = self.args.root_dir
        self.answer_file_num = self.args.answer_file_num
        self.answer_dir = f"{self.root_dir}/answer"
        self.upload_dir = f"{self.root_dir}/upload"
        self.temp_dir = f"{self.upload_dir}/temp"
        self.action = self.args.action
        self.std_answer = self.load_answer_file(f"{self.answer_dir}/答题卡.xlsx")
        self.student_list = []

    def load_answer_file(self, answer_file_path):
        answer_card_wb = load_workbook(answer_file_path)
        sheet = answer_card_wb["Sheet1"]
        parse_conf = {
            "single_choice": {'row': 3, 'max_col': 16},
            "multi_choice": {'row': 6, 'max_col': 6},
            "judgment": {'row': 9, 'max_col': 16}
        }
        answer = Answer([], [], [])
        for k in parse_conf.keys():
            conf = parse_conf.get(k)
            if conf is None:
                continue
            tmp_arr = []
            for col_idx in range(2, conf.get('max_col') + 1):
                tmp_arr.append(sheet.cell(conf.get('row'), col_idx).value)
            setattr(answer, k, tmp_arr)
        return answer

    def submit_check(self):
        rar_list = os.listdir(self.upload_dir)
        self._remove_dir_tree(dir_path=self.temp_dir, include_self=False)

        for rar_name in rar_list:
            if not rar_name.endswith("rar") and not rar_name.endswith("zip"):
                print(f"The file [{rar_name}] doesn't end with rar and zip, so ignored it!")
                continue
            rar_file_path = f"{self.upload_dir}/{rar_name}"
            s_id = rar_name[0:9]
            s_name = rar_name[9:-4]
            unrar_tmp_dir_path = f"{self.temp_dir}/{s_id}_{s_name}"
            student = Student(sid=s_id, name=s_name, std_answer=self.std_answer)
            is_valid = True
            try:
                self._remove_dir_tree(dir_path=unrar_tmp_dir_path, include_self=False)
                rar_file = rarfile.RarFile(rar_file_path)
                rar_file.extractall(path=unrar_tmp_dir_path)
                tmp_stu_dir_path = f"{unrar_tmp_dir_path}/{s_id}{s_name}"
                student.answer_dir_path = tmp_stu_dir_path
                card_path = f"{tmp_stu_dir_path}/答题卡.xlsx"
                if os.path.exists(card_path):
                    answer = self.load_answer_file(card_path)
                    student.answer = answer
                else:
                    is_valid = False
                if is_valid:
                    code_file_list = self._list_dir(dir_path=tmp_stu_dir_path, ext=self.args.ext_name)
                    is_valid = len(code_file_list) == self.answer_file_num
                student.valid = is_valid
                student.calc_score()
            except Exception as e:
                print(f"Fail to parse student[{s_id}: {s_name}]'s answer rar file!")

        invalid_student_list = []

        return invalid_student_list

    def evaluate(self):
        pass

    def _remove_dir_tree(self, dir_path, include_self=True):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        if not include_self:
            os.makedirs(dir_path)

    def _list_dir(self, dir_path, ext=None):
        name_list = []
        for dir_name in os.listdir(dir_path):
            if ext is None:
                name_list.append(dir_name)
            else:
                if dir_name.endswith(ext):
                    name_list.append(dir_name)
        return name_list

    def parse_cli_args(self):
        cli_parser = argparse.ArgumentParser(description="这是一个Python考试辅助工具。", add_help=False)
        cli_parser.add_argument('-a', '--action', nargs='?', choices=['submit', 'evaluate'], default='submit', help='设置运行环境（submit：交卷检测，evaluate：评卷），默认为：交卷检测')
        cli_parser.add_argument('-e', '--env_mode', nargs='?', choices=['dev', 'prod'], default='prod', help='设置运行环境（dev：开发环境，prod：生产环境），默认为：开发环境')
        cli_parser.add_argument('-n', '--answer_file_num', nargs='?', type=int, default=3, help='学生提交的python文件数，默认为3。')
        cli_parser.add_argument('-r', '--root_dir', nargs='?', default=f"{os.getcwd()}", help='程序工作根目录路径。')
        cli_parser.add_argument('-x', '--ext_name', nargs='?', default="py", help='学生提交作业中程序文件扩展名，默认为：py')
        cli_parser.add_argument('-h', '--help', action='help', help='显示本帮助信息并退出')
        cli_parser.add_argument('-v', '--version', action='version', version='%(prog)s V0.0.1', help='显示当前版本信息并退出')

        args = cli_parser.parse_args()
        scheduled_time = datetimeutils.datetime_to_str(datetime.now(), fmt=datetimeutils.FMT_DEFAULT)
        print(f"The programme[{cli_parser.prog}] was scheduled at {scheduled_time}, cwd = {os.getcwd()}, env_mode = {args.env_mode}, "
              f"root_dir = {args.root_dir}, answer_file_num = {args.answer_file_num}")
        return args

    def execute(self):
        if self.action == 'submit':
            self.submit_check()
        else:
            self.evaluate()


if __name__ == "__main__":
    ExamAssistant().execute()
