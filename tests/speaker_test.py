import speech_structure

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