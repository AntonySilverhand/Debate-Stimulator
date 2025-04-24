"""
Progress tracker for the Debate Stimulator.
Tracks debate history and provides feedback and advice based on past performance.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Agent to track debate progress and provide feedback based on debate history."""
    
    def __init__(self):
        """Initialize the progress tracker."""
        self.history_dir = Path(__file__).resolve().parent / "debate_history"
        self.history_dir.mkdir(exist_ok=True)
        
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Function calling tool to retrieve debate history.
        
        Args:
            limit: Optional limit on the number of most recent debates to return.
                  If None, returns all debate history.
        
        Returns:
            List of debate history dictionaries sorted by most recent first.
        """
        if not self.history_dir.exists():
            logger.warning(f"Debate history directory not found: {self.history_dir}")
            return []
            
        history_files = sorted(
            self.history_dir.glob("*.json"), 
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if limit is not None:
            history_files = history_files[:limit]
        
        debate_history = []
        for file_path in history_files:
            try:
                with open(file_path, 'r') as f:
                    debate_data = json.load(f)
                    # Add filename as metadata
                    debate_data['file_name'] = file_path.name
                    debate_data['timestamp'] = file_path.stem
                    debate_history.append(debate_data)
            except Exception as e:
                logger.error(f"Error reading debate history file {file_path}: {e}")
                
        return debate_history
    
    def get_speaker_performance(self, role: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieves performance data for a specific role across multiple debates.
        
        Args:
            role: The debater role to analyze (e.g., "Prime Minister")
            limit: Optional limit on the number of most recent debates to analyze
            
        Returns:
            List of dictionaries containing speech content and metadata for the role
        """
        debate_history = self.get_history(limit)
        performance_data = []
        
        for debate in debate_history:
            try:
                speeches = debate.get('speech_log', [])
                # Assuming speech_log indexes correspond to roles in order
                role_map = {
                    "Prime Minister": 0,
                    "Leader of Opposition": 1,
                    "Deputy Prime Minister": 2,
                    "Deputy Leader of Opposition": 3,
                    "Member of Government": 4,
                    "Member of Opposition": 5,
                    "Government Whip": 6,
                    "Opposition Whip": 7
                }
                
                if role in role_map and len(speeches) > role_map[role]:
                    performance_data.append({
                        'motion': debate.get('motion', 'Unknown motion'),
                        'timestamp': debate.get('timestamp', 'Unknown time'),
                        'speech': speeches[role_map[role]]
                    })
            except Exception as e:
                logger.error(f"Error processing debate for role {role}: {e}")
        
        return performance_data
    
    def analyze_progress(self, user_role: str = None) -> Dict[str, Any]:
        """
        Analyzes debate progress and provides feedback and advice.
        
        Args:
            user_role: Optional role to focus analysis on
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        debate_history = self.get_history()
        
        if not debate_history:
            return {
                'status': 'No debate history found',
                'recommendation': 'Complete your first debate to start tracking progress'
            }
        
        # Track debate count and frequency
        debate_count = len(debate_history)
        timestamps = [datetime.strptime(debate.get('timestamp', '').split('_')[0], '%Y%m%d') 
                      for debate in debate_history if 'timestamp' in debate]
        
        # Analyze recent debates
        recent_debates = debate_history[:3] if len(debate_history) >= 3 else debate_history
        
        # Analyze specific role if provided
        role_specific_analysis = {}
        if user_role:
            performances = self.get_speaker_performance(user_role)
            if performances:
                role_specific_analysis = {
                    'role': user_role,
                    'debates_participated': len(performances),
                    'recent_motions': [p['motion'] for p in performances[:3]],
                    'improvement_areas': self._identify_improvement_areas(performances)
                }
        
        # Prepare overall analysis
        analysis = {
            'status': 'Active',
            'total_debates': debate_count,
            'recent_motions': [debate.get('motion', 'Unknown') for debate in recent_debates],
            'recommendation': self._generate_recommendations(debate_count, user_role)
        }
        
        if role_specific_analysis:
            analysis['role_analysis'] = role_specific_analysis
            
        return analysis
    
    def _identify_improvement_areas(self, performances):
        """Identify areas for improvement based on speech patterns."""
        if not performances:
            return ["Not enough data to analyze"]
            
        areas = []
        
        # Check speech length consistency
        speech_lengths = [len(p.get('speech', '')) for p in performances]
        if any(length < 500 for length in speech_lengths):
            areas.append("Speech development - some speeches appear too short")
            
        # Simple content analysis (could be expanded with NLP in future)
        all_speeches = " ".join([p.get('speech', '') for p in performances])
        if "um" in all_speeches.lower() or "uh" in all_speeches.lower():
            areas.append("Reduce filler words (um, uh)")
            
        # Default improvements if none detected
        if not areas:
            areas.append("Continue practicing structured arguments")
            areas.append("Work on rebuttal techniques")
            
        return areas
    
    def _generate_recommendations(self, debate_count, user_role=None):
        """Generate personalized recommendations based on debate history."""
        if debate_count == 0:
            return "Complete your first debate to begin tracking progress"
        elif debate_count == 1:
            return "Great start! Try debating the same motion from different positions"
        elif debate_count < 5:
            return "Building experience - focus on structured arguments and evidence use"
        else:
            if user_role:
                if "Prime Minister" in user_role or "Leader" in user_role:
                    return "As an opening speaker, work on setting strong frameworks"
                elif "Whip" in user_role:
                    return "As a closing speaker, practice effective summarization techniques"
                else:
                    return "Develop stronger rebuttal skills and engage more with opposing arguments"
            else:
                return "Consider analyzing specific speeches to identify patterns and areas for improvement"


def get_tracker_instance():
    """Returns a singleton instance of the ProgressTracker."""
    if not hasattr(get_tracker_instance, "_instance"):
        get_tracker_instance._instance = ProgressTracker()
    return get_tracker_instance._instance