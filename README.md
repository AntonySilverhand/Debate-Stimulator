# Debate Stimulator - British Parliamentary Debate Practice

A sophisticated AI-powered tool for practicing British Parliamentary debate, receiving feedback, and tracking your progress over time.

*[中文版 (Chinese Version)](README_zh.md)*

## Overview

The Debate Stimulator provides a realistic environment to practice British Parliamentary (BP) debate with AI opponents or teammates. The system allows you to:

- Participate in full 8-speaker BP format debates
- Practice against AI debaters with advanced rhetorical capabilities
- Record and transcribe your speeches using speech-to-text
- Listen to AI speeches via text-to-speech
- Track your progress and receive personalized improvement suggestions
- Save debate history for later review and analysis

## British Parliamentary Debate Format

The British Parliamentary (BP) debate format involves 8 speakers across 4 teams:

1. **Opening Government**
   - Prime Minister
   - Deputy Prime Minister

2. **Opening Opposition**
   - Leader of Opposition
   - Deputy Leader of Opposition

3. **Closing Government**
   - Member of Government
   - Government Whip

4. **Closing Opposition**
   - Member of Opposition
   - Opposition Whip

Each speaker delivers a speech in order, with specific roles and responsibilities.

## Features

- **AI Debaters**: Powered by state-of-the-art language models to provide challenging opponents
- **Voice Interaction**: Record your speeches and hear AI responses for a natural debate experience
- **Customizable Motions**: Practice with a variety of debate topics
- **Team Brainstorming**: AI-assisted preparation for your speeches
- **Progress Tracking**: Analytics on your improvement over time
- **Debate History**: Save and review past debates for learning opportunities

## Getting Started

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure your preferences in `config.json`:
   - Set which positions are played by humans or AI
   - Adjust speech tones and AI models
4. Run the application:
   ```
   python main.py
   ```

## Configuration

Edit `config.json` to customize:
- Which debate positions are filled by humans vs AI
- AI provider and model selection
- Speaker and debater tone settings
- Other debate parameters

## Usage

1. Start a debate session with a predetermined motion
2. When prompted, deliver your speech by pressing Enter to begin recording
3. Press Enter again to finish recording
4. Listen to AI responses and prepare for your next speech if applicable
5. Review progress analysis at the end of the debate

## Progress Tracking

The system tracks your debate performance over time, providing:
- Overall skill development metrics
- Specific improvement areas
- Recommendations for future practice

## Requirements

- Python 3.8+
- Microphone and speakers
- Internet connection (for AI services)
- Required Python packages (see requirements.txt)

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0):

- **Open Source**: The complete source code must be made available to all users
- **Network Protection**: If you run a modified version on a server, you must make the source code available
- **Copyleft**: Derivative works must be distributed under the same license
- **Attribution**: You should give credit to the original author (AntonySilverhand)

See the [LICENSE](LICENSE) file for full details or view the [AGPL-3.0 License](https://www.gnu.org/licenses/agpl-3.0.html). A [Chinese translation](LICENSE_zh.md) of the license is also available.

## Contributors

AntonySilverhand

---

*Improve your debating skills through deliberate practice with AI-powered feedback.*
