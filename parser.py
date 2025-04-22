# import asyncio # async functionality in python (dynamic loading)
from langchain_community.document_loaders import PyPDFLoader

def parse(file):
    loader = PyPDFLoader(file)
    pages = []
    # async for page in loader.alazy_load():
    for page in loader.lazy_load():
        pages.append(page)
        
    return pages

if __name__=="__main__":
    pages = parse()
    print(f"{pages[0].metadata}\n")
    print(pages[0].page_content)
