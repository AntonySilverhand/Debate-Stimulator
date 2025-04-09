

speaker_with_prompt = [
    ["Prime Minister", ["speech_structure.prime_minister_speech, debater_tone"]],
    ["Leader of Opposition", ["speech_structure.leader_of_opposition_speech, debater_tone"]],
    ["Deputy Prime Minister", ["speech_structure.deputy_prime_minister_speech, debater_tone"]],
    ["Deputy Leader of Opposition", ["speech_structure.deputy_leader_of_opposition_speech, debater_tone"]],
    ["Member of Government", ["speech_structure.member_of_government_speech, debater_tone"]],
    ["Member of Opposition", ["speech_structure.member_of_opposition_speech, debater_tone"]],
    ["Government Whip", ["speech_structure.government_whip_speech, debater_tone"]],
    ["Opposition Whip", ["speech_structure.opposition_whip_speech, debater_tone"]]
]






def announce_motion():
    print("Motion announced")

def announce_next_speaker(current_position: str, next_position: str):
    print("Next speaker: {}".format(next_position))

def announce_end():
    print("End of debate")


if __name__ == "__main__":
    announce_motion()
    current_speaker = "Prime Minister"
    announce_end()