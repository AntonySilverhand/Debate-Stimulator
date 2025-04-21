from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os
from dotenv import load_dotenv
import debater_speech_structure
import asyncio
from text_generator import Responder
import json


"""
This file is to structure the final_prompt to be passed in the text generator.

There should be one def prompt_loader() that uses a general way of combining the different prompts and return the final_prompt, position should be a variable here.

"""

debater_tone = os.getenv("debater_tone")

speaker_with_prompt = [
    ["Prime Minister", [debater_speech_structure.prime_minister_speech, debater_tone], "OG"],
    ["Leader of Opposition", [debater_speech_structure.leader_of_opposition_speech, debater_tone], "OO"],
    ["Deputy Prime Minister", [debater_speech_structure.deputy_prime_minister_speech, debater_tone], "OG"],
    ["Deputy Leader of Opposition", [debater_speech_structure.deputy_leader_of_opposition_speech, debater_tone], "OO"],
    ["Member of Government", [debater_speech_structure.member_of_government_speech, debater_tone], "CG"],
    ["Member of Opposition", [debater_speech_structure.member_of_opposition_speech, debater_tone], "CO"],
    ["Government Whip", [debater_speech_structure.government_whip_speech, debater_tone], "CG"],
    ["Opposition Whip", [debater_speech_structure.opposition_whip_speech, debater_tone], "CO"]
]


def prompt_loader(motion: str, position: str, speech_log: list, clue: str) -> str:
    """
    This function is to structure the final_prompt to be passed in the text generator.
    
    Args:
        motion (str): The motion of the debate.
        position (str): The position of the speaker.
        speech_log (list): The list of previous speakers' conversations.
    
    Returns:
        str: The final_prompt to be passed in the text generator.

    TODO: The Prime Minister has no previous speaker, this should be optimized.
    """
    # find the speech template based on position
    speech_template = None
    for speaker in speaker_with_prompt:
        if speaker[0] == position:
            speech_template = speaker[1][0]
            break
    if speech_template is None:
        raise ValueError(f"Unknown position in prompt_loader: {position}")
    # format speech_log as string
    speech_log_text = "\n".join(speech_log) if isinstance(speech_log, list) else str(speech_log)
    final_prompt = (
        f"{speech_template}\n\n"
        f"The motion reads: {motion}\n\n"
        f"The previous speakers conversation: {speech_log_text}\n\n"
        f"Here are the clues you've prepared:\n\n{clue}"
    )
    return final_prompt

class Debater:
    def __init__(self, motion: str, position: str, speech_log: list, clue: dict[str, str]):
        self.motion = motion
        self.position = position
        self.speech_log = speech_log
        self.clue = clue
        self.responder = Responder()

    def deliver_speech(self) -> str:
        # Find the team for the current position
        debaterTeam = None
        for speaker in speaker_with_prompt:
            if speaker[0] == self.position:
                debaterTeam = speaker[2]
                break
        
        if debaterTeam is None:
            raise ValueError(f"Unknown position: {self.position}")
            
        clue = self.clue[debaterTeam]
        final_prompt = prompt_loader(self.motion, self.position, self.speech_log, clue)
        response = self.responder.respond_to(final_prompt)
        return response


if __name__ == "__main__":
    debater = Debater(motion="THBT civil rights movement should use violanve to advance its cause", position="Prime Minister", speech_log=[], clue={"OG": "", "OO": "", "CG": "", "CO": ""})
    print(debater.deliver_speech())

