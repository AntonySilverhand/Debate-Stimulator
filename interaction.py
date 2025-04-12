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
    def __init__(self):
        # For TTS
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # For STT
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def tts(self, service: str, tone: str, input: str) -> None:
        if service == "openai":
            return self.openai_tts(tone=tone, input=input)
        else:
            raise ValueError("Invalid service")

    def stt(self, service: str, audio_file: str) -> str:
        if service == "openai":
            return self.openai_stt(audio_file=audio_file)
        else:
            raise ValueError("Invalid service")

    async def openai_tts(self, tone: str, input: str) -> None:
        async with self.openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="coral",
            input=input,
            instructions=tone,
            response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)

    def openai_stt(self, audio_file: str) -> str:
        audio_file = open(audio_file, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe", 
            file=audio_file,
            response_format="text"
        )
        return transcription.text


    # TODO: Add more providers and add def stt(provider) & def tts(provider) to choose from



















