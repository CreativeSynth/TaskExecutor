import os, pandas as pd

# List of CSV file paths
csv_file_paths = [
    '/TaskExecutor/koalpaca5.8b/result.csv'
    ]

current_position = os.getcwd()
current_position = current_position[current_position.find('/TaskExecutor'):]

for csv_file_path in csv_file_paths:
    # Load the CSV file into a DataFrame
    relative_path = os.path.relpath(csv_file_path, current_position)
    df = pd.read_csv(relative_path)

    # Task is 'translation' if {task_name} includes '/' character
    df['group_name'] = df['task_name'].apply(lambda x: 'translation' if '/' in x else x)

    # Group the DataFrame by the new 'group_name' column
    grouped = df.groupby('group_name')

    # Create separate CSV files for each group
    for group_name, group_df in grouped:
        output_file_path = relative_path[:relative_path.rfind('/')] + '/grouped_results/' + group_name + '_result.csv'

        if not os.path.exists(relative_path[:relative_path.rfind('/')] + '/grouped_results'):
            os.makedirs(relative_path[:relative_path.rfind('/')] + '/grouped_results')

        group_df.drop(columns=['group_name'], inplace=True)  # Remove the temporary column
        group_df.to_csv(output_file_path, index=False)
        print(f'File created: {output_file_path}')