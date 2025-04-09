import asyncio

from openai import AsyncOpenAI, OpenAI
import os
from dotenv import load_dotenv
import debater
import speech_structure


class speaker(Debater):
    def __init__(self, api_key, motion, position):
        super().__init__(api_key, motion)
        self.position = position

    def announce_motion(async_client: AsyncOpenAI, motion: str, speaker_tone: str) -> None:
        asyncio.run(debater.tts(async_client=async_client, tone=speaker_tone, input="Ladies and gentlemen, welcome to this debate. The motion reads: {motion}, now let's welcome our first speaker, the prime minister, hear hear.".format(motion=motion)))


def main(motion: str) -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai = AsyncOpenAI(api_key=api_key)
    client = OpenAI(api_key=api_key)
    speaker_tone = os.getenv("speaker_tone")

    speech_log = []

    positions = ["prime_minister", "leader_of_opposition", "deputy_prime_minister", "deputy_leader_of_opposition", "member_of_government", "member_of_opposition", "government_whip", "opposition_whip"]

    debater = Debater(api_key=api_key, motion=motion)
    
    for position in positions:
        





if __name__ == "__main__":
    motion = "This house would legalize marijuana."
    main(motion)