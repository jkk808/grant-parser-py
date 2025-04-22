'''
    script that holds all model-related functions
'''

## SIMILARITY SEARCH STAGE
'''
- issues: needs contextual compression
'''
def sim_search(query, k, vector_store):    
    docs = vector_store.similarity_search(query, k=2) # TODO can play experiment w/ k value
    context = ""
    for doc in docs:
        # print(f'Page {doc.metadata["page"]}: {doc.page_content}\n')
        context += doc.page_content
        
    return context

## LLM STAGE
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Dict
from dotenv import load_dotenv

def retrieve_data_from_llm(question, context, py_obj):
    load_dotenv()
    llm = ChatOpenAI(
        model=os.getenv("MODEL"),
        temperature=0,
        api_key=os.getenv("OPENAI_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )    
    
    output = JsonOutputParser(pydantic_object=py_obj)

    # system prompt
    prompt = PromptTemplate(
    template="""
    You are a professional in grant reading and legal information. Use the context to retrieve the variables wanted.
    Context: {context}
    Question: {question}
    {format_instructions}""",
    input_variables=["context", "question"],
    partial_variables={"format_instructions": output.get_format_instructions()},)

    chain = prompt | llm | output
    response = chain.invoke({"context": context, "question": question})

    return response


# TODO can experiment with what metrics want through pydantic objects
class Project(BaseModel):
    name: str
    start_date: str
    end_date: str
class GeneralGrantInfo(BaseModel):
    grant_name: str = Field(description="Name of the grant rewarded")
    projects: list[Project] = Field(description="List of projects, each with a name, start/end date")
    # can validate if want to
    
class BudgetInfo(BaseModel):
    position: str = Field(description="Position name")
    
class Other(BaseModel):
    obj: str
    cost: int
class SpendingInfo(BaseModel):
    total: int = Field(description="Total funding provided")
    fringe: int = Field(description="Fringe Benefits like insurance, retirement, etc.")
    indirect: int = Field(description="Indirect costs like rent/utilities")
    travel: int = Field(description="Travel costs")
    equipment: int
    other: list[Other] = Field(description="List of other object funding recieved")
        
## OUTPUT PARSING
def determine_pyobj(key):            
    if key == "general":        
        return GeneralGrantInfo    
    elif key == "spending":
        return SpendingInfo

