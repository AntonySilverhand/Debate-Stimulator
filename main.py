import asyncio

from openai import AsyncOpenAI, OpenAI
import os
from dotenv import load_dotenv
import asyncio
import debater
import speech_structure



def main(motion: str) -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    speaker_tone = os.getenv("speaker_tone")
    openai = AsyncOpenAI(api_key=api_key)
    client = OpenAI(api_key=api_key)

    speaker = debater.Speaker(openai, motion, speaker_tone)
    speech_log = []

    speaker.announce_motion()







if __name__ == "__main__":
    motion = "This house would legalize marijuana."
    main(motion)