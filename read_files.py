import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import sqlite3

# Initialize Azure Text Analytics Client
key = "b8e6ac2cfda244dd848a823511255a0b"
endpoint = "https://hackathonservice.openai.azure.com/"
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Function to analyze text with Azure OpenAI
def analyze_text(text):
    response = text_analytics_client.analyze_sentiment(documents=[text])[0]
    return response

# Read text file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Store data in SQLite database
def store_in_database(file_name, response):
    # Connect to SQLite database (it will create one if it doesn't exist)
    conn = sqlite3.connect('azure_responses.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS responses
                      (filename TEXT, sentiment TEXT, positive_score REAL, neutral_score REAL, negative_score REAL)''')

    # Insert data
    cursor.execute('INSERT INTO responses VALUES (?, ?, ?, ?, ?)', (
        file_name,
        response.sentiment,
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative
    ))

    # Commit and close
    conn.commit()
    conn.close()

# Path to the single text file
file_path = '/home/jephuneh/Desktop/637hac/qaribu/files/Job_Descriptions.txt'

# Read text from file
file_name = os.path.basename(file_path)
text = read_text_file(file_path)

# Analyze text with Azure OpenAI
response = analyze_text(text)

# Store the result in the database
store_in_database(file_name, response)

print("File has been processed and stored in the database.")
