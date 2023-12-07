import re, os, csv

# Settings
reference_path = "ex_reference.csv"
generated_path = "ex_generated.csv"
result_path = "ex_result.csv"

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

def extract_numbers(input_string):
    # Use regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', input_string)
    return numbers

writer.writerow(['task_name', 'index', 'model_name', 'score'])

for ref_row, gen_row in zip(ref_data, gen_data):
    writer.writerow([task_name, ref_row[1], model_name, 1 if extract_numbers(gen_row[2]) == [ref_row[3]] else 0])