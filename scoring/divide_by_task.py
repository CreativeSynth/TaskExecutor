import pandas as pd

# Load the CSV file into a DataFrame
csv_file_path = 'result.csv'
df = pd.read_csv(csv_file_path)

# Extract the part of 'task_name' before '/'
df['group_name'] = df['task_name'].apply(lambda x: 'translation' if '/' in x else x)

# Group the DataFrame by the new 'group_name' column
grouped = df.groupby('group_name')

# Create separate CSV files for each group
for group_name, group_df in grouped:
    output_file_path = f'temp/{group_name}_output.csv'
    group_df.drop(columns=['group_name'], inplace=True)  # Remove the temporary column
    group_df.to_csv(output_file_path, index=False)
    print(f'File created: {output_file_path}')
