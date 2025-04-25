# Installing Debate Stimulator

The Debate Stimulator is a desktop application that lets you practice British Parliamentary debate with AI opponents.

## Prerequisites

- Python 3.9 or higher
- Microphone and speakers (for speech-to-text and text-to-speech)
- API keys for OpenAI and/or OpenRouter

## Installation

1. Clone the repository or download the source code.

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API keys:
   Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your-openai-key
   OPENROUTER_API_KEY=your-openrouter-key
   ```

## Configuration

Edit the `config.json` file to customize:
- Which positions are played by AI vs humans
- Which AI models to use
- Speaking tones and styles

## Running the Debate Stimulator

```bash
python main.py "Your debate motion here"
```

If no motion is provided, a default motion will be used.

## Logs and History

- Logs are stored in the `logs` directory
- Debate histories are saved in the `debate_history` directory
