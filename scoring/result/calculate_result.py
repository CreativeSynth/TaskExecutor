import os
import csv

def calculate_average(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        values = [float(row[-1]) for row in reader]
        return sum(values) / len(values)

def process_directory(directory):
    result_file_path = os.path.join(directory, f'{os.path.basename(directory)}_result.csv')
    
    with open(result_file_path, 'w', newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerow(['task', 'average score'])

        data = []

        for filename in os.listdir(directory):
            if filename.endswith('.csv') and filename != f'{os.path.basename(directory)}_result.csv':
                file_path = os.path.join(directory, filename)
                average = calculate_average(file_path)
                data.append([filename, average])
        
        data.sort(key=lambda x: x[0])

        writer.writerows(data)

    print(f'Processed: {result_file_path}')

def main():
    for root, dirs, files in os.walk('.'):
        for directory in dirs:
            process_directory(os.path.join(root, directory))

if __name__ == "__main__":
    main()
