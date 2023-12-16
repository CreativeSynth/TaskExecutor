import csv, difflib

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
            return
        
        if ref_row[0] != task_name: # task mixed in reference
            print(ref_row)
            print("Error: task mixed in reference!")
            return
        
        if gen_row[0] != task_name: # task mixed in generated
            print(gen_row)
            print("Error: task mixed in generated!")
            return
        
        if gen_row[3] != model_name: # model mixed in generated
            print(gen_row)
            print("Error: model mixed in generated!")
            return
        
    print("Matching successful!")

    def score(before, ref_answer, gen_answer):
        def generate_diff(before, after):
            differ = difflib.Differ()
            diff = list(differ.compare(before.split(), after.split()))

            result = []
            element = ['', '']

            for item in diff:
                if item.startswith(' ') and element != ['', '']:
                    element = [s.strip() for s in element]
                    result.append(element)
                    element = ['', '']
                elif item.startswith('- '):
                    element[0] += item[1:]
                elif item.startswith('+ '):
                    element[1] += item[1:]

            return result

        ref_diff = generate_diff(before, ref_answer)
        gen_diff = generate_diff(before, gen_answer)
        common = [element for element in ref_diff if element in gen_diff]

        R = len(common) / len(ref_diff)
        P = len(common) / len(gen_diff)
        F = (1.25 * R * P) / (R + 0.25 * P)

        return F

    writer.writerow(['task_name', 'index', 'model_name', 'prompt', 'output', 'score'])

    for ref_row, gen_row in zip(ref_data, gen_data):
        writer.writerow([task_name, ref_row[1], model_name, ref_row[2], gen_row[2], score(ref_row[2][50:], ref_row[3], gen_row[2])])

if __name__ == '__main__':
    reference_path = "ex_reference.csv"
    generated_path = "ex_generated.csv"
    result_path = "ex_result.csv"

    run(reference_path=reference_path, generated_path=generated_path, result_path=result_path)