import os
import csv

def merge_csv_files(directory):
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    # Sort files in alphanumeric order
    csv_files.sort()

    # Create a new CSV file for the merged data
    output_file_name = os.path.join(directory, f"../{directory}.csv")
    with open(output_file_name, 'w', encoding='utf8', newline='') as output_file:
        csv_writer = csv.writer(output_file)

        # Write header from the first CSV file
        with open(os.path.join(directory, csv_files[0]), 'r', encoding='utf8') as first_file:
            header = next(csv.reader(first_file))
            csv_writer.writerow(header)

        # Merge data from all CSV files
        for csv_file in csv_files:
            with open(os.path.join(directory, csv_file), 'r', encoding='utf8') as input_file:
                # Skip header in subsequent files
                next(input_file)
                # Copy data to the output file
                csv_writer.writerows(csv.reader(input_file))

    print(f"Merged data saved to: {output_file_name}")

def merge_all_csv_files_in_path(path):
    # Get all directories in the given path
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # Process each directory
    for directory in directories:
        current_directory = os.path.join(path, directory)
        merge_csv_files(current_directory)

if __name__ == "__main__":
    # Specify the path where directories with CSV files are located
    target_path = "."

    # Merge all CSV files in the specified path
    merge_all_csv_files_in_path(target_path)
