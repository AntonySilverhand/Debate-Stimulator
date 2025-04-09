from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import os
from dotenv import load_dotenv
import speech_structure

load_dotenv()

speaker_tone = os.getenv("speaker_tone")
debater_tone = os.getenv("debater_tone")

speaker_with_prompt = [
    ["Prime Minister", [speech_structure.prime_minister_speech, debater_tone]],
    ["Leader of Opposition", [speech_structure.leader_of_opposition_speech, debater_tone]],
    ["Deputy Prime Minister", [speech_structure.deputy_prime_minister_speech, debater_tone]],
    ["Deputy Leader of Opposition", [speech_structure.deputy_leader_of_opposition_speech, debater_tone]],
    ["Member of Government", [speech_structure.member_of_government_speech, debater_tone]],
    ["Member of Opposition", [speech_structure.member_of_opposition_speech, debater_tone]],
    ["Government Whip", [speech_structure.government_whip_speech, debater_tone]],
    ["Opposition Whip", [speech_structure.opposition_whip_speech, debater_tone]]
]

async def tts(async_client: AsyncOpenAI, tone: str, input: str) -> None:
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=input,
        instructions=tone,
        response_format="wav",
    ) as response:
        await LocalAudioPlayer().play(response)

def stt(client: OpenAI, audio_file: str) -> str:
    audio_file= open(audio_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe", 
        file=audio_file
    )
    return transcription.text

def prompt_loader(prompt: str) -> str:
    pass
    

class Debater:
    def __init__(self, api_key, motion):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.motion = motion

    def respond_to(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

class Speaker(Debater):
    def __init__(self, api_key, motion, position):
        super().__init__(api_key, motion)
        self.speaker_tone = speaker_tone
        
    def announce_motion(self, async_client: AsyncOpenAI) -> None:
        # TODO: make it more natural and use llm to generate the texts here.
        text = "Ladies and gentlemen, welcome to this debate. The motion reads: {motion}, now you have 1 minute to read the motion and then you will have 15 minutes for prep time.".format(motion=self.motion)
        asyncio.run(tts(async_client=async_client, tone=self.speaker_tone, input=text))

    def announce_next_speaker(self, async_client: AsyncOpenAI, current_speaker_position: str, next_speaker_position: str) -> None:
        # TODO: make it more natural and use llm to generate the texts here.
        text = "Thank you {} for that very fine speech, now let's welcome {} to deliver his speech, hear hear.".format(current_speaker_position, next_speaker_position)
        asyncio.run(tts(async_client=async_client, tone=self.speaker_tone, input=text))
        
# class PrimeMinister(Debater):
#     def __init__(self, api_key, motion):
#         super().__init__(api_key, motion)
#         self.prompt = prime_minister_speech
        
#     def respond(self, prompt=None) -> str:
#         response = self.client.chat.completions.create(
#             model="o1-mini",
#             messages=[
#                 {"role": "user", "content": self.prompt.format(motion=self.motion) + "\n\n"}
#             ]
#         )
#         return response.choices[0].message.content
        
    
