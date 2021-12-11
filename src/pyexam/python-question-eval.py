import os


class PythonQuestionEval(object):

    question_conf = [
        {"begin": "程序填空题01", "end": "txt"},
        {"begin": "程序填空题02", "end": "txt"},
        {"begin": "程序填空题03", "end": "txt"},
        {"begin": "综合题01", "end": "txt"},
        {"begin": "综合题02", "end": "txt"}
    ]

    def __init__(self, answer_dir_path=None):
        if answer_dir_path is None:
            answer_dir_path = f"{os.getcwd()}/upload/temp"
        self.answer_dir_path = answer_dir_path

    def eval_question_1(self, question_file_path):
        pass

    def eval_question_2(self, question_file_path):
        pass

    def eval_question_3(self, question_file_path):
        pass

    def eval_question_4(self, question_file_path):
        pass

    def eval_question_5(self, question_file_path):
        pass

    def evaluate(self):
        cnt = 1
        for stu_main_dir_name in os.listdir(self.answer_dir_path):
            stu_main_dir_path = f"{self.answer_dir_path}/{stu_main_dir_name}"
            print(f"{cnt}:BEGIN-------{stu_main_dir_name}--------")
            for stu_root, dirs, files in os.walk(stu_main_dir_path):
                if files is None or len(files) == 0:
                    continue
                for ans_file_name in files:
                    print(f"{stu_root}/{ans_file_name}")
            print(f"{cnt}:END-------{stu_main_dir_name}--------")
            cnt += 1


if __name__ == "__main__":
    print(f"cwd = {os.getcwd()}")
    PythonQuestionEval().evaluate()