import asyncio
import logging
import os
from pathlib import Path
from datetime import datetime
import json
import sounddevice as sd
import soundfile as sf
import tempfile
import numpy as np
import queue
import threading
from utilities.interaction import Interaction
from config_utils import get_config
from debater.team_brainstorm import BrainStormer
from speaker.speaker import Speaker
from debater.debater import Debater
from speaker.progress_tracker import get_tracker_instance

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



# --- Audio Recording Helper Function ---
def record_and_save_audio(role: str, samplerate=44100) -> str | None:
    """Records audio from microphone and saves to a temporary WAV file."""
    q = queue.Queue()
    audio_data = []
    temp_file_path = None
    recording_event = threading.Event()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            logger.warning(f"Audio recording status: {status}")
        if recording_event.is_set():
            q.put(indata.copy())

    try:
        input(f"Press Enter to start recording for {role}... ")
        logger.info(f"Starting recording for {role}...")
        recording_event.set() # Signal recording start

        # Start the stream in a non-blocking way
        with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
            # Wait for user to stop recording
            input("Press Enter again to stop recording... ")
            recording_event.clear() # Signal recording stop
            logger.info("Recording stopped.")

    except sd.PortAudioError as e:
        logger.error(f"PortAudio error during stream setup/operation: {e}", exc_info=True)
         # Check for common issues
        if "Invalid device ID" in str(e) or "No Default Input Device Available" in str(e):
            logger.error("No microphone detected or selected. Please check your system audio settings.")
        elif "Device unavailable" in str(e):
            logger.error("Microphone might be in use by another application.")
        return None # Exit early if stream fails
    except Exception as e: # Catch other potential errors during stream setup/input
        logger.error(f"Unexpected error during recording phase: {e}", exc_info=True)
        return None # Exit early

    # --- Data retrieval and saving separated ---    
    try:
        # Retrieve data from queue
        while not q.empty():
            audio_data.append(q.get())

        if not audio_data:
            logger.warning("No audio data recorded.")
            return None

        # Concatenate blocks and save
        audio_np = np.concatenate(audio_data, axis=0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f:
            temp_file_path = tmp_f.name
            # --- Write the file --- 
            sf.write(temp_file_path, audio_np, samplerate)
            logger.info(f"Audio saved temporarily to {temp_file_path}")
        return temp_file_path

    except Exception as e: # Catch errors during queue processing, concatenation, file writing
        logger.error(f"Error during audio processing/saving: {e}", exc_info=True)
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f"Cleaned up failed temporary file: {temp_file_path}")
            except OSError as del_e:
                 logger.error(f"Error deleting failed temporary file {temp_file_path}: {del_e}")
        return None
 
 # --- End Audio Recording Helper ---



def debate_history_saver(motion, speech_log, speaker_info=None):
    """Save debate history to a JSON file."""
    # Ensure debate_history directory exists
    history_dir = Path(__file__).resolve().parent / "debate_history"
    history_dir.mkdir(exist_ok=True)
    
    history = {
        "motion": motion,
        "speech_log": speech_log
    }
    
    # Add speaker info to history if provided
    if speaker_info and len(speaker_info) == len(speech_log):
        history["speaker_info"] = speaker_info
    
    history_file_path = history_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with history_file_path.open("w") as f:
        json.dump(history, f, indent=4)
    logger.debug(f"Debate history saved to {history_file_path}")
    return history_file_path




async def main(motion: str) -> None:
    logger.debug("Configuration loaded from config.json")
    logger.info(f"Starting debate with motion: {motion}")
    speaker = Speaker(motion)
    logger.debug("Speaker initialized")
    speech_log = []
    speaker_info = []  # Initialize list to track AI or human player information
    brainstormer = BrainStormer()
    logger.debug("BrainStormer initialized")
    interaction = Interaction()
    logger.debug("Interaction initialized")
    
    # Detect human players and collect nicknames
    human_nicknames = {}
    human_positions = [pos for pos, party in get_config("PARTY").items() if party == "Human"]
    
    if human_positions:
        print("\n=== Human Players Detected ===")
        print("Please enter nicknames for progress tracking:")
        for position in human_positions:
            nickname = input(f"Nickname for {position} (leave empty for 'Human'): ").strip()
            if not nickname:
                nickname = "Human"
            human_nicknames[position] = nickname
            logger.info(f"Human player '{nickname}' will play as {position}")
        print("===============================\n")

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
        ("Prime Minister", Debater(motion, "Prime Minister", speech_log, clue), get_config("PARTY")["Prime Minister"]),
        ("Leader of Opposition", Debater(motion, "Leader of Opposition", speech_log, clue), get_config("PARTY")["Leader of Opposition"]),
        ("Deputy Prime Minister", Debater(motion, "Deputy Prime Minister", speech_log, clue), get_config("PARTY")["Deputy Prime Minister"]),
        ("Deputy Leader of Opposition", Debater(motion, "Deputy Leader of Opposition", speech_log, clue), get_config("PARTY")["Deputy Leader of Opposition"]),
        ("Member of Government", Debater(motion, "Member of Government", speech_log, clue), get_config("PARTY")["Member of Government"]),
        ("Member of Opposition", Debater(motion, "Member of Opposition", speech_log, clue), get_config("PARTY")["Member of Opposition"]),
        ("Government Whip", Debater(motion, "Government Whip", speech_log, clue), get_config("PARTY")["Government Whip"]),
        ("Opposition Whip", Debater(motion, "Opposition Whip", speech_log, clue), get_config("PARTY")["Opposition Whip"]),
    ]
    # deliver speeches in order with logging
    for idx, (role, debater_obj, party) in enumerate(debaters):
        next_role = debaters[idx + 1][0] if idx + 1 < len(debaters) else None
        logger.info(f"{role} is delivering speech")
        
        # Track speaker information (AI or human nickname)
        if party == "AI":
            speaker_type = "AI"
            speech = debater_obj.deliver_speech()
            speech_log.append(speech)
            speaker_info.append({"role": role, "speaker": speaker_type})
            try:
                await interaction.tts(tone=get_config("debater_tone"), input=speech)
            except Exception as e:
                logger.error(f"TTS failed for {role}: {e}", exc_info=True)
        else:
            # Get the human nickname for this position
            speaker_type = human_nicknames.get(role, "Human")
            logger.info(f"Waiting for human input from {role} ({speaker_type}) via microphone.")
            temp_audio_file = await asyncio.to_thread(record_and_save_audio, role)
            speech = None

            if temp_audio_file:
                try:
                    logger.info(f"Converting speech to text for {role}...")
                    speech = await asyncio.to_thread(interaction.stt, audio_file=temp_audio_file)
                    if speech:
                        speech_log.append(speech)
                        speaker_info.append({"role": role, "speaker": speaker_type})
                        logger.info(f"{role} speech captured via STT (length={len(speech)}). Content: {speech[:100]}...")
                    else:
                        logger.warning(f"STT returned empty result for {role}.")
                except Exception as e:
                    logger.error(f"STT failed for {role}: {e}", exc_info=True)
                finally:
                    # Clean up the temporary audio file
                    if os.path.exists(temp_audio_file):
                        os.remove(temp_audio_file)
                        logger.debug(f"Cleaned up temporary audio file: {temp_audio_file}")
            else:
                logger.warning(f"No audio recorded for {role}, skipping speech.")

            # Log the speech if captured, otherwise log absence
            if speech:
                logger.debug(f"{role} speech delivered by {speaker_type}, length={len(speech)}")
                logger.debug(f"{role} speech content:\n{speech}")
            else:
                logger.debug(f"{role} speech skipped (no audio or STT failed). Adding empty entry to log.")
                speech_log.append("") # Add empty string if speech failed
                speaker_info.append({"role": role, "speaker": speaker_type})

        if next_role:
            logger.info(f"Announcing next speaker: {role} -> {next_role}")
            await speaker.announce_next_speaker(role, next_role)
    logger.info("Debate concluded")
    await speaker.announce_end()
    # snapshot all local variables at end of main
    logger.debug(f"Final local variables: {locals()}")
    # serialize and log speech mapping as JSON with speaker information
    speech_map = {}
    for idx, ((role, _, _), speech) in enumerate(zip(debaters, speech_log)):
        speaker = speaker_info[idx]["speaker"] if idx < len(speaker_info) else "Unknown"
        speech_map[role] = {"content": speech, "speaker": speaker}
    logger.info(f"Speeches JSON: {json.dumps(speech_map, ensure_ascii=False)}")
    
    # Save debate history with speaker information
    history_path = debate_history_saver(motion, speech_log, speaker_info)
    logger.info(f"Debate history saved to: {history_path}")
    



def run_debate():
    """Entry point for the debate-simulator command-line tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Debate Stimulator - Practice British Parliamentary debate with AI opponents")
    parser.add_argument("motion", nargs="?", default="This house would legalize marijuana.", 
                     help="The debate motion to discuss")
    args = parser.parse_args()
    
    try:
        asyncio.run(main(args.motion))
    except KeyboardInterrupt:
        print("\nDebate session interrupted by user. Exiting...")
    except Exception as e:
        logger.error(f"Error running debate: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")
        print("Check the logs for more details.")

if __name__ == "__main__":
    run_debate()
