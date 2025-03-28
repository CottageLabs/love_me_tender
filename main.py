# Love me tender
# Semantic search of tenders using open ai vectors
import os
from os.path import isfile, join
from typing import Any, List

from dotenv import load_dotenv
from openai import OpenAI

# loading variables from .env file


class LoveMeTender:
    def __init__(self, dir_path: str, vector_store: str):
        """
        Initialize the LoveMeTender class with directory path and vector store name.
        """
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"Path does not exist: {dir_path}")
        load_dotenv()
        api_key: str = os.getenv("OPEN_AI_API_KEY")
        if not api_key:
            raise ValueError("OPEN_AI_API_KEY not found in environment variables")
        self.dir_path: str = dir_path
        self.ai_client: OpenAI = OpenAI(api_key=api_key)

        # Create vector store
        self.vector_store = self.ai_client.vector_stores.create(name=vector_store)

    def create_vector_store(self) -> None:
        """
        Create a vector store by uploading files from the directory.
        """
        list_of_files: List[str] = self._get_list_of_files()
        for file_path in list_of_files:
            with open(file_path, "rb") as file:
                self.ai_client.vector_stores.files.upload_and_poll(
                    vector_store_id=self.vector_store.id, file=file
                )

    def get_answer(self, user_query: str) -> None:
        """
        Search the vector store and synthesize the result.
        """
        results = self._search_vector_store(user_query)
        formatted_result: str = self._synthesize_result(results, user_query)
        print(formatted_result)

    def _get_list_of_files(self) -> List[str]:
        """
        Get a list of file paths from the directory.
        """
        return [
            join(self.dir_path, f)
            for f in os.listdir(self.dir_path)
            if isfile(join(self.dir_path, f))
        ]

    def _search_vector_store(self, user_query: str) -> Any:
        """
        Search the vector store with the user's query.
        """
        return self.ai_client.vector_stores.search(
            vector_store_id=self.vector_store.id, query=user_query
        )

    def _synthesize_result(self, results: Any, user_query: str) -> str:
        """
        Synthesize the search results into a formatted string.
        """
        formatted_results: str = self._format_results(results)
        completion = self.ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "Produce a concise answer to the "
                    "query based on the provided sources.",
                },
                {
                    "role": "user",
                    "content": f"Sources: {formatted_results}\n\nQuery: '{user_query}'",
                },
            ],
        )
        return completion.choices[0].message.content

    def _format_results(self, results: Any) -> str:
        """
        Format the search results into a string.
        """
        formatted_results: str = ""
        for result in results.data:
            formatted_result = f"<result file_id='{result.file_id}'>"
            for part in result.content:
                formatted_result += f"<content>{part.text}</content>"
            formatted_results += formatted_result + "</result>"
        return f"<sources>{formatted_results}</sources>"


if __name__ == "__main__":
    love_me_tender = LoveMeTender("data", "tender_vector_store")
    love_me_tender.create_vector_store()
    love_me_tender.get_answer("What are the features of your repository")
