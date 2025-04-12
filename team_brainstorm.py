from openai import OpenAI
import os

"""
This file is for generating group discussion of each team.
We use thinking models to stimulate the process and result of group discussion during prep time.
"""

class BrainStormer:
    def __init__(self, service: str = os.getenv("TEAM_AI_PROVIDER")):
        self.service = service
        self.text = "You are a professional debater, now you are in a debate, the motion is {}, and you are now going to brainstorm for the {} team, you should provide motion analysis, possible arguments, and possible arguments from other teams and counter arguments. Think as many arguments as possible for your team, always reason as detailly as possible."

    def brain_storm(self, motion, team) -> str:
        if self.service == "openrouter":
            return self.openrouter_brainstormer(motion, team)
        elif self.service == "openai":
            return self.openai_brainstormer(motion, team)
        else:
            raise ValueError("Invalid service")

    def openrouter_brainstormer(self, motion, team) -> str:

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

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

