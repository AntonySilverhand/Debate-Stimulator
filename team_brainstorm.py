from openai import OpenAI
import os
from dotenv import load_dotenv
from text_generator import Responder

# Make sure to load environment variables
load_dotenv()

"""
This file is for generating group discussion of each team.
We use thinking models to stimulate the process and result of group discussion during prep time.
TODO: Restructure and use text_generator to provide texts.
"""

class BrainStormer:
    def __init__(self, service: str = None):
        # Get the service from environment or use the provided one
        self.service = service if service else os.getenv("TEAM_AI_PROVIDER")
        # Strip any whitespace that might be in the environment variable
        if self.service:
            self.service = self.service.strip().lower()
        print(f"Using AI service: {self.service}")
        self.text = "You are a professional debater, now you are in a debate, the motion is {}, and you are now going to brainstorm for the {} team, you should provide motion analysis, possible arguments, and possible arguments from other teams and counter arguments. Think as many arguments as possible for your team, always reason as detailly as possible."

    def brain_storm(self, motion, team) -> str:
        if not self.service:
            raise ValueError(f"No AI service specified. Please set TEAM_AI_PROVIDER in your .env file.")
        
        if self.service == "openrouter":
            return self.openrouter_brainstormer(motion, team)
        elif self.service == "openai":
            return self.openai_brainstormer(motion, team)
        else:
            raise ValueError(f"Invalid service: '{self.service}'. Valid options are 'openrouter' or 'openai'")

    def openrouter_brainstormer(self, motion, team) -> str:
        # Temporarily unset proxy environment variables
        original_http_proxy = os.environ.pop('http_proxy', None)
        original_https_proxy = os.environ.pop('https_proxy', None)
        
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )

            print("Making API call to OpenRouter...")
            completion = client.chat.completions.create(
                model=os.getenv("TEAM_AI_MODEL"),   
                messages=[
                    {
                        "role": "user",
                        "content": self.text.format(motion, team)
                    }
                ]
            )

            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            raise
        finally:
            # Restore proxy settings
            if original_http_proxy:
                os.environ['http_proxy'] = original_http_proxy
            if original_https_proxy:
                os.environ['https_proxy'] = original_https_proxy

    def openai_brainstormer(self, motion, team) -> str:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=os.getenv("TEAM_AI_MODEL"),
            messages=[
                {"role": "user", "content": self.text.format(motion, team)}
            ]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    brainstormer = BrainStormer()
    print(brainstormer.brain_storm("THW legalize marijuana?", "Opening Government"))

