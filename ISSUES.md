# Debate-Stimulator Identified Issues

## Main.py Issues

1. **Human Speech Not Added to Log**: Human speeches are logged but never added to `speech_log`. Only AI speeches and failed human speeches are added to the log.
   ```python
   # Line 192-194
   if speech:
       logger.debug(f"{role} speech delivered by human, length={len(speech)}")
       logger.debug(f"{role} speech content:\n{speech}")
       # TODO: Add speech_log.append(speech) here to include human speeches in the log
   ```

2. **Missing Queue Timeout**: No timeout handling when retrieving audio data from queue, which could potentially hang.
   ```python
   # Line 80-82
   # Retrieve data from queue
   while not q.empty():
       audio_data.append(q.get())
       # TODO: Add timeout mechanism to prevent potential hangs:
       # Example: Add timeout check or use q.get(block=True, timeout=0.5) with try/except
   ```

3. **Speech Map Assumption**: `speech_map` creation assumes `speech_log` and `debaters` have the same length and ordering.
   ```python
   # Line 207
   speech_map = {role: speech for (role, _), speech in zip(debaters, speech_log)}
   # TODO: Add validation to ensure speech_log and debaters match in length and order
   ```

4. **Hardcoded Motion**: Motion is hardcoded rather than being passed as a parameter.
   ```python
   # Line 212
   motion = "This house would legalize marijuana."
   # TODO: Replace hardcoded motion with command-line argument or config value
   ```

## Debater.py Issues

1. **Typo in Test Motion**: Contains a misspelled word in test motion.
   ```python
   # Line 90
   debater = Debater(motion="THBT civil rights movement should use violanve to advance its cause", position="Prime Minister", ...)
   # TODO: Fix typo: change "violanve" to "violence"
   ```

2. **Unused Imports**: Importing `LocalAudioPlayer` and `AsyncOpenAI` that aren't used.
   ```python
   # Line 1-2
   from openai import OpenAI, AsyncOpenAI
   from openai.helpers import LocalAudioPlayer
   # TODO: Remove unused imports - keep only OpenAI if that's all that's used
   ```

3. **Inefficient Speech Log Handling**: Redundant check and string conversion.
   ```python
   # Line 55-56
   speech_log_text = "\n".join(speech_log) if isinstance(speech_log, list) else str(speech_log)
   # TODO: Optimize by limiting speech log size or more efficient handling
   ```

4. **Incomplete Documentation**: Docstring in `prompt_loader` doesn't mention `clue` parameter.
   ```python
   # Line 32
   def prompt_loader(motion: str, position: str, speech_log: list, clue: str) -> str:
       """
       ...
       # TODO: Update docstring to include the clue parameter description
       """
   ```

## config_utils.py Issues

1. **Inefficient Config Loading**: Configuration is reloaded from disk on every call to `get_config()`.
   ```python
   # Line 16-27
   def get_config(key, default=None):
       # Reloads config from disk on every call
       config = load_config()
       return config.get(key, default)
       # TODO: Implement config caching with a global variable to store loaded config
   ```

2. **Missing Error Handling**: No error handling for missing config file or invalid JSON.
   ```python
   # Line 12-14
   config_path = Path(__file__).resolve().parent / "config.json"
   with open(config_path, "r") as f:
       return json.load(f)
   # TODO: Add try/except to handle FileNotFoundError and json.JSONDecodeError
   ```

## Interaction.py Issues

1. **Missing Environment Variable Error Handling**: No error handling if `INTERACTION_KEY` environment variable is missing.
   ```python
   # Line 33
   openai = AsyncOpenAI(api_key=os.environ.get("INTERACTION_KEY"))
   # TODO: Add check and error handling if INTERACTION_KEY is None
   ```

2. **Unclosed File Resources**: Audio files are opened but never properly closed.
   ```python
   # Line 47-48
   audio_file = open(audio_file, "rb")
   transcription = client.audio.transcriptions.create(...)
   # TODO: Use with statement to ensure file is closed: with open(audio_file, "rb") as file:
   ```

3. **Empty Lines**: File has many empty lines at the end (lines 67-76).
   ```python
   # TODO: Remove unnecessary empty lines at the end of the file
   ```

4. **Incomplete Implementation**: Todo comment at line 56 with no implementation.
   ```python
   # TODO: Implement additional providers and complete the commented functionality
   ```

## text_generator.py Issues

1. **Missing API Error Handling**: No exception handling for API calls in both `openai_respond_to` and `openrouter_respond_to` methods.
   ```python
   # Line 31-38
   def openai_respond_to(self, message: str) -> str:
       client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
       response = client.chat.completions.create(...)
       # TODO: Add try/except blocks to handle API errors and network issues
   ```

2. **Typo in TODO Comment**: Line 15 has "Resturture" instead of "Restructure".
   ```python
   # Line 15
   # TODO: Resturture to suit the response provider of team_brainstorm.py
   # TODO: Fix typo: change "Resturture" to "Restructure"
   ```

## Other Files Issues

1. **config.json.py**: Redundant with `config.json` but lacks the `PARTY` section.
   ```
   # TODO: Delete config.json.py file as it's redundant with config.json
   ```

2. **stimu.py**: Almost empty file with undefined variable references (`position`, `api_key`).
   ```
   # TODO: Either complete implementation of stimu.py or delete if not needed
   ```

3. **Empty Test Files**: Several test files are empty or incomplete.
   ```
   # TODO: Implement proper tests in debater_test.py and speaker_test.py
   ```

4. **Inconsistent Error Handling**: Different approaches to error handling across files.
   ```
   # TODO: Standardize error handling approach across all files
   ```

5. **API Key Management**: Inconsistent approach to retrieving and validating API keys.
   ```
   # TODO: Create a centralized credential management approach
   ```

6. **Proxy Handling**: Inconsistent handling of proxy settings across network calls.
   ```
   # TODO: Standardize proxy configuration across all network calls
   ```

7. **Incomplete Documentation**: Many files have TODOs or missing documentation.
   ```
   # TODO: Complete documentation across all files
   ```