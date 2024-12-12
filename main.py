import requests
from ollama import Client
import re


#Ollama setup
client = Client(
    host="http://localhost:11434"
)

#Doc split because of ocr limit
lex_docs = ["lex_doc-1.pdf", "lex_doc-2.pdf", "lex_doc-3.pdf", "lex_doc-4.pdf", "lex_doc-5.pdf", "lex_doc-6.pdf", "lex_doc-7.pdf", "lex_doc-8.pdf", "lex_doc-9.pdf", "lex_doc-10.pdf", "lex_doc-11.pdf", "lex_doc-12.pdf","lex_doc-13.pdf","lex_doc-14.pdf","lex_doc-15.pdf",]
cleaned_docs = []

def preprocess_text(text):
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text) 
    return cleaned_text

#Sets up the ocr scan function, got most of the code from public documentation
def ocr_fun(filename, overlay=False, api_key='K83267503988957', language='eng'):

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

#A prompt for specific cleaning instructions for the llama model
def clean_text(ocr_file):
    try:

        ocr_file = preprocess_text(ocr_file)

        prompt_text = (
    f"Extract the main content from this text. Keep only the names and what each person says. Format the output as `Name: Dialogue`. "
    f"When formating don't specifically say `Name` or `Dialogue`, but use the actual names and dialogue from the text. "
    f"If there is a space between an appostrophe and the next word, remove the space. For example, `it ' s` should be `it's`. "
    f"Remove metadata, comments, timestamps, garbled characters, and irrelevant details. If any text is incomplete or unreadable, omit it entirely. "
    f"Remove garbled characters (like �) and other unwanted symbols. Again, if there is no dialogue available, delete the line. "
    f"Don't rewrite any text whatsoever; keep it the same dialogue from the OCR. Here's the input text:\n\n{ocr_file}"
)

        response = client.generate(
            model="llama3.2",
            prompt=prompt_text
        )
        
        return response.get("response", "Failed to clean text. Response missing.")
    except Exception as e:
        return f"Error during text cleaning: {str(e)}"

#Loops all documents and processes them
for lex_doc in lex_docs:
    print(f"processing: {lex_doc}")
    ocr_file = ocr_fun(filename=lex_doc)
    cleaned_text = clean_text(ocr_file)
    cleaned_docs.append(cleaned_text)

#Writes the cleaned text to a file
with open('response.txt', 'w') as f: 
    for llama_docs in cleaned_docs:
        f.write(llama_docs)

