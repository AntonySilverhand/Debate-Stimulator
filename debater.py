from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os
from dotenv import load_dotenv
import speech_structure
import asyncio

load_dotenv()

debater_tone = os.getenv("debater_tone")

speaker_with_prompt = [
    ["Prime Minister", [speech_structure.prime_minister_speech, debater_tone]],
    ["Leader of Opposition", [speech_structure.leader_of_opposition_speech, debater_tone]],
    ["Deputy Prime Minister", [speech_structure.deputy_prime_minister_speech, debater_tone]],
    ["Deputy Leader of Opposition", [speech_structure.deputy_leader_of_opposition_speech, debater_tone]],
    ["Member of Government", [speech_structure.member_of_government_speech, debater_tone]],
    ["Member of Opposition", [speech_structure.member_of_opposition_speech, debater_tone]],
    ["Government Whip", [speech_structure.government_whip_speech, debater_tone]],
    ["Opposition Whip", [speech_structure.opposition_whip_speech, debater_tone]]
]


def load_prompt(motion: str, position: str) -> str:
    final_prompt = speaker_with_prompt[position][1][0] + "\n\n" + motion
    return final_prompt

class Debater:
    def __init__(self, client: OpenAI, motion: str):
        self.client = client
        self.motion = motion

    def respond_to(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content




