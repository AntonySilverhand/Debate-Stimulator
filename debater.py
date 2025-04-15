from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os
from dotenv import load_dotenv
import speech_structure
import asyncio
from text_generator import Responder

load_dotenv()

"""
This file is to structure the final_prompt to be passed in the text generator.

There should be one def prompt_loader() that uses a general way of combining the different prompts and return the final_prompt, position should be a variable here.

"""

debater_tone = os.getenv("debater_tone")

speaker_with_prompt = [
    ["Prime Minister", [speech_structure.prime_minister_speech, debater_tone], "OG"],
    ["Leader of Opposition", [speech_structure.leader_of_opposition_speech, debater_tone], "OO"],
    ["Deputy Prime Minister", [speech_structure.deputy_prime_minister_speech, debater_tone], "OG"],
    ["Deputy Leader of Opposition", [speech_structure.deputy_leader_of_opposition_speech, debater_tone], "OO"],
    ["Member of Government", [speech_structure.member_of_government_speech, debater_tone], "CG"],
    ["Member of Opposition", [speech_structure.member_of_opposition_speech, debater_tone], "CO"],
    ["Government Whip", [speech_structure.government_whip_speech, debater_tone], "CG"],
    ["Opposition Whip", [speech_structure.opposition_whip_speech, debater_tone], "CO"]
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
    final_prompt = speaker_with_prompt[position][1][0] + "\n\n" + "The motion reads: " + motion + "\n\n" + "The previous speakers conversation: " + speech_log +"\n\n" + "Here are the clues you've prepared: " + "\n\n" + clue
    return final_prompt

class Debater:
    def __init__(self, client: OpenAI, motion: str, position: str, speech_log: list, clue: dict[str, str]):
        self.client = client
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




