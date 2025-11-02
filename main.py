from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import json
import asyncio
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import sqlite3
import pyautogui
import pywhatkit
from urllib.parse import quote
import base64
from cryptography.fernet import Fernet
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import aifc

# Import the existing assistant class
from voice_assistant import AdvancedVoiceAssistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global assistant instance
assistant = None

class VoiceCommand(BaseModel):
    command: str

class ProfileUpdate(BaseModel):
    field: str
    value: str

class ContactData(BaseModel):
    name: str
    relationship: str
    phone: str
    email: str
    notes: str

class TaskData(BaseModel):
    task: str
    priority: str = "medium"

@app.on_event("startup")
async def startup_event():
    """Initialize the voice assistant on startup"""
    global assistant
    # We'll initialize the assistant when needed since it requires GUI components

@app.get("/")
async def read_root():
    return {"message": "Voice Assistant API is running"}

@app.get("/api/status")
async def get_status():
    return {"status": "running", "assistant_ready": assistant is not None}

@app.post("/api/initialize")
async def initialize_assistant():
    """Initialize the voice assistant"""
    global assistant
    try:
        if assistant is None:
            # We need to create a minimal tkinter root window in a separate thread
            def create_assistant():
                global assistant
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                assistant = AdvancedVoiceAssistant(root)
            
            thread = threading.Thread(target=create_assistant, daemon=True)
            thread.start()
            thread.join(timeout=5)
            
            if assistant:
                return {"status": "success", "message": "Assistant initialized"}
            else:
                return {"status": "error", "message": "Failed to initialize assistant"}
        else:
            return {"status": "success", "message": "Assistant already initialized"}
    except Exception as e:
        return {"status": "error", "message": f"Initialization failed: {str(e)}"}

@app.post("/api/command")
async def process_command(voice_command: VoiceCommand):
    """Process a voice command"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    try:
        # Process the command
        response = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: process_command_sync(assistant, voice_command.command)
        )
        
        return {
            "status": "success",
            "command": voice_command.command,
            "response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "command": voice_command.command,
            "response": f"Error processing command: {str(e)}"
        }

def process_command_sync(assistant, command):
    """Process command synchronously"""
    # Add to conversation
    assistant.add_to_conversation("You", command)
    
    # Process command and capture response
    response = assistant.process_enhanced_command(command)
    
    # Speak the response
    assistant.speak(response)
    
    return response

@app.get("/api/profile")
async def get_profile():
    """Get user profile"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    return {"profile": assistant.user_profile}

@app.put("/api/profile")
async def update_profile(update: ProfileUpdate):
    """Update user profile"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    assistant.user_profile[update.field] = update.value
    assistant.save_user_profile()
    
    return {"status": "success", "message": "Profile updated"}

@app.get("/api/contacts")
async def get_contacts():
    """Get all contacts"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    contacts = assistant.get_contacts()
    return {"contacts": contacts}

@app.post("/api/contacts")
async def add_contact(contact: ContactData):
    """Add a new contact"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    assistant.add_contact(
        contact.name,
        contact.relationship,
        contact.phone,
        contact.email,
        contact.notes
    )
    
    return {"status": "success", "message": "Contact added"}

@app.get("/api/tasks")
async def get_tasks():
    """Get all tasks"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    tasks = assistant.get_tasks()
    return {"tasks": tasks}

@app.post("/api/tasks")
async def add_task(task: TaskData):
    """Add a new task"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    assistant.add_task(task.task, task.priority)
    return {"status": "success", "message": "Task added"}

@app.get("/api/conversation")
async def get_conversation():
    """Get conversation history"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    # This would need to be implemented in the assistant class
    # For now, return empty
    return {"conversation": []}

@app.post("/api/speak")
async def speak_text(text: str):
    """Make the assistant speak text"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    assistant.speak(text)
    return {"status": "success", "message": "Text spoken"}

@app.post("/api/listen")
async def start_listening():
    """Start listening for voice input"""
    global assistant
    if not assistant:
        raise HTTPException(status_code=400, detail="Assistant not initialized")
    
    try:
        # This would need proper async handling for voice recognition
        # For now, return a placeholder
        return {
            "status": "success", 
            "message": "Listening started (web voice recognition not fully implemented)"
        }
    except Exception as e:
        return {"status": "error", "message": f"Listening failed: {str(e)}"}

# WebSocket for real-time communication
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process command through WebSocket
            command_data = json.loads(data)
            if 'command' in command_data:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: process_command_sync(assistant, command_data['command'])
                )
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "data": response
                }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount static files for web interface
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/web")
async def web_interface():
    """Serve the web interface"""
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)