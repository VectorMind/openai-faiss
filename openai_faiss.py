import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

# can also be an array input
# each input must have max 8191 tokens for text-embedding-ada-002
text_input = open("context_very_small.txt").read()

response = openai.Embedding.create(
    input=text_input,
    model="text-embedding-ada-002",
    user="openai_faiss.py"
)
print(" -------- embeddings -------- ")
embeddings = response['data'][0]['embedding']
print(len(embeddings))
