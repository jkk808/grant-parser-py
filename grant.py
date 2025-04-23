'''
    main script that generates json of grant data
'''

from parser import parse
from rag import *
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import argparse
argparser = argparse.ArgumentParser(description="Parse a grant file (.pdf)")
argparser.add_argument("filepath", type=str, help="Path to the grant pdf file")
argparser.add_argument("k", type=int, help="# nearest neighbors to retrieve for similarity search")
args = argparser.parse_args()

print("Loading PDF...")
pages = parse(args.filepath)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = InMemoryVectorStore.from_documents(pages, embeddings)

# queries = {
#     "general": ["grant name", "project names", "start and end dates",],
#     "spending": ["salary", "indirect", "travel", "supplies", "fringe"],
#     # "budget": ["per position", "per position program"]
# }
llm_queries = {
    "general": "What is the title of the grant? List all programs or projects stated, including each project or programs' name, start dates/periods and end dates/periods.",
    "spending": "What is the total award amount? Break down the spending into: fringe benefits, indirect costs, travel, equipment, and other. For “other,” provide a list of items with their names and cost."

}
vec_queries = {
    "general": "Information about any programs' or projects' name/title, the start and end dates/periods, and the official name of the grant agreement.",
    "spending": "Details about total funding, and how the grant money is allocated — including fringe benefits, indirect costs, travel, equipment, and other types of spending."
}
import json
grant_json = {}

# go through each batch of queries to efficiently/accurately get the proper data from pdf
for query in llm_queries:    
    # # form query string
    # vars = "" 
    # for var in queries[query]:
    #     vars += (f"{var}, ")        
    # question = f"What is the {vars}stated in this grant file?"
    print("Similar searching...")
    vec_question = vec_queries[query]
    print("Q: ", vec_question)                
    context = sim_search(vec_question, args.k, vector_store)
    py_obj = determine_pyobj(query)
    print("Context: ", context)
    
    print("Asking LLM...")
    llm_question = llm_queries[query]
    print("Q: ", llm_question)
    response = retrieve_data_from_llm(llm_question, context, py_obj)
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