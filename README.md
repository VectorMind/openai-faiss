# streamlit-openai-faiss
Lang chain example using open AI and FAISS

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

## references
- https://github.com/alejandro-ao/langchain-ask-pdf/tree/main

