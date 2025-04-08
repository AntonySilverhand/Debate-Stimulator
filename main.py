import asyncio

from openai import AsyncOpenAI, OpenAI
from openai.helpers import LocalAudioPlayer
import os
from dotenv import load_dotenv
import debater

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai = AsyncOpenAI(api_key=api_key)
client = OpenAI(api_key=api_key)

speech_log = []


def main(motion: str) -> None:
    asyncio.run(tts(motion=motion, input="Ladies and gentlemen, welcome to this debate. The motion reads: {motion}, now let's welcome our first speaker, the prime minister, hear hear.".format(motion=motion)))

if __name__ == "__main__":
    motion = "This house would legalize marijuana"
    main(motion)