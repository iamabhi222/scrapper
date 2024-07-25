import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import json

# Ensure you have installed NLTK and downloaded the 'punkt' tokenizer models.
# import nltk
# nltk.download('punkt')

# Function to read raw text from a file
def read_raw_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Function to extract meaningful sentences from a paragraph
def extract_sentences_from_paragraph(paragraph):
    # Tokenize the paragraph into sentences
    sentences = sent_tokenize(paragraph)
    # Filter out sentences with fewer than 12 words and tokenize each sentence into words
    meaningful_sentences = [sentence for sentence in sentences if len(sentence.split()) > 15]
    return meaningful_sentences

# Function to extract meaningful sentences from raw text
def extract_sentences(text):
    # Split the text into paragraphs (assuming paragraphs are separated by two newlines)
    paragraphs = text.split('\n\n')
    # Process each paragraph to extract meaningful sentences
    meaningful_sentences_per_paragraph = [extract_sentences_from_paragraph(paragraph) for paragraph in paragraphs]
    # Flatten the list of lists (paragraphs) into a single list of sentences
    meaningful_sentences = [sentence for paragraph in meaningful_sentences_per_paragraph for sentence in paragraph]
    return meaningful_sentences

# Function to save list of lists to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Main script
def get_sentences():
    input_filename = 'output.txt'  # Replace with your input file name
    output_filename = 'interM_sentences.json'  # Replace with your desired output file name

    # Read the raw text from the input file
    raw_text = read_raw_text(input_filename)

    # Extract meaningful sentences from the raw text
    meaningful_sentences = extract_sentences(raw_text)

    # Save the meaningful sentences to the output file
    save_to_json(meaningful_sentences, output_filename)

    print(f"Extracted {len(meaningful_sentences)} meaningful sentences and saved to {output_filename}")
