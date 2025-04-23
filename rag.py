'''
    script that holds all model-related functions
'''

## SIMILARITY SEARCH STAGE
'''
- issues: needs contextual compression
'''
def sim_search(query, k, vector_store):    
    docs = vector_store.similarity_search(query, k) # TODO can play experiment w/ k value
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
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
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
You are a professional analyst specializing in grants and legal funding information. Your job is to extract structured information from legal documents.

Use the context provided to answer the question. Format your output as **valid JSON** matching the structure described below. 

‼️ Important instructions:
- ONLY report the variables stated in the format and NOTHING MORE. Do NOT report any other variables!
- Do NOT include explanations, comments, or text before or after the JSON curly braces like `json ... `.
- Return a valid JSON object only. Make sure it can be parsed with json.loads().
- If a value is not found, use an empty string or an empty list.

Context:
{context}

Question:
{question}

Format:
{format_instructions}
    """,
    input_variables=["context", "question"],
    partial_variables={"format_instructions": output.get_format_instructions()},)

    chain = prompt | llm | output
    response = chain.invoke({"context": context, "question": question})
    # response = chain.invoke({"context": context, "question": question})
        
    return response


# TODO can experiment with what metrics want through pydantic objects
class Project(BaseModel):
    name: str = Field(..., description="Name or title of the project or program")
    start_date: str = Field(..., description="Start date of the project in MM/DD/YYYY or YYYY-MM-DD format")
    end_date: str = Field(..., description="End date of the project in MM/DD/YYYY or YYYY-MM-DD format")

class GeneralGrantInfo(BaseModel):
    grant_name: str = Field(..., description="The official name or title of the grant")
    projects: list[Project] = Field(..., description="List of projects funded by this grant, each with a name, start date, and end date")
    
class Other(BaseModel):
    obj: str = Field(..., description="A specific object or item receiving funding under 'other' spending")
    cost: int = Field(..., description="Cost amount allocated to this object in USD")

class SpendingInfo(BaseModel):
    total: int = Field(..., description="Total amount of grant funding in USD")
    fringe: int = Field(..., description="Amount for fringe benefits such as insurance, retirement, etc.")
    indirect: int = Field(..., description="Amount for indirect costs like rent, administrative overhead, and utilities")
    travel: int = Field(..., description="Amount allocated to travel-related expenses")
    equipment: int = Field(..., description="Amount allocated to equipment purchases")
    other: list[Other] = Field(..., description="List of other individual items or objects that received funding, with their respective cost")

    
class BudgetInfo(BaseModel):
    position: str = Field(description="Position name")
        
## OUTPUT PARSING
def determine_pyobj(key):            
    if key == "general":        
        return GeneralGrantInfo    
    elif key == "spending":
        return SpendingInfo

