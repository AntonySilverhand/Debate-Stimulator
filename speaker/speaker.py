import asyncio
from utilities.text_generator import Responder
from utilities.interaction import Interaction
from config_utils import get_config


# text = "Ladies and gentlemen, welcome to this debate. The motion reads: {motion}, now you have 1 minute to read the motion and then you will have 15 minutes for prep time.".format(motion=self.motion)
# text = "Ladies and gentlemen, the prep time is over. Now let's welcome the Prime Minister to deliver his speech, hear hear."
# text = "Thank you {} for that very fine speech, now let's welcome {} to deliver his speech, hear hear.".format(current_speaker_position, next_speaker_position)
# text = "Thank you all for your speeches, please wait for the results."     




class Speaker():
    def __init__(self, motion: str):
        self.responder = Responder()
        self.interaction = Interaction()
        self.motion = motion
        self.speaking_order = ["Prime Minister", "Leader of Opposition", "Deputy Prime Minister", "Deputy Leader of Opposition", "Member of Government", "Member of Opposition", "Government Whip", "Opposition Whip"]
        self.speaker_tone = get_config("speaker_tone")
        
    async def announce_motion(self) -> None:
        text = "Ladies and gentlemen, welcome to this debate. The motion reads: {motion}, now you have 1 minute to read the motion and then you will have 15 minutes for prep time.".format(motion=self.motion)
        await self.interaction.tts(tone=self.speaker_tone, input=text)

    async def start_debate(self) -> None:
        text = "Ladies and gentlemen, the prep time is over. Now let's welcome the Prime Minister to deliver his speech, hear hear."
        await self.interaction.tts(tone=self.speaker_tone, input=text)

    async def announce_next_speaker(self, current_speaker_position: str, next_speaker_position: str) -> None:
        text = "Thank you {} for that very fine speech, now let's welcome {} to deliver his speech, hear hear.".format(current_speaker_position, next_speaker_position)
        await self.interaction.tts(tone=self.speaker_tone, input=text)

    async def announce_end(self) -> None:
        text = "Thank you all for your speeches, please wait for the results."
        await self.interaction.tts(tone=self.speaker_tone, input=text)

    def generate_rankings(speech_log: list) -> list:
        text = f"{judge_prompt}\n\n Based on the previous speakers' debate: {speech_log} + \n\n + Please rank the performances of each team, from best to worst. Afterwards, please explain why you ranked them the way you did."
        return self.responder.generate_response(text)

if __name__ == "__main__":
    speaker = Speaker(motion="This house would legalize marijuana.")
    asyncio.run(speaker.announce_motion())
    asyncio.run(speaker.start_debate())
    for i in range(len(speaker.speaking_order) - 1):
        asyncio.run(speaker.announce_next_speaker(speaker.speaking_order[i], speaker.speaking_order[i + 1]))
    asyncio.run(speaker.announce_end())
