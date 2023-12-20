import csv, os

# Settings:
input_files = [
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_1_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_2_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_3_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_4_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_5_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_6_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_7_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/ko_quiz_8_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/nli_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/number_1_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/number_2_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/number_3_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/reasoning_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/spelling_correct_result.csv',
    # '/TaskExecutor/ko_vicuna/grouped_results/before_sorting/summarization_result.csv',
    '/TaskExecutor/koalpaca5.8b/grouped_results/before_sorting/translation_result.csv',
    ]
output_files = [input_path.replace('before_sorting/', '') for input_path in input_files]

# Calculate current position
current_position = os.getcwd()
current_position = current_position[current_position.find('/TaskExecutor'):]

def custom_sort_key(row):
    first_column_value = row[0]
    if '/' in first_column_value:
        # If the value contains '/', sort based on custom order
        custom_order = ['translation/techsci', 'translation/socialsci', 'translation/dailylife',
                        'translation/basicsci', 'translate/media', 'translation/humanities']
        return (custom_order.index(first_column_value), int(row[1]))
    else:
        # If the value does not contain '/', sort by int(row[1])
        return int(row[1])


def sort_csv_files(input_file_paths, output_file_paths):
    if len(input_file_paths) != len(output_file_paths):
        raise ValueError("Input and output file paths must have the same length.")

    for input_path, output_path in zip(input_file_paths, output_file_paths):
        input_path = os.path.relpath(input_path, current_position)
        output_path = os.path.relpath(output_path, current_position)

        # Read the CSV file into a list of lists
        with open(input_path, 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = list(reader)

        # Sort the data based on the second column (converted to integers)
        data.sort(key=custom_sort_key)

        # Write the sorted data to a new CSV file
        with open(output_path, 'w', encoding='utf8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)

        print(f"Rows in {input_path} have been sorted based on the second column in increasing order. "
              f"The sorted data has been written to {output_path}.")

sort_csv_files(input_files, output_files)