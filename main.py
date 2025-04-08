import asyncio

from openai import AsyncOpenAI, OpenAI
import os
from dotenv import load_dotenv
import debater



def main(motion: str) -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai = AsyncOpenAI(api_key=api_key)
    client = OpenAI(api_key=api_key)
    speaker_tone = os.getenv("speaker_tone")

    speech_log = []

    asyncio.run(debater.tts(async_client=openai, tone=speaker_tone, input="Ladies and gentlemen, welcome to this debate. The motion reads: {motion}, now let's welcome our first speaker, the prime minister, hear hear.".format(motion=motion)))

if __name__ == "__main__":
    motion = "This house would legalize marijuana."
    main(motion)