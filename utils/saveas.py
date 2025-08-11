import os
import json
import pandas as pd

# Save as XML
def save_xml(pmc_id, full_text, save_folder):
    if full_text:
        file_path = os.path.join(save_folder, f"{pmc_id}.xml")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(full_text)
            print(f"Saved full text for PMC ID {pmc_id} to {file_path}")
        except Exception as e:
            print(f"Error saving full text for PMC ID {pmc_id}: {e}")

# Save as JSON
def save_json(data, output_file):
    """
    Saves data to a JSON file.

    Args:
        data (dict): Data to save.
        output_file (str): Path to the JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f'Results saved to JSON: {output_file}')

# Save as CSV
def save_csv(data, output_file):
    """
    Saves data to a CSV file.

    Args:
        data (dict): Data to save.
        output_file (str): Path to the CSV file.
    """
    records = []
    for file, results in data.items():
        for step, answer in results.items():
            records.append({
                'File': file,
                'Step': step,
                'Answer': answer
            })
    
    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    print(f'Results saved to CSV: {output_file}')