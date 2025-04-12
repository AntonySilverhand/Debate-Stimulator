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

class Responder:
    def __init__(self, service: str = os.getenv("INDIVIDUAL_AI_PROVIDER")):
        self.service = service

    def respond_to(self,message: str) -> str:
        if self.service == "openai":
            return self.openai_respond_to(message)
        elif self.service == "openrouter":
            return self.openrouter_respond_to(message)
        else:
            raise ValueError("Invalid service")

    def openai_respond_to(self, message: str) -> str:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=os.getenv("INDIVIDUAL_AI_MODEL"),
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content

    def openrouter_respond_to(self, message: str) -> str:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        response = client.chat.completions.create(
            model=os.getenv("INDIVIDUAL_AI_MODEL"),
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    responder = Responder()
    print(responder.respond_to("Hello, how are you?"))



