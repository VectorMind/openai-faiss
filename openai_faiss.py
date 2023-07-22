import os
import openai
import json
from dotenv import load_dotenv

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


load_dotenv()
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

# can also be an array input
# each input must have max 8191 tokens for text-embedding-ada-002
input = "list"
if(input == "list"):
    json_data = load_json("extract_site/export/chunks.json")
    text_input = json_data[:10] #take first x10 to test with
else:
    text_input = open("context_very_small.txt").read()

response = openai.Embedding.create(
    input=text_input,
    model="text-embedding-ada-002",
    user="openai_faiss.py"
)
print(" -------- embeddings -------- ")
embeddings = response['data'][0]['embedding']
print(len(embeddings))
