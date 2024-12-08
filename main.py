import requests
from PIL import Image
import pytesseract
from ollama import Client
import pdf2image


#Ollama setup
client = Client(
    host="http://localhost:11434"
)



def ocr_space_file(filename, overlay=False, api_key='K83267503988957', language='eng'):

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
            f"Take all the metadata out of this text and return only the main content:\n\n{ocr_file}")
        response = client.generate(
            model="llama3.2",  # Replace "cleaner" with the specific model you are using
            prompt=  prompt_text
        )
        
        # Extract the cleaned text from the response
        return response.get("response", "Failed to clean text. Response missing.")
    except Exception as e:
        # Handle any errors that occur during the query
        return f"Error during text cleaning: {str(e)}"
    


ocr_file = ocr_space_file(filename='lex_doc.pdf')
cleaned_text = clean_text(ocr_file)

print(cleaned_text)

'''with open('response.txt', 'w') as f:
    f.write(cleaned_text)
    f.close'''
