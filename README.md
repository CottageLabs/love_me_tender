# Love me tender

An example application to answer questions using open ai, based on documents we feed.

Note: It does not support csv files

## Usage

Add all your data in the `data` fiolder

```
# initialise
l = LoveMeTender('data')
# Create a vector store with your data
l.create_vector_store()
# Get answers to your question
l.get_answer('What are the features of your repository')
```

Reference: https://platform.openai.com/docs/guides/retrieval#synthesizing-responses

