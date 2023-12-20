import os, csv

# Import all scoring functions
from methods.ko_quiz_3.eval_ko_quiz_3               import run as run_ko_quiz_3
from methods.multiple_choice.eval_multiple_choice   import run as run_multiple_choice
from methods.number_1.eval_number_1                 import run as run_number_1
from methods.number_3.eval_number_3                 import run as run_number_3
from methods.reasoning.eval_reasoning               import run as run_reasoning
from methods.spelling_correct.eval_spelling_correct import run as run_spelling_correct
from methods.summarization.eval_summarization       import run as run_summarization
from methods.translation.eval_translation           import run as run_translation

# Settings: enter the target files here!
# Start with '/TaskExecutor'!
target_folders = [
          '/TaskExecutor/gemini/'
          ]
file_names = ['ko_quiz_1_result.csv',
              'ko_quiz_2_result.csv',
              'ko_quiz_3_result.csv',
              'ko_quiz_4_result.csv',
              'ko_quiz_5_result.csv',
              'ko_quiz_6_result.csv',
              'ko_quiz_7_result.csv',
              'ko_quiz_8_result.csv',
              'nli_result.csv',
              'number_1_result.csv',
              'number_2_result.csv',
              'number_3_result.csv',
            #   'reasoning_result.csv',
              'spelling_correct_result.csv',
            #   'summarization_result.csv',
              'translation_result.csv']
target = [(target_folder + file_name) for target_folder in target_folders for file_name in file_names]

# Evaluate methods
methods = {'ko_quiz_1'        : 'multiple_choice',
           'ko_quiz_2'        : 'multiple_choice',
           'ko_quiz_3'        : 'ko_quiz_3',
           'ko_quiz_4'        : 'multiple_choice',
           'ko_quiz_5'        : 'multiple_choice',
           'ko_quiz_6'        : 'multiple_choice',
           'ko_quiz_7'        : 'multiple_choice',
           'ko_quiz_8'        : 'multiple_choice',
           'nli'              : 'multiple_choice',
           'number_1'         : 'number_1',
           'number_2'         : 'multiple_choice',
           'number_3'         : 'number_3',
           'reasoning'        : 'reasoning',
           'spelling_correct' : 'spelling_correct',
           'summarization'    : 'summarization',
           'translation'      : 'translation',
           'translate'        : 'translation'
           }

# Calculate current position
current_position = os.getcwd()
current_position = current_position[current_position.find('/TaskExecutor'):]

for file in target:
    print('Start evaluating', file)

    generated_path = os.path.relpath(file, current_position)

    reader = csv.reader(open(generated_path, "rt", encoding='utf8', newline=''))
    next(reader)
    first_row = next(reader)

    # Get data information: task_name, model_name
    task_name, model_name = first_row[0], first_row[3]

    # Set run function
    try:
        run = globals()['run_' + methods[task_name.split('/')[0]]]
    except:
        print('Error setting run function.')
        continue

    reference_path = '/TaskExecutor/../TaskManager/ko_quiz/' + task_name + '.csv' if 'ko_quiz' in task_name else '/TaskExecutor/../TaskManager/' + task_name + '/' + task_name + '.csv' if '/' not in task_name else '/TaskExecutor/../TaskManager/translation/translation.csv'
    reference_path = os.path.relpath(reference_path, current_position)

    result_path = '/TaskExecutor/scoring/result/' + model_name + '/' + (task_name if '/' not in task_name else 'translation') + '.csv'
    result_path = os.path.relpath(result_path, current_position)

    try:
        run(reference_path, generated_path, result_path)
    except Exception as e:
        print(e)