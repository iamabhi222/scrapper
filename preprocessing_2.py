import re
import json

# Function to determine if a sentence is meaningful
def is_meaningful(sentence):
    # Remove newline characters and excessive whitespace
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    
    # Remove sentences that contain more numbers than words
    words = sentence.split()
    num_count = sum(1 for word in words if word.isdigit())
    if num_count > len(words) / 2:
        return False

    # Remove sentences that are too short or contain excessive special characters
    if len(sentence) < 10 or re.search(r'^[^A-Za-z]*$', sentence):
        return False
    
    # Check for a reasonable amount of alphabetic content
    alpha_count = sum(c.isalpha() for c in sentence)
    if alpha_count < len(sentence) / 2:
        return False

    return True

# Function to filter sentences
def filter_sentences(sentences):
    return [sentence for sentence in sentences if is_meaningful(sentence)]

# Function to clean each sentence
def clean_sentence(sentence):
    # Remove newline characters
    sentence = sentence.replace('\n', ' ')
    sentence = sentence.lower()
    # Remove unwanted special characters but keep basic punctuation and structural symbols
    sentence = re.sub(r'[^A-Za-z0-9À-ÖØ-öø-ÿ&,.!?;:\'\"\(\)\-\[\]{}@#\/\s]', '', sentence)
    # Remove excessive whitespace
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence

# Function to preprocess the document
def preprocess_document(sentences):
    cleaned_sentences = []
    for sentence in sentences:
        cleaned = clean_sentence(sentence)
        # Filter out sentences with less than or equal to 15 words
        if len(cleaned.split()) > 15 and is_meaningful(cleaned):
            cleaned_sentences.append(cleaned)
    return cleaned_sentences

# Function to save the cleaned sentences to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Main script
def cleaned_sentences():
    input_filename = 'interM_sentences.json'  # Replace with your input file name
    output_filename = 'cleaned_sentences.json'  # Replace with your desired output file name

    # Read the sentences from the input file
    sentences = read_json_file(input_filename)

    # Preprocess the document
    cleaned_sentences = preprocess_document(sentences)

    # Save the cleaned sentences to the output file
    save_to_json(cleaned_sentences, output_filename)

    print(f"Cleaned sentences saved to {output_filename}")

# Function to read the JSON file
def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)
