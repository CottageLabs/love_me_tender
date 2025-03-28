# Love me tender

An example application to answer questions using open ai, based on documents we feed.

Note: It does not support csv files

## Usage

Add all your data in the `data` folder.

```
# initialise
love_me_tender = LoveMeTender('data', 'tender_vector_store')
# Create a vector store with your data
love_me_tender.upload_data()
# Get answers to your question
love_me_tender.get_answer('What are the features of your repository')
```

Reference:
* https://platform.openai.com/docs/guides/retrieval#synthesizing-responses
