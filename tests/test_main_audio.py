import pytest
import os
import tempfile
import numpy as np
from unittest.mock import patch, MagicMock, call

# Import the function to test from main.py
# Assuming main.py is in the parent directory relative to the tests directory
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Now we can import the function, but we need to be careful as main.py also runs code at the top level
# Let's try importing it directly. If main.py has side effects on import, this might need adjustment.
# It's generally better practice to have functions like this in a separate utils module.
try:
    from main import record_and_save_audio, logger as main_logger
except ImportError as e:
    print(f"Error importing from main: {e}")
    # Define a placeholder if import fails, so tests can be collected (but will fail)
    def record_and_save_audio(*args, **kwargs): raise RuntimeError("Import failed")
    main_logger = MagicMock()

# Mock sounddevice globally for all tests in this module, as it's a hardware dependency
@pytest.fixture(autouse=True)
def mock_sounddevice():
    mock_sd = MagicMock()
    # Mock InputStream context manager
    mock_stream = MagicMock()
    mock_sd.InputStream.return_value.__enter__.return_value = mock_stream
    mock_sd.InputStream.return_value.__exit__.return_value = None
    # Mock PortAudioError class for exception testing
    mock_sd.PortAudioError = sd.PortAudioError if 'sd' in globals() else Exception # Use real if available

    with patch('main.sd', mock_sd):
        yield mock_sd

# Mock soundfile globally
@pytest.fixture(autouse=True)
def mock_soundfile():
    mock_sf = MagicMock()
    with patch('main.sf', mock_sf):
        yield mock_sf

# Mock tempfile globally
@pytest.fixture(autouse=True)
def mock_tempfile():
    created_files = []

    # This inner class simulates the object returned by NamedTemporaryFile
    class MockNamedTemporaryFile:
        def __init__(self, suffix=".wav", delete=False):
            # Create a real temp file to get a valid path
            fd, self.name = tempfile.mkstemp(suffix=suffix)
            os.close(fd)
            created_files.append(self.name) # Keep track for cleanup
            # We don't need a real file object usually, just the name

        # Simulate context manager protocol
        def __enter__(self):
            return self # Return the object with the .name attribute

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass # Do nothing on exit in the mock

    # Patch tempfile.NamedTemporaryFile to return our mock class instance
    with patch('main.tempfile.NamedTemporaryFile', MockNamedTemporaryFile):
        yield # Let the test run

    # Cleanup any files created during the test
    for fpath in created_files:
        if os.path.exists(fpath):
            try:
                os.remove(fpath)
            except OSError:
                pass # Ignore errors during test cleanup

# Mock builtins.input globally
@pytest.fixture(autouse=True)
def mock_input():
    with patch('builtins.input', return_value="") as mock_input_func:
        yield mock_input_func

# Mock the logger used in main to check log messages
@pytest.fixture
def mock_logger():
    with patch('main.logger', MagicMock()) as logger_mock:
        yield logger_mock

# --- Test Cases ---

def test_record_and_save_audio_success(mock_sounddevice, mock_soundfile, mock_tempfile, mock_input, mock_logger):
    """Test successful audio recording and saving."""
    role = "TestRole"
    samplerate = 16000
    fake_audio_data = np.random.rand(samplerate * 2, 1).astype(np.float32) # 2 seconds

    # Simulate the callback putting data into the queue by patching queue.Queue
    mock_queue_instance = MagicMock()
    mock_queue_instance.empty.side_effect = [False, True] # Simulate one item then empty
    mock_queue_instance.get.return_value = fake_audio_data
    with patch('main.queue.Queue', return_value=mock_queue_instance):
        # Call the function
        result_path = record_and_save_audio(role, samplerate=samplerate)

    # Assertions
    assert result_path is not None
    # Ensure the function returned the same path that was passed to sf.write
    assert result_path == mock_soundfile.write.call_args[0][0], f"Returned path '{result_path}' differs from path used in write '{mock_soundfile.write.call_args[0][0]}'"
    assert isinstance(result_path, str) # Verify it's a string
    assert result_path.endswith(".wav") # Verify the suffix

    # Check soundfile.write call
    mock_soundfile.write.assert_called_once()
    args, kwargs = mock_soundfile.write.call_args
    np.testing.assert_array_equal(args[1], fake_audio_data)
    assert args[2] == samplerate

    # Check input calls
    mock_input.assert_has_calls([
        call(f"Press Enter to start recording for {role}... "),
        call("Press Enter again to stop recording... ")
    ])

    # Check logger info messages
    assert any(f"Starting recording for {role}..." in str(call_args) for call_args in mock_logger.info.call_args_list)
    assert any("Recording stopped." in str(call_args) for call_args in mock_logger.info.call_args_list)
    mock_logger.info.assert_any_call(f"Audio saved temporarily to {result_path}")

    # Manual cleanup for this test's file if needed (though fixture should handle)
    if os.path.exists(result_path):
        os.remove(result_path)

def test_record_and_save_audio_no_data(mock_sounddevice, mock_logger):
    """Test the case where no audio data is captured."""
    # Simulate the queue being empty
    mock_queue_instance = MagicMock()
    mock_queue_instance.empty.return_value = True
    with patch('main.queue.Queue', return_value=mock_queue_instance):
        result_path = record_and_save_audio("TestRole")

    assert result_path is None
    mock_logger.warning.assert_called_with("No audio data recorded.")

def test_record_and_save_audio_portaudio_error_stream(mock_sounddevice, mock_logger):
    """Test handling of PortAudioError during InputStream creation."""
    # Simulate PortAudioError on entering InputStream context
    mock_sounddevice.InputStream.return_value.__enter__.side_effect = mock_sounddevice.PortAudioError("Test PortAudio Error")

    result_path = record_and_save_audio("TestRole")

    assert result_path is None
    # Check the specific error log
    found_log = False
    for call_arg in mock_logger.error.call_args_list:
        args, kwargs = call_arg
        if args and "PortAudio error during stream setup/operation" in args[0]:
            found_log = True
            assert kwargs.get('exc_info') is True
            break
    assert found_log, "Expected PortAudio stream error log not found"

def test_record_and_save_audio_write_error(mock_sounddevice, mock_soundfile, mock_tempfile, mock_logger):
    """Test handling of an error during soundfile.write."""
    role = "TestRole"
    samplerate = 16000
    fake_audio_data = np.random.rand(samplerate * 1, 1).astype(np.float32) # 1 second

    # Simulate data being put in queue
    mock_queue_instance = MagicMock()
    mock_queue_instance.empty.side_effect = [False, True]
    mock_queue_instance.get.return_value = fake_audio_data
    # Mock os.path.exists and os.remove specifically for this test's cleanup phase
    with patch('main.queue.Queue', return_value=mock_queue_instance), \
         patch('main.os.path.exists', return_value=True) as mock_exists, \
         patch('main.os.remove') as mock_remove:
        # Mock soundfile.write to raise an error
        mock_soundfile.write.side_effect = IOError("Disk full")

        result_path = record_and_save_audio(role, samplerate=samplerate)

    # Assertions
    assert result_path is None
    # Check the specific processing/saving error log
    found_log = False
    for call_arg in mock_logger.error.call_args_list:
        args, kwargs = call_arg
        if args and "Error during audio processing/saving" in args[0]:
            found_log = True
            assert "Disk full" in args[0]
            assert kwargs.get('exc_info') is True
            break
    assert found_log, "Expected processing/saving error log not found"

    # Get the path that exists should have been called with
    exists_call_args, _ = mock_exists.call_args
    exists_path = exists_call_args[0]
    assert isinstance(exists_path, str)

    # Get the path that remove should have been called with
    remove_call_args, _ = mock_remove.call_args
    remove_path = remove_call_args[0]
    assert isinstance(remove_path, str)

    # Check that os.path.exists and os.remove were called on the temp file
    # Check the file that was supposed to be written to no longer exists
    # The fixture cleans it up AFTER the test, so we check our mock's list
    # Check the specific debug message for cleanup
    mock_logger.debug.assert_any_call(f"Cleaned up failed temporary file: {remove_path}")
