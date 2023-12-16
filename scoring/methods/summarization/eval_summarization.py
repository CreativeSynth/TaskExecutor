# The rows of the two csv files should be perfectly matched!

from bert_score import score as bertscore
import os, csv

# Settings
score_type = "f1" # p -> precision, r -> recall, f1 -> f1 score

if score_type not in ['p', 'r', 'f1']:
    print("Error: wrong score type!")
    exit()

def run(reference_path, generated_path, result_path):
    reference_file = open(reference_path, "rt", encoding='utf8', newline='')
    generated_file = open(generated_path, "rt", encoding='utf8', newline='')
    result_file = open(result_path, "wt", encoding='utf8', newline='')

    ref_reader = csv.reader(reference_file)
    gen_reader = csv.reader(generated_file)
    writer = csv.writer(result_file)

    next(ref_reader)
    next(gen_reader)

    ref_data = [row for row in ref_reader]
    gen_data = [row for row in gen_reader]

    task_name, model_name = gen_data[0][0], gen_data[0][3]

    for ref_row, gen_row in zip(ref_data, gen_data):
        if ref_row[1] != gen_row[1]: # index not match
            print(f"Ref: {ref_row[0]} {ref_row[1]} / Gen: {gen_row[0]} {gen_row[1]}")
            print("Error: index not match!")
            exit()
        
        if ref_row[0] != task_name: # task mixed in reference
            print(ref_row)
            print("Error: task mixed in reference!")
            exit()
        
        if gen_row[0] != task_name: # task mixed in generated
            print(gen_row)
            print("Error: task mixed in generated!")
            exit()
        
        if gen_row[3] != model_name: # model mixed in generated
            print(gen_row)
            print("Error: model mixed in generated!")
            exit()
        
    print("Matching successful!")

    P, R, F1 = bertscore([row[2] for row in gen_data], [row[3] for row in ref_data], lang='ko', verbose=True)
    my_score = (P if score_type == 'p' else R if score_type == 'r' else F1).tolist()

    writer.writerow(['task_name', 'index', 'model_name', 'prompt', 'output', 'score'])

    for score, row, ref_row in zip(my_score, gen_data, ref_data):
        writer.writerow([task_name, row[1], model_name, ref_row[2], row[2], score])

if __name__ == '__main__':
    reference_path = "ex_reference.csv"
    generated_path = "ex_generated.csv"
    result_path = "ex_result.csv"

    run(reference_path=reference_path, generated_path=generated_path, result_path=result_path)