### Different test run folders are here

# NOTES 
## Working with the larger models:
- k values of 2 give best results overall (anything higher leads to hallucinating)
- best prompting style is seperate questions for the similarity search and for the llm (cannot be the same)
- make each pydantic object field very descriptive
- may need example jsons to keep format valid

### KS PDF (most stable)
long corporate law paper
- k of 3
- split-prompting

### US EPA 
direct sectioned data pdf with the corporate things after
- postparsing wrapper for output parser to clean output
- took out keywords in vec_query like "funding" in general query
- moved order of keywords for the vec_query to grab the dates first (titles are arbitrary)
- moved format instructions higher in prompt template
- k of 2
- split-prompting