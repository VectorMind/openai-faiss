import tiktoken

#encoding = tiktoken.get_encoding("cl100k_base")
#encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
encoding = tiktoken.encoding_for_model("text-embedding-ada-002")

text_input = open("context_very_small.txt").read()
#text_input = "This is a test for tokens count and decoding"
tokens = encoding.encode(text_input)
print(len(tokens))

decoded_text = [encoding.decode_single_token_bytes(token) for token in tokens]

print(decoded_text)
