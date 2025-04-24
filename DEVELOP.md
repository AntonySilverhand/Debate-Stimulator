# Developer Guide for Debate Stimulator

This document provides an overview of the project structure and explains how the different components work together to create the British Parliamentary debate simulation experience.

*[中文版 (Chinese Version)](DEVELOP_zh.md)*

## Project Architecture

The Debate Stimulator is built with a modular architecture that separates different concerns:

```
Debate Stimulator/
├── main.py                 # Main application entry point
├── config.json             # Configuration settings
├── config_utils.py         # Utilities for accessing configuration
├── debater.py              # Debater agent implementation
├── debater_speech_structure.py # Speech templates for different positions
├── speaker.py              # Speaker/moderator implementation
├── interaction.py          # Speech-to-text and text-to-speech functionality
├── team_brainstorm.py      # Team preparation and argument generation
├── progress_tracker.py     # Tracking and analyzing debate performance
├── text_generator.py       # Interface to LLM providers
├── tests/                  # Unit and integration tests
└── debate_history/         # Stored debate history (created at runtime)
```

## Core Components

### 1. Main Application Flow (`main.py`)

The main module orchestrates the entire debate process:
- Initializes the debate with a motion
- Sets up the speaker, debaters, and brainstorming
- Manages the flow of speeches between different positions
- Handles audio recording for human participants
- Processes speech-to-text and text-to-speech conversions
- Saves debate history and provides progress analysis

### 2. Configuration System (`config.json` & `config_utils.py`)

The configuration system allows customization of:
- AI provider settings (OpenAI, OpenRouter)
- Model selection for different components
- Speech tones for speakers and debaters
- Role assignments (human vs. AI) for each debate position

### 3. Debate Participants

#### Speaker (`speaker.py`)
The Speaker acts as the debate moderator:
- Announces the motion and starts the debate
- Introduces each speaker in turn
- Manages transitions between speakers
- Concludes the debate session

#### Debater (`debater.py`)
The Debater represents each participant in the debate:
- Implements the 8 different positions in British Parliamentary debate
- Uses position-specific templates from `debater_speech_structure.py`
- Delivers speeches based on the motion, previous speeches, and team preparation
- Can be configured as AI or human participant

### 4. Team Preparation (`team_brainstorm.py`)

The BrainStormer component simulates team preparation:
- Generates strategic arguments for each team
- Analyzes the motion from different perspectives
- Anticipates opposing arguments and prepares counterarguments
- Provides clues and talking points for debaters

### 5. Voice Interaction (`interaction.py`)

The Interaction module handles voice communication:
- Implements text-to-speech (TTS) for AI speeches
- Implements speech-to-text (STT) for human speeches
- Supports different provider backends (currently OpenAI)
- Applies appropriate tones and speaking styles

### 6. Progress Tracking (`progress_tracker.py`)

The ProgressTracker analyzes debate performance over time:
- Saves debate history to JSON files
- Tracks participation across multiple debates
- Identifies areas for improvement
- Generates personalized recommendations
- Provides analytics on debating skill development

## Data Flow

1. **Initialization**:
   - The application starts with a motion
   - Configuration is loaded from `config.json`
   - Speaker, debaters, and brainstorming components are initialized

2. **Preparation Phase**:
   - BrainStormer generates team-specific arguments
   - Speaker announces the motion and starts the debate

3. **Debate Phase**:
   - For each position in order:
     - If AI: Debater generates and delivers speech via TTS
     - If human: System records audio, converts to text via STT
   - Speaker manages transitions between speakers

4. **Conclusion Phase**:
   - Speaker concludes the debate
   - Debate history is saved
   - Progress is analyzed and feedback is provided

## AI Integration

The system uses language models in several ways:

1. **Team Brainstorming**: Uses models to generate strategic arguments for each team
2. **Speech Generation**: Creates position-specific speeches for AI debaters
3. **Voice Interaction**: Converts text to speech and speech to text
4. **Progress Analysis**: Analyzes debate performance and provides feedback

## Adding New Features

### Adding a New AI Provider

To add a new AI provider:
1. Update the `interaction.py` file with a new method for the provider
2. Add provider-specific implementation in `text_generator.py`
3. Update the configuration options in `config.json`

### Adding New Debate Formats

To support additional debate formats:
1. Create new speech templates in `debater_speech_structure.py`
2. Update the speaking order in `speaker.py`
3. Modify the debate flow in `main.py`

### Enhancing Progress Tracking

To improve the progress tracking:
1. Extend the analysis methods in `progress_tracker.py`
2. Add new metrics or visualization capabilities
3. Implement more sophisticated feedback mechanisms

## Testing

The `tests/` directory contains unit and integration tests for various components:
- `test_main_audio.py`: Tests for audio recording and processing
- `debater_test.py`: Tests for the debater component
- `speaker_test.py`: Tests for the speaker component
- `test_progress_tracker.py`: Tests for progress tracking functionality

Run tests using pytest:
```
pytest tests/
```

## Configuration Reference

Key configuration options in `config.json`:

```json
{
  "speaker_tone": "...",        // Tone instructions for the Speaker
  "debater_tone": "...",        // Tone instructions for Debaters
  "TEAM_AI_PROVIDER": "...",    // Provider for team brainstorming
  "TEAM_AI_MODEL": "...",       // Model for team brainstorming
  "INDIVIDUAL_AI_PROVIDER": "...", // Provider for individual debaters
  "INDIVIDUAL_AI_MODEL": "...",  // Model for individual debaters
  "INTERACTION_PROVIDER": "...", // Provider for TTS/STT
  "PARTY": {                    // Role assignments (AI or human)
    "Prime Minister": "AI",
    "Leader of Opposition": "AI",
    ...
  }
}
```

## Environment Variables

The application requires the following environment variables:
- `OPENAI_API_KEY`: For OpenAI services
- `OPENROUTER_API_KEY`: For OpenRouter services
- `INTERACTION_KEY`: For speech-to-text and text-to-speech services

## Future Development Directions

Potential areas for enhancement:
1. **Multi-language support**: Add support for debates in different languages
2. **Real-time feedback**: Provide immediate feedback during speeches
3. **Advanced analytics**: Implement more sophisticated analysis of debate techniques
4. **Web interface**: Create a web-based UI for easier interaction
5. **Additional AI providers**: Support for more LLM providers and models
6. **Debate recording**: Save audio recordings of debates for review
