import pandas as pd
import sacrebleu

def read_sentences_from_csv(file_path, column_name):
    df = pd.read_csv(file_path)
    return df[column_name].tolist()

def calculate_sacrebleu(generated_sentences, reference_sentences):
    bleu = sacrebleu.corpus_bleu(generated_sentences, [reference_sentences])
    return bleu.score

def run(generated_path, reference_path, result_path):
    # Replace these with the paths to your CSV files
    generated_file_path = generated_path
    reference_file_path = reference_path
    output_file_path = result_path

    # Read sentences from CSV files
    generated_df = pd.read_csv(generated_file_path)
    reference_df = pd.read_csv(reference_file_path)

    # Check if lengths, 'task_name', 'index', and 'model_name' match
    if not all([
        len(generated_df) == len(reference_df),
        all(generated_df['task_name'] == reference_df['task_name']),
        all(generated_df['index'] == reference_df['index']),
        all(generated_df['model_name'] == generated_df['model_name'].iloc[0])
    ]):
        print("Error: Data mismatch between generated and reference files.")
        return

    # Calculate SacreBLEU score for each row
    scores = []
    for index, row in generated_df.iterrows():
        generated_sentences = row['result'].split('\n')
        reference_sentences = reference_df.loc[index, 'answer'].split('\n')

        bleu_score = calculate_sacrebleu(generated_sentences, reference_sentences)
        scores.append(bleu_score)

    # Add scores to the output DataFrame
    output_df = generated_df[['task_name', 'index', 'model_name']].copy()
    output_df['prompt'] = reference_df['prompt']
    output_df['output'] = generated_df['result']
    output_df['score'] = scores

    # Save the output DataFrame to a new CSV file
    output_df.to_csv(output_file_path, index=False)

    print(f"SacreBLEU scores saved to {output_file_path}")

if __name__ == '__main__':
    reference_path = "ex_reference.csv"
    generated_path = "ex_generated.csv"
    result_path = "ex_result.csv"

    run(reference_path=reference_path, generated_path=generated_path, result_path=result_path)
