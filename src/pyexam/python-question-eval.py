import os
import subprocess
import operator


FMT_DEFAULT = "%Y-%m-%d %H:%M:%S"
UTF8 = "UTF-8"


class StuScore(object):

    def __init__(self, stu_id):
        self.stu_id = stu_id
        self.scores = [0, 0, 0, 0, 0]

    def set_question_score(self, q_id: int, score: int):
        self.scores[q_id - 1] = score

    def __str__(self):
        return ",".join([self.stu_id] + [str(i) for i in self.scores] + [str(sum(self.scores))]) + "\n"


class PythonQuestionEval(object):

    question_conf = [
        {
            "begin": "程序填空题01", "end": "txt", "method": "eval_question_1",
            "input": ["{'a': 2, 'b': 3}", "{'a': 4, 'b': 3}"],
            "output": ["5", "7"]
        },
        {
            "begin": "程序填空题02", "end": "txt", "method": "eval_question_2",
            "input": ["", ""]
        },
        {
            "begin": "程序填空题03", "end": "txt", "method": "eval_question_3",
            "input": ["飞行学员需学习量子计算在航空航天领域的应用。", "aaa量子bbb飞行ccc航空ddd"],
            "output": ["*学员需学习*计算在*航天领域的应用。", "aaa*bbb*ccc*ddd"]
        },
        {"begin": "综合题01", "end": "txt", "method": "eval_question_4"},
        {"begin": "综合题02", "end": "txt", "method": "eval_question_5"}
    ]

    def __init__(self, answer_dir_path=None, py_code_dir_path=None):
        if answer_dir_path is None:
            answer_dir_path = f"{os.getcwd()}/upload/temp"
        if py_code_dir_path is None:
            py_code_dir_path = f"{os.getcwd()}/upload/py-code"
        self.answer_dir_path = answer_dir_path
        self.py_code_dir_path = py_code_dir_path
        self.stu_score_list = []

    def exec_shell_cmd(self, cmd, encoding=UTF8):
        exec_result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result_str = str(exec_result.stdout, encoding=encoding).strip()
        return result_str

    def generate_callable_py(self, stu_id, question_file_path, q_id):
        tmp_py_path = f"{self.py_code_dir_path}/{''.join(list(filter(str.isdigit, stu_id)))}-q{q_id}.py"
        if os.path.exists(tmp_py_path):
            os.remove(tmp_py_path)
        with open(question_file_path, mode='r', encoding="UTF-8-sig") as fr:
            read_txt = fr.read()
            replaced_txt = read_txt.replace("input()", "sys.argv[1]")
            with open(tmp_py_path, mode='w') as fw:
                fw.writelines(["import sys\n"])
                fw.write(replaced_txt)
        return tmp_py_path

    def clear_blank_in_file(self, question_file_path):
        with open(question_file_path, mode='r', encoding="UTF-8-sig") as fr:
            read_txt = fr.read()
        return "".join(read_txt.split(" "))

    def eval_question_1(self, stu_id, question_file_path, q_conf):
        tmp_py_path = self.generate_callable_py(stu_id, question_file_path, 1)
        # 第一步：通过执行py文件验证程序逻辑是否正确
        step1_flag = False
        try:
            exe_results = []
            for in_args in q_conf.get("input"):
                cmd = f"python3 {tmp_py_path} \"{in_args}\""
                out_str = self.exec_shell_cmd(cmd)
                exe_results.append(out_str)
            step1_flag = operator.eq(q_conf.get("output"), exe_results)
        except BaseException as e:
            print(str(e))

        if step1_flag:
            score = 5
        else:
            target_txt = self.clear_blank_in_file(question_file_path)
            score = 2 if target_txt.find("dictMenu.values()") != -1 else 0
            score += (3 if (target_txt.find("total+=i") != -1 or target_txt.find("total=total+i") != -1) else 0)
        return 1, score

    def eval_question_2(self, stu_id, question_file_path, q_conf):
        # 本题输出具有随机性，无法通过程序执行判断。
        target_txt = self.clear_blank_in_file(question_file_path)
        score = 2 if target_txt.find("importrandom") != -1 else 0
        score += (3 if target_txt.find("random.choice") != -1 else 0)
        return 2, score

    def eval_question_3(self, stu_id, question_file_path, q_conf):
        tmp_py_path = self.generate_callable_py(stu_id, question_file_path, 3)
        # 第一步：通过执行py文件验证程序逻辑是否正确
        step1_flag = False
        try:
            exe_results = []
            for in_args in q_conf.get("input"):
                cmd = f"python3 {tmp_py_path} \"{in_args}\""
                out_str = self.exec_shell_cmd(cmd)
                exe_results.append(out_str)
            step1_flag = operator.eq(q_conf.get("output"), exe_results)
        except BaseException as e:
            print(str(e))

        if step1_flag:
            score = 5
        else:
            target_txt = self.clear_blank_in_file(question_file_path)
            score = 5 if target_txt.find("text=text.replace(word,'*')") != -1 else 0
        return 3, score

    def eval_question_4(self, stu_id, question_file_path, q_conf):
        return 4, 0

    def eval_question_5(self, stu_id, question_file_path, q_conf):
        return 5, 0

    def evaluate(self):
        self.stu_score_list.clear()
        cnt = 1
        for stu_main_dir_name in os.listdir(self.answer_dir_path):
            stu_main_dir_path = f"{self.answer_dir_path}/{stu_main_dir_name}"
            print(f"{cnt}:BEGIN-------{stu_main_dir_name}--------")
            stu_score = StuScore(stu_main_dir_name)
            for stu_root, dirs, files in os.walk(stu_main_dir_path):
                if files is None or len(files) == 0:
                    continue
                files.sort()
                for ans_file_name in files:
                    q_conf = self.find_matched_conf(ans_file_name)
                    if q_conf is None:
                        continue
                    ans_file_path = f"{stu_root}/{ans_file_name}"
                    print(f"开始评阅题目：{ans_file_path}")
                    target_method = getattr(self, q_conf.get("method"))
                    q_id, q_score = target_method(stu_main_dir_name, ans_file_path, q_conf)
                    stu_score.set_question_score(q_id, q_score)
            self.stu_score_list.append(stu_score)
            print(f"{cnt}:END-------{stu_main_dir_name}--------")
            cnt += 1

        stu_score_file_path = f"{os.path.dirname(self.answer_dir_path)}/stu-score.csv"
        if os.path.exists(stu_score_file_path):
            os.remove(stu_score_file_path)
        with open(stu_score_file_path, mode='w') as score_writer:
            score_writer.writelines([str(stu_score) for stu_score in self.stu_score_list])
        return stu_score_file_path

    def find_matched_conf(self, file_name: str):
        matched_conf = None
        for conf in self.question_conf:
            matched_conf = conf if file_name.startswith(conf.get("begin")) \
                                   and file_name.endswith(conf.get("end")) else None
            if matched_conf is not None:
                break
        return matched_conf

    def datetime_to_str(self, dt, fmt=FMT_DEFAULT):
        return dt.strftime(fmt)


if __name__ == "__main__":
    print(f"cwd = {os.getcwd()}")
    PythonQuestionEval().evaluate()
