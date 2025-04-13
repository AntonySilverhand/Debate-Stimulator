import asyncio

from openai import AsyncOpenAI, OpenAI
import os
from dotenv import load_dotenv
import asyncio
import debater
import speech_structure
from team_brainstorm import BrainStormer







def main(motion: str) -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    speaker_tone = os.getenv("speaker_tone")
    openai = AsyncOpenAI(api_key=api_key)
    client = OpenAI(api_key=api_key)

    speaker = debater.Speaker(openai, motion, speaker_tone)
    speech_log = []
    brainstormer = BrainStormer()

    asyncio.run(speaker.announce_motion())

    teams = ["Opening Government", "Opening Opposition", "Closing Government", "Closing Opposition"]

    # Brainstorm TODO: refine this async function
    tasks = []
    for team in teams:
        task = asyncio.create_task(brainstormer.brain_storm(motion, team))
        tasks.append(task)
    
    asyncio.run(asyncio.gather(*tasks))

    asyncio.run(speaker.start_debate())

    for i in range(len(speaker.speaking_order) - 1):
        asyncio.run(speaker.announce_next_speaker(speaker.speaking_order[i], speaker.speaking_order[i + 1]))
    asyncio.run(speaker.announce_end())

    






if __name__ == "__main__":
    motion = "This house would legalize marijuana."
    main(motion)