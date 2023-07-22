# openai-faiss
experimenting with openAI and FAISS for custom content question answering

# Notebooks

* [langchain.ipynb](langchain.ipynb) simple example of custom chunks question answering with langchain
* [website_chunks.ipynb](website_chunks.ipynb) creating text chunks from all pages taken from sitemap
* [question_chunks.ipynb](question_chunks.ipynb) extracting relevant chunks to the question and feeding them as context. although it is much easier to use langchain the goal of this notebook is to explore the native openai and FAISS without the langchain abstraction

# Python scripts
## openai_faiss.py
* https://platform.openai.com/docs/guides/embeddings
* https://platform.openai.com/docs/api-reference/embeddings

this script only goes up to embeddings extraction, the full process is covered by [website_chunks.ipynb](website_chunks.ipynb)

## langchain_streamlit.py
* streamlit for ui
* langchain
    * Character Text Splitter
    * Open AI Embeddings (text-embedding-ada-002-v2)
    * Open AI LLM (text-davinci)
    * FAISS vector store
## very small example

* uploaded file [context_very_small.txt](./context_very_small.txt)
* question `How can MQTT help the consumer network ?`
* result using the single chunk 0
    * answer `MQTT reduces the overhead in comparison to REST API, allowing for more efficient communication between clients and servers. It also enables client polling and server based events notification, allowing for more flexibility in the client-server architecture.`

log
```shell
Tokens Used: 284
        Prompt Tokens: 240
        Completion Tokens: 44
Successful Requests: 1
Total Cost (USD): $0.005679999999999999
```

account usage
```text
text-embedding-ada-002-v2, 3 requests
348 prompt + 0 completion = 348 tokens

text-davinci, 1 request
240 prompt + 44 completion = 284 tokens
```

Pricing as of 21.07.2023
* Embeddings : Ada v2	$0.0001 / 1K tokens

## references
- https://github.com/alejandro-ao/langchain-ask-pdf/tree/main
- https://openai.com/pricing
