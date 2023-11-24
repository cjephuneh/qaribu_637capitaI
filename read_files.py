import os
import requests
import sqlite3
from tqdm import tqdm

# Azure OpenAI endpoint and key
key = "b8e6ac2cfda244dd848a823511255a0b"
endpoint = "https://hackathonservice.openai.azure.com/"  # Modify with correct endpoint

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# Function to get text completion from Azure OpenAI
def get_text_completion(prompt):
    data = {
        "prompt": prompt,
        "max_tokens": 150  # Adjust as needed
    }
    response = requests.post(endpoint, headers=headers, json=data)
    return response.json()

# Read text file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Store data in SQLite database
def store_in_database(file_name, completion):
    # Connect to SQLite database
    conn = sqlite3.connect('openai_responses.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS responses
                      (filename TEXT, completion TEXT)''')

    # Insert data
    cursor.execute('INSERT INTO responses VALUES (?, ?)', (
        file_name,
        completion
    ))

    # Commit and close
    conn.commit()
    conn.close()

# Path to directory with text files
path_to_files = '/home/jephuneh/Desktop/637hac/qaribu/files'

# Loop through all text files in the directory
for file_name in os.listdir(path_to_files):
    if file_name.endswith('.txt'):
        file_path = os.path.join(path_to_files, file_name)
        text = read_text_file(file_path)

        # Get text completion from Azure OpenAI
        completion_response = get_text_completion(text)
        completion_text = completion_response.get("choices")[0].get("text") if completion_response.get("choices") else ""

        # Store the result in the database
        store_in_database(file_name, completion_text)


print("All files have been processed and stored in the database.")
