### Different test run folders are here

# NOTES 
## Working with the larger models:
- k values of 2 give best results overall (anything higher leads to hallucinating)
- best prompting style is seperate questions for the similarity search and for the llm (cannot be the same)
- make each pydantic object field very descriptive

### KS PDF (most stable)
- k of 2
- split-prompting

