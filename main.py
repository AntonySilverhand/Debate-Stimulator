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

    asyncio.run(speaker.announce_motion())

    for i in range(len(speaker.speaking_order) - 1):
        asyncio.run(speaker.announce_next_speaker(speaker.speaking_order[i], speaker.speaking_order[i + 1]))
    asyncio.run(speaker.announce_end())

    






if __name__ == "__main__":
    motion = "This house would legalize marijuana."
    main(motion)