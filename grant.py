from parser import parse
from rag import *

# embedding model ==> vector representation of text
from langchain_ollama import OllamaEmbeddings

# embed docs & embed input to compare vectors (stores in memory)
from langchain_core.vectorstores import InMemoryVectorStore
print("Loading PDF...")
pages = parse()
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = InMemoryVectorStore.from_documents(pages, embeddings)

queries = {
    "general": ["grant name", "project name", "start and end date",],
    "spending": ["salary", "indirect", "travel", "supplies", "fringe"],
    "budget": ["per position", "per position program"]
}

import json
grant_json = {}

# go through each batch of queries to efficiently/accurately get the proper data from pdf
for query in queries:    
    # form query string
    vars = "" 
    for var in queries[query]:
        vars += (f"{var}, ")        
    question = f"What is the {query} {vars}stated in this grant reward?"
    print("Q: ", question)                
    
    print("Similar searching...")
    context = sim_search(question, 2, vector_store)
    py_obj = determine_pyobj(query)
    print("Got context")
    
    print("Asking LLM...")
    response = retrieve_data_from_llm(question, context, py_obj)
    print("response: ", response)
    
    print("Updating grant json...")
    x = json.loads(json.dumps(grant_json))
    x.update(response)
    print(json.dumps(x))
    grant_json = x
    
# write to json file
obj = json.dumps(grant_json, indent=4)
with open("grant.json", "w") as outfile:
    outfile.write(obj)