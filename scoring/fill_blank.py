import os
import csv

# Calculate current position
current_position = os.getcwd()
current_position = current_position[current_position.find('/TaskExecutor'):]

def modify_csv_files(directory_string_tuples):
    for directory, replacement_string in directory_string_tuples:
        directory = os.path.relpath(directory, current_position)
        if not os.path.isdir(directory):
            print(f"Error: Directory '{directory}' does not exist.")
            continue

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                modify_csv_file(file_path, replacement_string)

def modify_csv_file(file_path, replacement_string):
    # Read the CSV file into a list of lists
    with open(file_path, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Check if the header is present
    if len(data) > 0:
        header = data[0]
    else:
        print(f"Error: File '{file_path}' is empty.")
        return

    # Modify the last column for each row (excluding the header)
    for row in data[1:]:
        if len(row) == len(header):
            last_column_index = len(header) - 1
            if row[last_column_index] == "":
                row[last_column_index] = replacement_string
            elif row[last_column_index] != replacement_string:
                print(f"Error: Value in the last column of file '{file_path}' is not identical to the input string.")
                print(row)
                return

    # Write the modified data back to the CSV file
    with open(file_path.replace('/before_filling', ''), 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Modified file '{file_path}'.")

# Example usage:
directories_and_strings = [
    ('/TaskExecutor/ko_vicuna/grouped_results/before_filling', 'ko_vicuna_7b'),
    # Add more directories and replacement strings as needed
]

modify_csv_files(directories_and_strings)
