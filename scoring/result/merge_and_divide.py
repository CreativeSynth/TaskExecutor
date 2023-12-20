import os
import pandas as pd

# Function to read and merge CSV files
def merge_csv_files(file_paths):
    dfs = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        dfs.append(df)
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

# Function to separate data based on 'task_name' and '/'
def separate_by_task_name(df, output_folder):
    # Group by a custom function to consider '/' as the same group
    grouped = df.groupby(lambda x: 'translation' if '/' in df['task_name'][x] else df['task_name'][x])
    for name, group in grouped:
        # Replace '/' with '_'
        filename = name.replace('/', '_') + '.csv'
        output_path = os.path.join(output_folder, filename)
        group.to_csv(output_path, index=False)

# Specify the paths of the CSV files and the output folder
file_paths = [
    'gemini-pro.csv',
    'gpt-3.5-turbo.csv',
    'ko_vicuna_7b.csv',
    'KoAlpaca-Polyglot-5.8B.csv',
    'kullm5.8b.csv',
    'kullm12.8b.csv',
    'llama2_13b.csv',
    'polyglot-ko-1.3b.csv'
    ]
output_folder = './re-sorted/'

# Merge CSV files
merged_data = merge_csv_files(file_paths)

# Separate data based on 'task_name' and '/'
separate_by_task_name(merged_data, output_folder)