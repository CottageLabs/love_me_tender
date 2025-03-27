# Love me tender
# Semantic search of tenders using open ai vectors
import os
from os.path import isfile, join
from openai import OpenAI
from dotenv import load_dotenv
# loading variables from .env file


class LoveMeTender:
    def __init__(self, dir_path):
        if not os.path.exists(dir_path):
            raise Exception("path does not exist")
        load_dotenv()
        API_KEY = os.getenv("OPEN_AI_API_KEY")
        self.dir_path = dir_path
        self.ai_client = OpenAI(api_key=API_KEY)
        self.vector_store = self.ai_client.vector_stores.create(
            # Create vector store
            name="Love me tender",
        )

    def create_vector_store(self):
        list_of_files = self._get_list_of_files()
        for f in list_of_files:
            self.ai_client.vector_stores.files.upload_and_poll(  # Upload file
                vector_store_id=self.vector_store.id,
                file=open(f, "rb")
            )

    def get_answer(self, user_query):
        results = self._search_vector_store(user_query)
        formatted_result = self._synthesize_result(results, user_query)
        print(formatted_result)

    def _get_list_of_files(self):
        list_of_files = []
        for f in os.listdir(self.dir_path):
            file_path = join(self.dir_path, f)
            if isfile(file_path):
                list_of_files.append(file_path)
        return list_of_files

    def _search_vector_store(self, user_query):
        results = self.ai_client.vector_stores.search(
            vector_store_id=self.vector_store.id,
            query=user_query,
        )
        return results

    def _synthesize_result(self, results, user_query):
        formatted_results = self._format_results(results)

        # '\n'.join('\n'.join(c.text) for c in result.content for result in results.data)

        completion = self.ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "Produce a concise answer to the query based on the provided sources."
                },
                {
                    "role": "user",
                    "content": f"Sources: {formatted_results}\n\nQuery: '{user_query}'"
                }
            ],
        )
        return completion.choices[0].message.content

    def _format_results(self, results):
        formatted_results = ''
        for result in results.data:
            # formatted_result = f"<result file_id='{result.file_id}' file_name='{result.file_name}'>"
            formatted_result = f"<result file_id='{result.file_id}'>"
            for part in result.content:
                formatted_result += f"<content>{part.text}</content>"
            formatted_results += formatted_result + "</result>"
        return f"<sources>{formatted_results}</sources>"


if __name__ == "__main__":
    l = LoveMeTender('data')
    l.create_vector_store()
    l.get_answer('What are the features of your repository')

