import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import json
from threading import Thread
import time
import sqlite3
import pickle
import base64
from cryptography.fernet import Fernet
import subprocess
import pyautogui
import pywhatkit
from urllib.parse import quote
import platform

class AdvancedVoiceAssistant:
    def __init__(self, root=None):
        self.root = root
        
        # Initialize personal profile
        self.user_profile = {}
        self.encryption_key = self.generate_encryption_key()
        
        # Initialize databases
        self.init_databases()
        
        # Load user profile
        self.load_user_profile()
        
        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[1].id)  # Female voice
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        except:
            print("Microphone not available")
        
        self.is_listening = False
        
        # Only setup UI if we have a root window
        if root:
            self.setup_ui()
    
    def generate_encryption_key(self):
        """Generate or load encryption key for secure data storage"""
        try:
            with open('key.key', 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open('key.key', 'wb') as key_file:
                key_file.write(key)
            return key
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        fernet = Fernet(self.encryption_key)
        return fernet.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        fernet = Fernet(self.encryption_key)
        return fernet.decrypt(encrypted_data).decode()
    
    def init_databases(self):
        """Initialize SQLite databases for personal data"""
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        
        # User profile table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                key TEXT PRIMARY KEY,
                value BLOB
            )
        ''')
        
        # Contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                relationship TEXT,
                phone TEXT,
                email TEXT,
                notes TEXT
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                priority TEXT,
                due_date TEXT,
                completed INTEGER DEFAULT 0,
                created_date TEXT
            )
        ''')
        
        # Notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_date TEXT,
                category TEXT
            )
        ''')
        
        # Apps table for quick access
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS apps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT,
                command TEXT,
                category TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Add default apps
        self.add_default_apps()
    
    def add_default_apps(self):
        """Add default applications to the database"""
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        
        # Check if apps already exist
        cursor.execute("SELECT COUNT(*) FROM apps")
        if cursor.fetchone()[0] == 0:
            default_apps = [
                ('Notepad', 'notepad.exe', 'notepad', 'Utilities'),
                ('Calculator', 'calc.exe', 'calc', 'Utilities'),
                ('Chrome', 'chrome.exe', 'chrome', 'Browser'),
                ('Spotify', 'spotify.exe', 'spotify', 'Music'),
                ('VLC', 'vlc.exe', 'vlc', 'Media'),
                ('Word', 'winword.exe', 'word', 'Office'),
                ('Excel', 'excel.exe', 'excel', 'Office'),
            ]
            
            for app in default_apps:
                cursor.execute(
                    "INSERT INTO apps (name, path, command, category) VALUES (?, ?, ?, ?)",
                    app
                )
        
        conn.commit()
        conn.close()
    
    def load_user_profile(self):
        """Load user profile from database"""
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT key, value FROM user_profile")
        rows = cursor.fetchall()
        
        for key, encrypted_value in rows:
            try:
                self.user_profile[key] = self.decrypt_data(encrypted_value)
            except:
                self.user_profile[key] = encrypted_value.decode() if encrypted_value else ""
        
        conn.close()
        
        # Set default values if profile is empty
        if not self.user_profile:
            self.setup_user_profile()
    
    def setup_user_profile(self):
        """Initial setup for user profile"""
        self.user_profile = {
            'name': '',
            'age': '',
            'birthday': '',
            'email': '',
            'phone': '',
            'address': '',
            'work': '',
            'interests': '',
            'emergency_contact': '',
            'medical_info': '',
            'favorite_music': '',
            'favorite_websites': ''
        }
    
    def save_user_profile(self):
        """Save user profile to database"""
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM user_profile")
        
        for key, value in self.user_profile.items():
            if value:
                encrypted_value = self.encrypt_data(str(value))
                cursor.execute(
                    "INSERT INTO user_profile (key, value) VALUES (?, ?)",
                    (key, encrypted_value)
                )
        
        conn.commit()
        conn.close()
    
    def setup_ui(self):
        # Only setup UI if we have a root window
        if not self.root:
            return
            
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title with user name
        user_name = self.user_profile.get('name', 'User')
        title_label = ttk.Label(main_frame, text=f"Advanced Assistant", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=1, column=0, columnspan=4, pady=(0, 10))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(0, 10))
        
        # Listen button
        self.listen_button = ttk.Button(button_frame, text="Start Listening", command=self.toggle_listening)
        self.listen_button.grid(row=0, column=0, padx=2)
        
        # Profile button
        self.profile_button = ttk.Button(button_frame, text="My Profile", command=self.manage_profile)
        self.profile_button.grid(row=0, column=1, padx=2)
        
        # Contacts button
        self.contacts_button = ttk.Button(button_frame, text="Contacts", command=self.manage_contacts)
        self.contacts_button.grid(row=0, column=2, padx=2)
        
        # Tasks button
        self.tasks_button = ttk.Button(button_frame, text="Tasks", command=self.manage_tasks)
        self.tasks_button.grid(row=0, column=3, padx=2)
        
        # Apps button
        self.apps_button = ttk.Button(button_frame, text="Apps", command=self.manage_apps)
        self.apps_button.grid(row=0, column=4, padx=2)
        
        # Quick Actions button
        self.actions_button = ttk.Button(button_frame, text="Quick Actions", command=self.show_quick_actions)
        self.actions_button.grid(row=0, column=5, padx=2)
        
        # Conversation area
        conversation_label = ttk.Label(main_frame, text="Conversation:")
        conversation_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        self.conversation_area = scrolledtext.ScrolledText(main_frame, width=90, height=20, state=tk.DISABLED)
        self.conversation_area.grid(row=4, column=0, columnspan=4, pady=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Enhanced commands examples
        examples_label = ttk.Label(main_frame, text="Enhanced Commands:")
        examples_label.grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        
        examples_text = """
• "Play Despacito on YouTube" - Play specific song
• "Open Spotify" - Launch applications
• "Search for AI tutorials" - Web search
• "Play some jazz music" - Play genre on YouTube
• "Open calculator" - Open system apps
• "Type hello world" - Type text automatically
• "Take a screenshot" - Capture screen
• "Scroll down" - Control scrolling
• "What's the weather?" - Weather information
• "Set volume to 50" - Control system volume
• "Open my email" - Open Gmail
• "Show my tasks" - Display pending tasks
• "Remember I like pizza" - Store personal note
• "What time is it?" - Current time
• "Tell me a joke" - Entertainment
        """
        
        examples_display = tk.Text(main_frame, width=90, height=8, wrap=tk.WORD)
        examples_display.grid(row=6, column=0, columnspan=4, pady=(0, 10))
        examples_display.insert(tk.END, examples_text)
        examples_display.config(state=tk.DISABLED)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(text="Stop Listening")
            self.status_label.config(text="Listening...", foreground="blue")
            self.add_to_conversation("Assistant", "I'm listening...")
            # Start listening in a separate thread
            self.listening_thread = Thread(target=self.listen_loop)
            self.listening_thread.daemon = True
            self.listening_thread.start()
        else:
            self.is_listening = False
            self.listen_button.config(text="Start Listening")
            self.status_label.config(text="Ready", foreground="green")
            self.add_to_conversation("Assistant", "Stopped listening.")
    
    def listen_loop(self):
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Recognize speech
                command = self.recognizer.recognize_google(audio).lower()
                self.add_to_conversation("You", command)
                self.process_enhanced_command(command)
                
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                pass
            except sr.UnknownValueError:
                self.add_to_conversation("Assistant", "Sorry, I didn't understand that.")
                self.speak("Sorry, I didn't understand that.")
            except sr.RequestError as e:
                self.add_to_conversation("Assistant", f"Error with speech recognition: {e}")
                self.speak("There was an error with speech recognition.")
            except Exception as e:
                self.add_to_conversation("Assistant", f"Unexpected error: {e}")
    
    def process_enhanced_command(self, command):
        response = "I'm not sure how to help with that."
        
        # Music and YouTube commands
        if any(word in command for word in ["play", "song", "music"]):
            response = self.handle_music_command(command)
        
        # Application control
        elif any(word in command for word in ["open", "launch", "start"]):
            response = self.handle_app_command(command)
        
        # Web control commands
        elif any(word in command for word in ["search", "find", "look for"]):
            response = self.handle_search_command(command)
        
        # System control commands
        elif any(word in command for word in ["type", "write", "enter"]):
            response = self.handle_typing_command(command)
        
        elif any(word in command for word in ["scroll", "page"]):
            response = self.handle_scroll_command(command)
        
        elif "screenshot" in command:
            response = self.take_screenshot()
        
        elif "volume" in command:
            response = self.handle_volume_command(command)
        
        # Personal information queries
        elif any(word in command for word in ["my name", "who am i", "what's my name"]):
            name = self.user_profile.get('name', 'Not set')
            response = f"Your name is {name}" if name else "I don't know your name yet."
        
        elif any(word in command for word in ["my age", "how old am i"]):
            age = self.user_profile.get('age', 'Not set')
            response = f"You are {age} years old" if age else "I don't know your age yet."
        
        # Contact management
        elif any(word in command for word in ["contact", "call", "phone"]):
            response = self.handle_contact_command(command)
        
        # Task management
        elif any(word in command for word in ["task", "reminder", "todo", "schedule"]):
            response = self.handle_task_command(command)
        
        # Notes management
        elif any(word in command for word in ["remember", "note", "memorize"]):
            response = self.handle_note_command(command)
        
        # Standard commands
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
        
        elif "joke" in command:
            joke = self.get_joke()
            response = joke
        
        elif "weather" in command:
            response = self.get_weather()
        
        elif any(word in command for word in ["exit", "quit", "stop", "goodbye"]):
            response = "Goodbye! Have a great day!"
            if self.root:
                self.add_to_conversation("Assistant", response)
                self.speak(response)
                self.root.after(1000, self.root.destroy)
            return response
        
        else:
            response = "I can play music, open apps, control your computer, manage your personal information, and much more!"
        
        if self.root:
            self.add_to_conversation("Assistant", response)
        self.speak(response)
        return response

    # ... (Include all the other methods from your original code here)
    # handle_music_command, handle_app_command, handle_search_command, etc.
    # manage_profile, manage_contacts, manage_tasks, etc.
    # get_contacts, add_contact, get_tasks, add_task, etc.

    def handle_music_command(self, command):
        """Handle music and YouTube playback commands"""
        try:
            if "on youtube" in command or "play" in command:
                # Extract song name
                if "play" in command:
                    song = command.replace("play", "").replace("on youtube", "").replace("song", "").strip()
                else:
                    song = command.replace("on youtube", "").strip()
                
                if song:
                    if self.root:
                        self.add_to_conversation("Assistant", f"Playing {song} on YouTube...")
                    # Use pywhatkit to play on YouTube
                    pywhatkit.playonyt(song)
                    return f"Playing {song} on YouTube"
                else:
                    return "What song would you like me to play?"
            
            elif "music" in command:
                # Play random music based on genre
                if "jazz" in command:
                    pywhatkit.playonyt("jazz music")
                    return "Playing jazz music"
                elif "rock" in command:
                    pywhatkit.playonyt("rock music")
                    return "Playing rock music"
                elif "classical" in command:
                    pywhatkit.playonyt("classical music")
                    return "Playing classical music"
                else:
                    # Play user's favorite music if set
                    favorite = self.user_profile.get('favorite_music', '')
                    if favorite:
                        pywhatkit.playonyt(favorite)
                        return f"Playing your favorite music: {favorite}"
                    else:
                        pywhatkit.playonyt("top hits")
                        return "Playing popular music"
        
        except Exception as e:
            return f"Couldn't play music: {str(e)}"

    def handle_app_command(self, command):
        """Handle application launching commands"""
        app_name = command.replace("open", "").replace("launch", "").replace("start", "").strip()
        
        # Common applications
        app_commands = {
            'notepad': 'notepad',
            'calculator': 'calc' if os.name == 'nt' else 'gnome-calculator',
            'chrome': 'chrome',
            'firefox': 'firefox',
            'spotify': 'spotify',
            'vlc': 'vlc',
            'word': 'winword',
            'excel': 'excel',
            'powerpoint': 'powerpnt',
            'paint': 'mspaint',
            'cmd': 'cmd',
            'task manager': 'taskmgr',
            'control panel': 'control',
        }
        
        # Check database for custom apps
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, path FROM apps WHERE name LIKE ? OR command LIKE ?", 
                      (f'%{app_name}%', f'%{app_name}%'))
        app = cursor.fetchone()
        conn.close()
        
        if app:
            try:
                os.startfile(app[1]) if os.name == 'nt' else subprocess.Popen([app[1]])
                return f"Opening {app[0]}"
            except:
                return f"Couldn't open {app[0]}"
        
        # Check common apps
        for key, cmd in app_commands.items():
            if key in app_name:
                try:
                    if os.name == 'nt':
                        os.system(f'start {cmd}')
                    else:
                        subprocess.Popen([cmd])
                    return f"Opening {key}"
                except:
                    return f"Couldn't open {key}"
        
        # Try to open as website
        if "." in app_name or "website" in command:
            webbrowser.open(f"https://{app_name}")
            return f"Opening {app_name} in browser"
        
        return f"I'm not sure how to open {app_name}"

    def handle_search_command(self, command):
        """Handle web search commands"""
        query = command.replace("search for", "").replace("search", "").replace("find", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={quote(query)}")
            return f"Searching for {query}"
        return "What would you like me to search for?"

    def handle_typing_command(self, command):
        """Handle automatic typing commands"""
        text = command.replace("type", "").replace("write", "").replace("enter", "").strip()
        if text:
            # Wait a moment for user to focus on text field
            def type_text():
                time.sleep(2)
                pyautogui.write(text)
            
            Thread(target=type_text, daemon=True).start()
            return f"Typing: {text}"
        return "What would you like me to type?"

    def handle_scroll_command(self, command):
        """Handle scrolling commands"""
        if "down" in command:
            pyautogui.scroll(-300)  # Scroll down
            return "Scrolling down"
        elif "up" in command:
            pyautogui.scroll(300)   # Scroll up
            return "Scrolling up"
        else:
            pyautogui.scroll(-300)
            return "Scrolling down"

    def take_screenshot(self):
        """Take a screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Couldn't take screenshot: {str(e)}"

    def handle_volume_command(self, command):
        """Handle volume control commands"""
        try:
            if "up" in command:
                for _ in range(5):
                    pyautogui.press('volumeup')
                return "Volume increased"
            elif "down" in command:
                for _ in range(5):
                    pyautogui.press('volumedown')
                return "Volume decreased"
            elif "mute" in command:
                pyautogui.press('volumemute')
                return "Volume muted"
            else:
                # Extract number from command
                import re
                numbers = re.findall(r'\d+', command)
                if numbers:
                    volume_level = int(numbers[0])
                    # This is a simplified volume control
                    return f"Setting volume to {volume_level}% (limited control available)"
                else:
                    return "Please specify volume level or say 'volume up/down/mute'"
        except Exception as e:
            return f"Couldn't control volume: {str(e)}"

    def handle_contact_command(self, command):
        """Handle contact-related commands"""
        if "list" in command or "all" in command or "what are" in command:
            contacts = self.get_contacts()
            if contacts:
                response = "Your contacts:\n" + "\n".join([f"{c[1]} ({c[2]}): {c[3]}" for c in contacts])
            else:
                response = "No contacts stored yet."
        else:
            # Extract contact name from command
            for word in command.split():
                contact_info = self.find_contact(word)
                if contact_info:
                    name, relationship, phone, email = contact_info
                    return f"Found {name} ({relationship}): Phone: {phone}, Email: {email}"
            response = "Who would you like me to find in your contacts?"
        return response

    def handle_task_command(self, command):
        """Handle task-related commands"""
        if "add" in command or "create" in command or "new" in command:
            task_text = command.replace("add", "").replace("create", "").replace("new", "").replace("task", "").strip()
            if task_text:
                self.add_task(task_text)
                return f"Added task: {task_text}"
            else:
                return "What task would you like to add?"
        
        elif "list" in command or "show" in command or "what are" in command:
            tasks = self.get_tasks()
            if tasks:
                response = "Your tasks:\n" + "\n".join([f"- {task[1]}" for task in tasks if not task[4]])
            else:
                response = "No tasks pending."
            return response
        
        else:
            return "I can add tasks or show your current tasks. Try 'add task [description]' or 'show my tasks'."

    def handle_note_command(self, command):
        """Handle note-taking commands"""
        if "remember" in command:
            note_text = command.replace("remember", "").replace("that", "").replace("i", "").replace("like", "").strip()
            if note_text:
                self.add_note("Personal Note", note_text)
                return f"I'll remember that: {note_text}"
        return "What would you like me to remember?"

    def get_weather(self):
        try:
            # Using a simple weather API
            response = requests.get("http://wttr.in/?format=3", timeout=5)
            if response.status_code == 200:
                return f"Weather: {response.text.strip()}"
        except:
            pass
        return "Couldn't fetch weather information. Please check your connection."

    def get_contacts(self):
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        conn.close()
        return contacts

    def find_contact(self, name):
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR relationship LIKE ?", 
                      (f'%{name}%', f'%{name}%'))
        contact = cursor.fetchone()
        conn.close()
        return contact

    def add_contact(self, name, relationship, phone, email, notes):
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, relationship, phone, email, notes) VALUES (?, ?, ?, ?, ?)",
            (name, relationship, phone, email, notes)
        )
        conn.commit()
        conn.close()

    def get_tasks(self):
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE completed = 0 ORDER BY created_date DESC")
        tasks = cursor.fetchall()
        conn.close()
        return tasks

    def add_task(self, task_text, priority="medium"):
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task, priority, created_date) VALUES (?, ?, ?)",
            (task_text, priority, datetime.datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def add_note(self, title, content, category="personal"):
        conn = sqlite3.connect('personal_assistant.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content, created_date, category) VALUES (?, ?, ?, ?)",
            (title, content, datetime.datetime.now().isoformat(), category)
        )
        conn.commit()
        conn.close()

    def get_joke(self):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
            if response.status_code == 200:
                joke_data = response.json()
                return f"{joke_data['setup']} ... {joke_data['punchline']}"
        except:
            pass
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
        ]
        import random
        return random.choice(jokes)

    def speak(self, text):
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
        Thread(target=speak_thread, daemon=True).start()

    def add_to_conversation(self, speaker, text):
        if hasattr(self, 'conversation_area'):
            self.conversation_area.config(state=tk.NORMAL)
            self.conversation_area.insert(tk.END, f"{speaker}: {text}\n")
            self.conversation_area.see(tk.END)
            self.conversation_area.config(state=tk.DISABLED)

    # UI management methods (only work if UI is initialized)
    def manage_profile(self):
        if not self.root:
            return
        # ... (your existing manage_profile implementation)

    def manage_contacts(self):
        if not self.root:
            return
        # ... (your existing manage_contacts implementation)

    def manage_tasks(self):
        if not self.root:
            return
        # ... (your existing manage_tasks implementation)

    def show_quick_actions(self):
        if not self.root:
            return
        # ... (your existing show_quick_actions implementation)

    def manage_apps(self):
        if not self.root:
            return
        # ... (your existing manage_apps implementation)

    def show_add_contact_dialog(self, parent, callback):
        if not self.root:
            return
        # ... (your existing show_add_contact_dialog implementation)