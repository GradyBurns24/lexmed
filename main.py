import requests
from PIL import Image
import pytesseract
from ollama import Client
import pdf2image
import re

with open("response.txt", "w") as f:
    f.write("")
#Ollama setup
client = Client(
    host="http://localhost:11434"
)

lex_docs = ["lex_doc-1.pdf", "lex_doc-2.pdf", "lex_doc-3.pdf", "lex_doc-4.pdf", "lex_doc-5.pdf", "lex_doc-6.pdf", "lex_doc-7.pdf", "lex_doc-8.pdf", "lex_doc-9.pdf", "lex_doc-10.pdf", "lex_doc-11.pdf",]
cleaned_docs = []





def preprocess_text(text):
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text) 
    return cleaned_text




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

def clean_text(ocr_file):
    try:

        ocr_file = preprocess_text(ocr_file)

        prompt_text = (
            f"Extract the main content from this text. Keep only the names and what each person says. Format the output as `Name: Dialogue`. Remove metadata, comments, timestamps, garbled characters, and irrelevant details. If any text is incomplete or unreadable, omit it entirely. Remove garbled characters (like �) and other unwanted symbols. Here's the input text:\n\n{ocr_file}"
        )
        response = client.generate(
            model="llama3.2",
            prompt=prompt_text
        )
        
        return response.get("response", "Failed to clean text. Response missing.")
    except Exception as e:
        return f"Error during text cleaning: {str(e)}"

    

for lex_doc in lex_docs:
    ocr_file = ocr_fun(filename=lex_doc)
    cleaned_text = clean_text(ocr_file)
    cleaned_docs.append(cleaned_text)

cleaned_docs.reverse()

with open('response.txt', 'a') as f: 
    for llama_docs in cleaned_docs:
        f.write(llama_docs + '\n')
