import requests
from PIL import Image
import pytesseract
from ollama import Client
import pdf2image

with open("response.txt", "w") as f:
    f.write("erase")
#Ollama setup
client = Client(
    host="http://localhost:11434"
)

lex_docs = ["lex_doc-1.pdf", "lex_doc-2.pdf", "lex_doc-3.pdf", "lex_doc-4.pdf", "lex_doc-5.pdf", "lex_doc-6.pdf", "lex_doc-7.pdf", "lex_doc-8.pdf", "lex_doc-9.pdf", "lex_doc-10.pdf", "lex_doc-11.pdf",]
cleaned_docs = []

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
        # Query the Ollama API with the text
        prompt_text = (
            f"Extract the main content from this text. Keep only the names and what each person says. Format the output as `Name: Dialogue`. Remove metadata, comments, and other irrelevant details such as timestamps, footnotes, or non-dialogue content. Preserve the speaker's name and exact words. Here's the input text:\n\n{ocr_file}")
        response = client.generate(
            model="llama3.2",  # Replace "cleaner" with the specific model you are using
            prompt=  prompt_text
        )
        
        # Extract the cleaned text from the response
        return response.get("response", "Failed to clean text. Response missing.")
    except Exception as e:
        # Handle any errors that occur during the query
        return f"Error during text cleaning: {str(e)}"
    

for lex_doc in lex_docs:
    ocr_file = ocr_fun(filename=lex_doc)
    cleaned_text = clean_text(ocr_file)
    cleaned_docs.append(cleaned_text)


for llama_docs in cleaned_docs:
    with open('response.txt', 'a') as f: 
        f.write(llama_docs + '\n')  
