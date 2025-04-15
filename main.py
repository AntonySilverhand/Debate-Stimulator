import asyncio

from dotenv import load_dotenv
from team_brainstorm import BrainStormer
from speaker import Speaker







async def main(motion: str) -> None:
    load_dotenv()
    speaker = Speaker(motion)
    speech_log = []
    brainstormer = BrainStormer()

    await speaker.announce_motion()

    teams = ["Opening Government", "Opening Opposition", "Closing Government", "Closing Opposition"]
    speaking_order = speaker.speaking_order

    # Brainstorm for all teams concurrently
    tasks = []
    for team in teams:
        task = brainstormer.brain_storm(motion, team)
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    clue = [result for result in tasks]

    clue = {"OG": clue[0], "OO": clue[1], "CG": clue[2], "CO": clue[3]}

    await speaker.start_debate()

    for i in range(len(speaking_order) - 1):
        await speaker.announce_next_speaker(speaking_order[i], speaking_order[i + 1])
    await speaker.announce_end()

    






if __name__ == "__main__":
    motion = "This house would legalize marijuana."
    asyncio.run(main(motion))