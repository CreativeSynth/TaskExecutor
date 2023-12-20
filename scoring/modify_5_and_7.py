import os, pandas as pd

def synchronize_indices(input_path, reference_path, output_path):
    # Read CSV files
    input_df = pd.read_csv(input_path)
    reference_df = pd.read_csv(reference_path)

    # Find indices to keep
    common_indices = reference_df['index'].tolist()
    input_df = input_df[input_df['index'].isin(common_indices)]

    # Save the synchronized data to a new CSV file
    input_df.to_csv(output_path, index=False)

# Example usage:
input_file_path = '/TaskExecutor/koalpaca5.8b/grouped_results/before_sorting/ko_quiz_7_result.csv'
reference_file_path = '/TaskManager/ko_quiz/ko_quiz_7.csv'
output_file_path = '/TaskExecutor/koalpaca5.8b/grouped_results/ko_quiz_7_result.csv'

current_position = os.getcwd()
current_position = current_position[current_position.find('/TaskExecutor'):]

input_file_path = os.path.relpath(input_file_path, current_position)
reference_file_path = os.path.relpath(reference_file_path, current_position)
output_file_path = os.path.relpath(output_file_path, current_position)

synchronize_indices(input_file_path, reference_file_path, output_file_path)
