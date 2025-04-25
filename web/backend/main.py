from fastapi import FastAPI, HTTPException, WebSocket, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import sys
import os
import asyncio
import logging
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import base64
import tempfile
from pathlib import Path

# Set up path to allow importing from parent directory
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))

# Import debate simulator components
from debater.debater import Debater
from debater.team_brainstorm import BrainStormer
from speaker.speaker import Speaker
from utilities.interaction import Interaction
from config_utils import get_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Debate Stimulator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class DebateMotion(BaseModel):
    motion: str

class RoleConfig(BaseModel):
    role: str
    is_human: bool
    nickname: Optional[str] = None

class DebateConfig(BaseModel):
    motion: str
    roles: List[RoleConfig]

class SpeechInput(BaseModel):
    role: str
    text: Optional[str] = None
    audio_base64: Optional[str] = None

# Store active debates
active_debates = {}

@app.get("/")
async def root():
    return {"message": "Debate Stimulator API is running"}

@app.get("/config")
async def get_config_endpoint():
    """Get the current debate configuration"""
    try:
        with open(str(parent_dir / "config.json"), "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading config: {str(e)}")

@app.post("/start-debate")
async def start_debate(config: DebateConfig, background_tasks: BackgroundTasks):
    """Start a new debate with the given configuration"""
    try:
        debate_id = str(len(active_debates) + 1)
        
        # Initialize debate components
        speaker = Speaker(config.motion)
        brainstormer = BrainStormer()
        interaction = Interaction()
        
        # Update config
        party_config = {"PARTY": {}}
        for role_config in config.roles:
            party_config["PARTY"][role_config.role] = "Human" if role_config.is_human else "AI"
        
        # Store debate state
        active_debates[debate_id] = {
            "config": config.dict(),
            "speaker": speaker,
            "brainstormer": brainstormer,
            "interaction": interaction,
            "speech_log": [],
            "speaker_info": [],
            "current_speaker_index": 0,
            "clue": {},
            "party_config": party_config,
            "speaking_order": speaker.speaking_order,
        }
        
        # Start brainstorming in background
        background_tasks.add_task(
            initialize_debate_brainstorming,
            debate_id,
            config.motion
        )
        
        return {"debate_id": debate_id, "status": "initializing"}
    
    except Exception as e:
        logger.error(f"Error starting debate: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting debate: {str(e)}")

async def initialize_debate_brainstorming(debate_id: str, motion: str):
    """Initialize debate brainstorming for all teams"""
    try:
        debate = active_debates[debate_id]
        teams = ["Opening Government", "Opening Opposition", "Closing Government", "Closing Opposition"]
        
        # Brainstorm for all teams concurrently
        tasks = []
        for team in teams:
            task = asyncio.to_thread(debate["brainstormer"].brain_storm, motion, team)
            tasks.append(task)
        
        # Wait for all tasks and collect results
        results = await asyncio.gather(*tasks)
        logger.info(f"Debate {debate_id}: Brainstorming tasks completed")
        
        # Map results to clue keys in the original order
        debate["clue"] = {"OG": results[0], "OO": results[1], "CG": results[2], "CO": results[3]}
        debate["status"] = "ready"
        
        # Initialize debaters
        speech_log = debate["speech_log"]
        clue = debate["clue"]
        
        debate["debaters"] = [
            (role, Debater(motion, role, speech_log, clue), "Human" if config["is_human"] else "AI")
            for role, config in [(role_config.role, role_config) 
                               for role_config in debate["config"]["roles"]]
        ]
        
        logger.info(f"Debate {debate_id}: Initialization complete")
    
    except Exception as e:
        logger.error(f"Error initializing debate {debate_id}: {e}")
        if debate_id in active_debates:
            active_debates[debate_id]["status"] = "error"
            active_debates[debate_id]["error"] = str(e)

@app.get("/debates/{debate_id}/status")
async def get_debate_status(debate_id: str):
    """Get the status of a debate"""
    if debate_id not in active_debates:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    debate = active_debates[debate_id]
    current_speaker_index = debate["current_speaker_index"]
    total_speakers = len(debate["config"]["roles"])
    
    return {
        "status": debate.get("status", "initializing"),
        "current_speaker_index": current_speaker_index,
        "total_speakers": total_speakers,
        "current_speaker": debate["config"]["roles"][current_speaker_index].role if current_speaker_index < total_speakers else None,
        "speech_log_length": len(debate["speech_log"]),
        "error": debate.get("error")
    }

@app.get("/debates/{debate_id}/next-speaker")
async def get_next_speaker(debate_id: str):
    """Get the next speaker in the debate"""
    if debate_id not in active_debates:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    debate = active_debates[debate_id]
    if debate.get("status") != "ready":
        raise HTTPException(status_code=400, detail="Debate is not ready yet")
    
    current_index = debate["current_speaker_index"]
    if current_index >= len(debate["config"]["roles"]):
        return {"status": "complete", "message": "Debate is complete"}
    
    current_role = debate["config"]["roles"][current_index]
    
    return {
        "role": current_role.role,
        "is_human": current_role.is_human,
        "nickname": current_role.nickname,
        "index": current_index,
        "total": len(debate["config"]["roles"])
    }

@app.post("/debates/{debate_id}/speech")
async def submit_speech(debate_id: str, speech_input: SpeechInput):
    """Submit a speech for the current speaker"""
    if debate_id not in active_debates:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    debate = active_debates[debate_id]
    if debate.get("status") != "ready":
        raise HTTPException(status_code=400, detail="Debate is not ready yet")
    
    current_index = debate["current_speaker_index"]
    if current_index >= len(debate["config"]["roles"]):
        raise HTTPException(status_code=400, detail="Debate is already complete")
    
    current_role = debate["config"]["roles"][current_index]
    
    # Validate speaker
    if speech_input.role != current_role.role:
        raise HTTPException(status_code=400, detail=f"Expected speech from {current_role.role}, got {speech_input.role}")
    
    try:
        speech_text = None
        
        # Process audio if provided
        if speech_input.audio_base64:
            # Decode base64 audio and save to temp file
            audio_data = base64.b64decode(speech_input.audio_base64)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f:
                tmp_f.write(audio_data)
                temp_file_path = tmp_f.name
            
            # Convert audio to text
            interaction = debate["interaction"]
            try:
                speech_text = await asyncio.to_thread(interaction.stt, audio_file=temp_file_path)
            finally:
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
        elif speech_input.text:
            speech_text = speech_input.text
        else:
            raise HTTPException(status_code=400, detail="Either text or audio must be provided")
        
        # Record the speech
        if speech_text:
            debate["speech_log"].append(speech_text)
            debate["speaker_info"].append({
                "role": current_role.role,
                "speaker": current_role.nickname or ("Human" if current_role.is_human else "AI")
            })
            
            # Move to next speaker
            debate["current_speaker_index"] += 1
            
            return {"status": "success", "speech_text": speech_text}
        else:
            raise HTTPException(status_code=400, detail="Failed to process speech")
    
    except Exception as e:
        logger.error(f"Error processing speech: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing speech: {str(e)}")

@app.post("/debates/{debate_id}/ai-speech")
async def generate_ai_speech(debate_id: str, background_tasks: BackgroundTasks):
    """Generate speech for the current AI speaker"""
    if debate_id not in active_debates:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    debate = active_debates[debate_id]
    if debate.get("status") != "ready":
        raise HTTPException(status_code=400, detail="Debate is not ready yet")
    
    current_index = debate["current_speaker_index"]
    if current_index >= len(debate["config"]["roles"]):
        raise HTTPException(status_code=400, detail="Debate is already complete")
    
    current_role = debate["config"]["roles"][current_index]
    
    # Check if current speaker is AI
    if current_role.is_human:
        raise HTTPException(status_code=400, detail="Current speaker is human, not AI")
    
    # Generate AI speech in background to avoid blocking
    background_tasks.add_task(
        generate_ai_speech_task,
        debate_id,
        current_role.role,
        current_index
    )
    
    return {"status": "generating", "role": current_role.role}

async def generate_ai_speech_task(debate_id: str, role: str, index: int):
    """Background task to generate AI speech"""
    try:
        debate = active_debates[debate_id]
        motion = debate["config"]["motion"]
        speech_log = debate["speech_log"]
        clue = debate["clue"]
        
        # Create debater and generate speech
        debater = Debater(motion, role, speech_log, clue)
        speech = debater.deliver_speech()
        
        # Record the speech
        debate["speech_log"].append(speech)
        debate["speaker_info"].append({
            "role": role,
            "speaker": "AI"
        })
        
        # Move to next speaker
        debate["current_speaker_index"] = index + 1
        
        logger.info(f"Debate {debate_id}: AI speech generated for {role}")
    
    except Exception as e:
        logger.error(f"Error generating AI speech for debate {debate_id}, role {role}: {e}")
        if debate_id in active_debates:
            active_debates[debate_id]["error"] = f"Error generating AI speech: {str(e)}"

@app.post("/debates/{debate_id}/audio")
async def upload_audio(debate_id: str, file: UploadFile = File(...)):
    """Upload audio for speech-to-text conversion"""
    if debate_id not in active_debates:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    debate = active_debates[debate_id]
    
    try:
        # Save uploaded file to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f:
            content = await file.read()
            tmp_f.write(content)
            temp_file_path = tmp_f.name
        
        # Convert audio to text
        interaction = debate["interaction"]
        try:
            speech_text = await asyncio.to_thread(interaction.stt, audio_file=temp_file_path)
            return {"text": speech_text}
        finally:
            # Clean up temp file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.get("/debates/{debate_id}/speeches")
async def get_speeches(debate_id: str):
    """Get all speeches in a debate"""
    if debate_id not in active_debates:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    debate = active_debates[debate_id]
    
    speeches = []
    for i, speech in enumerate(debate["speech_log"]):
        speaker_info = debate["speaker_info"][i] if i < len(debate["speaker_info"]) else {"role": "Unknown", "speaker": "Unknown"}
        speeches.append({
            "role": speaker_info["role"],
            "speaker": speaker_info["speaker"],
            "speech": speech,
            "index": i
        })
    
    return speeches

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
