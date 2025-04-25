from debater import Debater
















positions = ["Prime Minister", "Leader of Opposition", "Deputy Prime Minister", "Deputy Leader of Opposition", "Member of Government", "Member of Opposition", "Government Whip", "Opposition Whip"]

def main():
    """
    Main function to check if a given position is in the list of predefined positions.
    """
    if position in positions:
        pass
        
        





if __name__ == "__main__":
    motion = input("Enter the motion: ")
    debater = Debater(api_key=api_key, motion=motion)
    ai_debaters = input("Enter the AI debaters (comma separated): ").split(",")
    for ai_debater in ai_debaters:
        print(f"{ai_debater} is ready.")
