from openai import OpenAI
import os

speaker_tone = os.getenv("speaker_tone")
debater_tone = os.getenv("debater_tone")

async def tts(tone: str, input: str) -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=input,
        instructions=tone,
        response_format="wav",
    ) as response:
        await LocalAudioPlayer().play(response)

def stt() -> str:
    audio_file= open("/path/to/file/audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe", 
        file=audio_file
    )
    return transcription.text

class Debater:
    def __init__(self, api_key, motion):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.motion = motion

    def respond(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
        
class PrimeMinister(Debater):
    def __init__(self, api_key, motion):
        super().__init__(api_key, motion)
        self.prompt = prime_minister_speech
        
    def respond(self, prompt=None) -> str:
        response = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": self.prompt.format(motion=self.motion) + "\n\n"}
            ]
        )
        return response.choices[0].message.content
        
    
        
prime_minister_speech="""
🎤 Prime Minister Speech Generator Prompt (Humanized BP Format)
You're the Prime Minister opening a British Parliamentary debate. Your speech should sound authentic, passionate, and conversational—like a real person leading a discussion. Generate a speech of at least 720 words but no more than 800 words. Persuade your audience that your policy is necessary, justified, and effective. Follow this natural-speaking structure precisely as described, clearly reflecting the traditional BP debate structure stored in memory:
Describe the Status Quo: Start vividly: "What we see nowadays is..." or "Right now, we live in a world where..." Use storytelling or relatable examples to capture attention emotionally and practically.
Identify the Problem: Smoothly highlight why this situation isn't acceptable: "The problem is clear..." or "This is something we simply can't accept anymore." Emphasize seriousness and urgency.
Explain Your Stance: Clearly introduce your stance by confidently stating something like: "That's why we, on side government, are proud to propose..." or simply "Today, this House would..."
Give Your Definition: Casually clarify any key terms or concepts your audience might not immediately grasp. Avoid overly technical explanations; just explain naturally, perhaps using examples for clarity.
Explain Your Policy: Describe your policy in plain language: "Here's exactly what we're going to do..." or "Our plan is simple and clear—here's how it works." Make sure it sounds practical and realistic.
Justification and Moral Framing: Transition naturally into why this is the right thing to do: "We believe deeply this policy is justified because..." or "This isn't just practical—it's morally necessary."
Stakeholders and Benefits: Talk about who your policy helps: "This will directly benefit people who..." or "Imagine how life changes positively for..." Clearly highlight vulnerable or important stakeholders, and explain why they deserve attention.
Tag Your Arguments: Announce your key arguments conversationally: "I've got two main reasons for you today—first is... and secondly... Now, let me explain each of these clearly."
End With Momentum: Wrap up powerfully yet authentically: "Ultimately, this policy matters because..." End your speech on an uplifting, forward-looking note: "We genuinely believe we can make a difference here, and that's exactly why we propose this motion."
Tone & Delivery Tips:
Speak clearly, passionately, and naturally—avoid sounding robotic or overly formal.
Use natural pauses, variations in pace, and genuine emotion.
Sound approachable yet authoritative and convincing, like a trusted leader rallying others around an important cause.

Now you are going to start your speech, the motion is: {motion}
""".format(motion=self.motion)