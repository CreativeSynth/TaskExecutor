'''
현재 인식되는 tasks들을 관리하고 보여줌
'''
from typing import Iterable
import pandas as pd

class TaskReader:
    mount_dir = "../TaskManager"
    data_dirs = []
    data_lens = []

    def __init__(self, mount_dir="../TaskManager", subdirs:Iterable[str]=["ko_quiz/ko_quiz_1.csv",
                   "ko_quiz/ko_quiz_2.csv",
                   "ko_quiz/ko_quiz_3.csv",
                   "ko_quiz/ko_quiz_4.csv",
                   "ko_quiz/ko_quiz_5.csv",
                   "ko_quiz/ko_quiz_6.csv",
                   "ko_quiz/ko_quiz_7.csv",
                   "ko_quiz/ko_quiz_8.csv",
                   "nli/nli.csv",
                   "number_1/number_1.csv",
                   "number_2/number_2.csv",
                   "number_3/number_3.csv",
                   "reasoning/reasoning.csv",
                   "spelling_correct/spelling_correct.csv",
                   "summarization/summarization.csv",
                   "translation/translation.csv"
                   ]):
        self.mount_dir = mount_dir
        su = 0
        for subdir in subdirs:
            csv_dir = mount_dir + "/" + subdir
            try:
                data = pd.read_csv(csv_dir)
                print(subdir,"\t:",len(data),"개 데이터 인식됨")
                self.data_dirs.append(csv_dir)
                self.data_lens.append(len(data))
                su += len(data)
            except Exception as e:
                print(csv_dir+" 읽는 중 에러 발생")
                print(e)

        print(f"전체 {len(subdirs)}개 중 {len(self.data_dirs)}개 처리 완료.")
        print(f"전체 데이터 개수 = {su}")
    
    def get_input_data_dirs(self):
        return self.data_dirs