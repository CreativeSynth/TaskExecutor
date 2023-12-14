import pandas as pd
import sys
sys.path.append('../')
from tasks_configure import TaskReader

result_data = pd.read_csv("result.csv")
taskReader = TaskReader("../../TaskManager")

for input_data_dir in taskReader.get_input_data_dirs():
    data = None
    try:
        data = pd.read_csv(input_data_dir)
    except:
        print(f"Error occures while reading {input_data_dir}. Skikped.")
        continue
    for row in data:
        print(row)
