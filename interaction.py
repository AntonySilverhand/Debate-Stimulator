import asyncio
from openai import AsyncOpenAI, OpenAI
from openai.helpers import LocalAudioPlayer
import os
from dotenv import load_dotenv

load_dotenv()

"""
This is a file for tts & stt to allow human and ai to interact.
There should be more providers in the future.
Currently it only supports openai.
"""



class Interaction:
    def __init__(self, service=os.getenv("INTERACTION_PROVIDER")):
        self.service = service

    async def tts(self, tone: str, input: str) -> None:
        if self.service == "openai":
            return await self.openai_tts(tone=tone, input=input)
        else:
            raise ValueError("Invalid service")

    def stt(self, audio_file: str) -> str:
        if self.service == "openai":
            return self.openai_stt(audio_file=audio_file)
        else:
            raise ValueError("Invalid service")

    async def openai_tts(self, tone: str, input: str) -> None:
        # For TTS
        openai = AsyncOpenAI(api_key=os.getenv("INTERACTION_KEY"))
        
        async with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            input=input,
            instructions=tone,
            response_format="wav",
        ) as response:
            await LocalAudioPlayer().play(response)

    def openai_stt(self, audio_file: str) -> str:
        # For STT
        client = OpenAI(api_key=os.getenv("INTERACTION_KEY"))
        audio_file = open(audio_file, "rb")
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe", 
            file=audio_file,
            response_format="text"
        )
        return transcription.text


    # TODO: Add more providers and add def stt(provider) & def tts(provider) to choose from



















