# import asyncio # async functionality in python (dynamic loading)
from langchain_community.document_loaders import PyPDFLoader

def parse():
    file_path = "./us_epa_grant_agreement.pdf"
    # file_path = "./ks_grant_reward.pdf"
    loader = PyPDFLoader(file_path)
    pages = []
    # async for page in loader.alazy_load():
    for page in loader.lazy_load():
        pages.append(page)
        
    return pages

if __name__=="__main__":
    pages = parse()
    print(f"{pages[0].metadata}\n")
    print(pages[0].page_content)
