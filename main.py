import asyncio
import logging
import os
from pathlib import Path
from datetime import datetime
import json
from interaction import Interaction

# ensure logs directory exists
log_dir = Path(__file__).resolve().parent / "logs"
log_dir.mkdir(exist_ok=True)
# create a new log file for each run using timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"main_{timestamp}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from team_brainstorm import BrainStormer
from speaker import Speaker
from debater import Debater


async def main(motion: str) -> None:
    load_dotenv()
    logger.debug("Environment variables loaded")
    logger.info(f"Starting debate with motion: {motion}")
    speaker = Speaker(motion)
    logger.debug("Speaker initialized")
    speech_log = []
    brainstormer = BrainStormer()
    logger.debug("BrainStormer initialized")
    interaction = Interaction()
    logger.debug("Interaction initialized")

    await speaker.announce_motion()
    logger.info("Motion announced")

    teams = ["Opening Government", "Opening Opposition", "Closing Government", "Closing Opposition"]
    speaking_order = speaker.speaking_order

    # Brainstorm for all teams concurrently
    tasks = []
    for team in teams:
        # run blocking brainstorm sync function in thread pool
        task = asyncio.to_thread(brainstormer.brain_storm, motion, team)
        tasks.append(task)

    # wait for all tasks and collect results
    results = await asyncio.gather(*tasks)
    logger.info("Brainstorming tasks completed")
    # log individual brainstorming outputs
    logger.debug("Team brainstorming outputs:")
    for idx, team in enumerate(teams):
        logger.debug(f"{team} output:\n{results[idx]}")
    # map results to clue keys in the original order
    clue = {"OG": results[0], "OO": results[1], "CG": results[2], "CO": results[3]}

    await speaker.start_debate()
    logger.info("Debate session started")

    # initialize debaters
    debaters = [
        ("Prime Minister", Debater(motion, "Prime Minister", speech_log, clue)),
        ("Leader of Opposition", Debater(motion, "Leader of Opposition", speech_log, clue)),
        ("Deputy Prime Minister", Debater(motion, "Deputy Prime Minister", speech_log, clue)),
        ("Deputy Leader of Opposition", Debater(motion, "Deputy Leader of Opposition", speech_log, clue)),
        ("Member of Government", Debater(motion, "Member of Government", speech_log, clue)),
        ("Member of Opposition", Debater(motion, "Member of Opposition", speech_log, clue)),
        ("Government Whip", Debater(motion, "Government Whip", speech_log, clue)),
        ("Opposition Whip", Debater(motion, "Opposition Whip", speech_log, clue)),
    ]
    # deliver speeches in order with logging
    for idx, (role, debater_obj) in enumerate(debaters):
        next_role = debaters[idx + 1][0] if idx + 1 < len(debaters) else None
        logger.info(f"{role} is delivering speech")
        speech = debater_obj.deliver_speech()
        try:
            await interaction.tts(tone=os.getenv("debater_tone"), input=speech)
        except Exception as e:
            logger.error(f"TTS failed for {role}: {e}", exc_info=True)
        speech_log.append(speech)
        logger.debug(f"{role} speech generated, length={len(speech)}")
        logger.debug(f"{role} speech content:\n{speech}")
        if next_role:
            logger.info(f"Announcing next speaker: {role} -> {next_role}")
            await speaker.announce_next_speaker(role, next_role)
    logger.info("Debate concluded")
    await speaker.announce_end()
    # snapshot all local variables at end of main
    logger.debug(f"Final local variables: {locals()}")
    # serialize and log speech mapping as JSON
    speech_map = {role: speech for (role, _), speech in zip(debaters, speech_log)}
    logger.info(f"Speeches JSON: {json.dumps(speech_map, ensure_ascii=False)}")


if __name__ == "__main__":
    motion = "This house would legalize marijuana."
    asyncio.run(main(motion))