import os
import csv

def calculate_average(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        values = [float(row[-1]) for row in reader]
        return sum(values) / len(values)

def process_directory(directory):
    data = []

    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename != f'{os.path.basename(directory)}_result.csv':
            file_path = os.path.join(directory, filename)
            average = calculate_average(file_path)
            data.append([filename, average])
    
    data.sort(key=lambda x: x[0])

    return (directory, data)

def main():
    tasks = ['ko_quiz_1', 'ko_quiz_2', 'ko_quiz_3', 'ko_quiz_4', 'ko_quiz_5', 'ko_quiz_6', 'ko_quiz_7', 'ko_quiz_8',
             'nli', 'number_1', 'number_2', 'number_3', 'reasoning', 'spelling_correct', 'summarization', 'translation']
    data = []
    for root, dirs, files in os.walk('.'):
        for directory in dirs:
            result = process_directory(os.path.join(root, directory))
            if [i[0].replace('.csv', '') for i in result[1]] != tasks:
                print('Error: missing data in', directory)
                continue
            data.append((result[0], [i[1] for i in result[1]]))
    
    writer = csv.writer(open('result.csv', mode='w', encoding='utf8', newline=''))
    writer.writerow(['task_name'] + [i[0].replace('./', '') for i in data])
    for i in range(len(tasks)):
        writer.writerow([tasks[i]] + [row[1][i] for row in data])

if __name__ == "__main__":
    main()
