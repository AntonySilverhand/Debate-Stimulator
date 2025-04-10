from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os
from dotenv import load_dotenv
import speech_structure
import asyncio

load_dotenv()
speaker_tone = os.getenv("speaker_tone")


class Speaker():
    def __init__(self, client: OpenAI, motion: str, speaker_tone: str):
        self.client = client
        self.motion = motion
        self.speaker_tone = speaker_tone
        self.speaking_order = ["Prime Minister", "Leader of Opposition", "Deputy Prime Minister", "Deputy Leader of Opposition", "Member of Government", "Member of Opposition", "Government Whip", "Opposition Whip"]

        
    async def announce_motion(self) -> None:
        # TODO: make it more natural and use llm to generate the texts here.
        text = "Ladies and gentlemen, welcome to this debate. The motion reads: {motion}, now you have 1 minute to read the motion and then you will have 15 minutes for prep time.".format(motion=self.motion)
        await tts(async_client=self.client, tone=self.speaker_tone, input=text)

    async def start_debate(self) -> None:
        # TODO: make it more natural and use llm to generate the texts here.
        text = "Ladies and gentlemen, the prep time is over. Now let's welcome the Prime Minister to deliver his speech, hear hear."
        await tts(async_client=self.client, tone=self.speaker_tone, input=text)

    async def announce_next_speaker(self, current_speaker_position: str, next_speaker_position: str) -> None:
        # TODO: make it more natural and use llm to generate the texts here.
        text = "Thank you {} for that very fine speech, now let's welcome {} to deliver his speech, hear hear.".format(current_speaker_position, next_speaker_position)
        await tts(async_client=self.client, tone=self.speaker_tone, input=text)

    async def announce_end(self) -> None:
        # TODO: make it more natural and use llm to generate the texts here.
        text = "Thank you all for your speeches, please wait for the results."     
        await tts(async_client=self.client, tone=self.speaker_tone, input=text)


