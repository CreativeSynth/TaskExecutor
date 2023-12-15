import pandas as pd
import sys
result_data = pd.read_csv("result.csv", engine="python")

print(result_data.head())