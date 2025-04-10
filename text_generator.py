from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

"""
This file is for generating text responses of the speaker's and the debaters'.
There should be at least OpenAI and OpenRouter as providers.
More is expected in the future.

It is designed to respond to only one message, so system message and message history is not supported.
The message should be passed as a string and be loaded with being passed in.

Wether the response is used for Speaker or Debater should be defined in main.py instead of here.
"""

class OpenAI_Responder:
    def __init__(self, model: str, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def respond_to(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    responder = OpenAI_Responder(model="o1-mini", api_key=os.getenv("OPENAI_API_KEY"))
    print(responder.respond_to("Hello, how are you?"))



