"""
Test module for the progress tracker.
"""
import os
import json
import tempfile
import shutil
from pathlib import Path
import unittest
from datetime import datetime
import sys

# Add parent directory to path to allow importing modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

from progress_tracker import ProgressTracker

class TestProgressTracker(unittest.TestCase):
    """Test cases for ProgressTracker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test history files
        self.temp_dir = tempfile.mkdtemp()
        self.test_history_dir = Path(self.temp_dir) / "debate_history"
        self.test_history_dir.mkdir(exist_ok=True)
        
        # Create a test instance with the temporary directory
        self.tracker = ProgressTracker()
        # Override history_dir with test directory
        self.tracker.history_dir = self.test_history_dir
        
        # Create sample debate history files
        self.create_sample_debates()
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def create_sample_debates(self):
        """Create sample debate history files for testing."""
        # Sample debate 1
        debate1 = {
            "motion": "This house would ban social media for children under 16.",
            "speech_log": [
                "As Prime Minister, I strongly believe that social media poses significant risks to children under 16...",
                "As Leader of Opposition, I must challenge the government's paternalistic approach...",
                "As Deputy Prime Minister, I want to build upon the case established by the Prime Minister...",
                "As Deputy Leader of Opposition, I shall address the practical concerns of implementing such a ban...",
                "As Member of Government, I will focus on the mental health impacts of social media on youth...",
                "As Member of Opposition, I wish to highlight the educational benefits of social media...",
                "As Government Whip, my role today is to summarize our case...",
                "As Opposition Whip, I will demonstrate why our arguments prevail..."
            ]
        }
        
        # Sample debate 2
        debate2 = {
            "motion": "This house believes that space exploration should be privatized.",
            "speech_log": [
                "The government strongly believes that privatizing space exploration is beneficial...",
                "The opposition challenges the core assumptions made by the government...",
                "Building upon our case for privatization...",
                "We have heard much from the government about the benefits of privatization...",
                "I want to address some of the opposition's concerns about oversight...",
                "The private sector lacks the necessary incentives for pure scientific research...",
                "In conclusion, we have demonstrated several advantages of privatization...",
                "The opposition has clearly shown why space exploration should remain public..."
            ]
        }
        
        # Write sample debates to files with different timestamps
        time1 = datetime.now().strftime("%Y%m%d_%H%M%S")
        time2 = datetime.now().strftime("%Y%m%d_%H%M00")  # Earlier time
        
        with open(self.test_history_dir / f"{time1}.json", "w") as f:
            json.dump(debate1, f, indent=4)
            
        with open(self.test_history_dir / f"{time2}.json", "w") as f:
            json.dump(debate2, f, indent=4)
    
    def test_get_history(self):
        """Test get_history function returns the debate history."""
        history = self.tracker.get_history()
        
        # Verify we retrieved all sample debates
        self.assertEqual(len(history), 2)
        self.assertIn("motion", history[0])
        self.assertIn("speech_log", history[0])
        self.assertIn("file_name", history[0])
        self.assertIn("timestamp", history[0])
        
        # Test limit parameter
        limited_history = self.tracker.get_history(limit=1)
        self.assertEqual(len(limited_history), 1)
    
    def test_get_speaker_performance(self):
        """Test retrieving performance data for a specific role."""
        performances = self.tracker.get_speaker_performance("Prime Minister")
        
        # Verify we get performance data for the Prime Minister
        self.assertEqual(len(performances), 2)
        for perf in performances:
            self.assertIn("motion", perf)
            self.assertIn("timestamp", perf)
            self.assertIn("speech", perf)
    
    def test_analyze_progress(self):
        """Test the progress analysis functionality."""
        analysis = self.tracker.analyze_progress()
        
        # Verify analysis contains expected keys
        self.assertIn("status", analysis)
        self.assertIn("total_debates", analysis)
        self.assertIn("recent_motions", analysis)
        self.assertIn("recommendation", analysis)
        
        # Test with specific role
        role_analysis = self.tracker.analyze_progress(user_role="Prime Minister")
        self.assertIn("role_analysis", role_analysis)
        self.assertEqual(role_analysis["role_analysis"]["role"], "Prime Minister")
        self.assertIn("improvement_areas", role_analysis["role_analysis"])

if __name__ == "__main__":
    unittest.main()