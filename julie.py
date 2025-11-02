import streamlit as st
import datetime
import re
import time
import random


BACKEND_URL = ("BACKEND_URL",
            " http://0.0.0.0:8000")

# Simulated data (replace with actual logic)
def simulate_speak(text):
    st.markdown(f'<div class="ai-response-bubble">🤖 <strong>Assistant:</strong> {text}</div>', unsafe_allow_html=True)

def handle_calculation(cmd):
    try:
        math = re.sub(r'calculate|what is|compute', '', cmd)
        math = re.sub(r'plus|add', '+', math)
        math = re.sub(r'minus|subtract', '-', math)
        math = re.sub(r'times|multiply|multiplied by', '*', math)
        math = re.sub(r'divided by|divide', '/', math)
        math = re.sub(r'\s+', ' ', math).strip()

        match = re.match(r'(-?\d*\.?\d+)\s*([\+\-\\/])\s(-?\d*\.?\d+)', math)
        if match:
            num1 = float(match.group(1))
            op = match.group(2)
            num2 = float(match.group(3))
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    return "Division by zero is not allowed."
                result = num1 / num2
            else:
                return "Invalid operator."
            formatted = int(result) if float(result).is_integer() else round(result, 2)
            return f"The result is {formatted}"
        return "I couldn't parse that calculation. Try 'calculate 15 plus 7' or similar."
    except Exception:
        return "An error occurred during calculation."

def process_command(command):
    cmd = command.lower()
    result = ""

    start_time = time.time()
    if 'time' in cmd:
        now = datetime.datetime.now()
        result = f"The current time is {now.strftime('%I:%M:%S %p')}"
    elif 'date' in cmd:
        now = datetime.datetime.now()
        result = f"Today is {now.strftime('%A, %B %d, %Y')}"
    elif any(word in cmd for word in ['calculate', 'plus', 'minus', 'times', 'divided']):
        result = handle_calculation(cmd)
    elif 'search for' in cmd:
        query = cmd.split('search for')[1].strip() if len(cmd.split('search for')) > 1 else ''
        if query:
            result = f'Searching for "{query}". Opening your browser...'
            st.info(f"🔍 Simulating browser open: https://www.google.com/search?q={query}")
        else:
            result = "What would you like to search for?"
    elif 'weather' in cmd:
        location = cmd.split('in')[1].strip() if 'in' in cmd else 'your area'
        result = f"Checking weather in {location}. Opening search..."
        st.info(f"☁ Simulating browser open: https://www.google.com/search?q=weather {location}")
    elif any(g in cmd for g in ['hello', 'hi', 'hey']):
        result = "Hello! I'm your AI voice assistant. How can I help you today? Ask about time, date, calculations, or search anything!"
    elif any(h in cmd for h in ['help', 'commands']):
        result = "Available commands: time/date, calculations (e.g., 'calculate 10 plus 5'), search (e.g., 'search for AI'), weather. Just speak naturally!"
    elif 'joke' in cmd:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call fake spaghetti? An impasta!"
        ]
        result = random.choice(jokes)
    else:
        result = f"I heard: '{command}'. That's interesting! For now, I can help with time, date, math, searches, weather, or tell a joke. What else?"

    end_time = time.time()
    response_time = int((end_time - start_time) * 1000)
    return result, response_time

# Streamlit App Configuration
st.set_page_config(page_title="JULIE AI", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")

# Session state initialization
if 'history' not in st.session_state:
    st.session_state.history = []
if 'commands_processed' not in st.session_state:
    st.session_state.commands_processed = 0
if 'avg_response' not in st.session_state:
    st.session_state.avg_response = 500
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False

# Ultra Modern CSS with Stunning Graphics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Audiowide&family=Iceland&display=swap');

/* ========== LIQUID AURORA BACKGROUND ========== */
.main {
    background: 
        radial-gradient(ellipse at 20% 30%, rgba(255, 50, 200, 0.35) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 70%, rgba(50, 200, 255, 0.35) 0%, transparent 50%),
        radial-gradient(ellipse at 40% 80%, rgba(150, 50, 255, 0.3) 0%, transparent 45%),
        radial-gradient(ellipse at 60% 20%, rgba(255, 150, 50, 0.25) 0%, transparent 50%),
        linear-gradient(135deg, #0a0015 0%, #1a0530 25%, #0f1b3a 50%, #1a0530 75%, #0a0015 100%);
    background-size: 400% 400%, 400% 400%, 500% 500%, 450% 450%, 100% 100%;
    animation: liquidFlow 25s ease-in-out infinite;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
    font-family: 'Space Grotesk', sans-serif;
}

@keyframes liquidFlow {
    0%, 100% { 
        background-position: 0% 50%, 100% 50%, 50% 100%, 50% 0%, 0% 0%;
        filter: brightness(1) saturate(1.2);
    }
    33% { 
        background-position: 100% 0%, 0% 100%, 0% 50%, 100% 50%, 0% 0%;
        filter: brightness(1.1) saturate(1.4);
    }
    66% { 
        background-position: 50% 100%, 50% 0%, 100% 0%, 0% 100%, 0% 0%;
        filter: brightness(1.05) saturate(1.3);
    }
}

/* ========== FLOATING GEOMETRIC SHAPES ========== */
.geometric-shape {
    position: fixed;
    pointer-events: none;
    z-index: 1;
    opacity: 0.4;
    filter: blur(1px);
    border: 2px solid;
    animation: shapeFloat 30s ease-in-out infinite;
}

@keyframes shapeFloat {
    0%, 100% {
        transform: translate(0, 0) rotate(0deg) scale(1);
        opacity: 0.3;
    }
    25% {
        transform: translate(100px, -150px) rotate(90deg) scale(1.2);
        opacity: 0.5;
    }
    50% {
        transform: translate(-80px, 100px) rotate(180deg) scale(0.9);
        opacity: 0.4;
    }
    75% {
        transform: translate(120px, 50px) rotate(270deg) scale(1.1);
        opacity: 0.6;
    }
}

/* ========== ANIMATED GRADIENT BLOBS ========== */
.gradient-blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    mix-blend-mode: screen;
    pointer-events: none;
    z-index: 2;
    animation: blobMorph 20s ease-in-out infinite;
}

@keyframes blobMorph {
    0%, 100% {
        transform: translate(0, 0) scale(1) rotate(0deg);
        border-radius: 50% 50% 50% 50%;
    }
    33% {
        transform: translate(80px, -100px) scale(1.3) rotate(120deg);
        border-radius: 60% 40% 50% 50%;
    }
    66% {
        transform: translate(-60px, 80px) scale(0.9) rotate(240deg);
        border-radius: 40% 60% 60% 40%;
    }
}

/* ========== DYNAMIC LIGHTNING BOLTS ========== */
.lightning {
    position: fixed;
    width: 3px;
    height: 200px;
    background: linear-gradient(180deg, 
        rgba(100, 200, 255, 0) 0%,
        rgba(100, 200, 255, 0.8) 50%,
        rgba(255, 100, 200, 0.8) 100%);
    box-shadow: 0 0 20px rgba(100, 200, 255, 0.8);
    pointer-events: none;
    z-index: 3;
    animation: lightning 8s ease-in-out infinite;
    transform-origin: top center;
}

@keyframes lightning {
    0%, 90%, 100% {
        opacity: 0;
        transform: scaleY(0) translateX(0) skewX(0deg);
    }
    91% {
        opacity: 1;
        transform: scaleY(1) translateX(20px) skewX(15deg);
    }
    92% {
        opacity: 0;
    }
    93% {
        opacity: 1;
        transform: scaleY(1) translateX(-10px) skewX(-10deg);
    }
    94%, 100% {
        opacity: 0;
    }
}

/* ========== CONSTELLATION NETWORK ========== */
.constellation {
    position: fixed;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
}

.constellation-dot {
    position: absolute;
    width: 4px;
    height: 4px;
    background: radial-gradient(circle, rgba(100, 200, 255, 1), transparent);
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(100, 200, 255, 0.8);
    animation: dotPulse 4s ease-in-out infinite;
}

@keyframes dotPulse {
    0%, 100% {
        opacity: 0.5;
        transform: scale(1);
        box-shadow: 0 0 10px rgba(100, 200, 255, 0.8);
    }
    50% {
        opacity: 1;
        transform: scale(1.5);
        box-shadow: 0 0 20px rgba(100, 200, 255, 1);
    }
}

/* ========== ENERGY WAVES ========== */
.energy-wave {
    position: fixed;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 2;
    background: 
        repeating-linear-gradient(
            90deg,
            transparent 0px,
            rgba(100, 200, 255, 0.03) 1px,
            transparent 2px,
            transparent 40px
        );
    animation: waveScroll 15s linear infinite;
}

@keyframes waveScroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(40px); }
}

/* ========== PARTICLE EXPLOSION ========== */
.particle {
    position: fixed;
    width: 4px;
    height: 4px;
    background: radial-gradient(circle, #ff50c8, #3264ff);
    border-radius: 50%;
    pointer-events: none;
    z-index: 3;
    animation: particleExplode 8s ease-out infinite;
    box-shadow: 0 0 15px rgba(255, 80, 200, 0.8);
}

@keyframes particleExplode {
    0% {
        transform: translate(0, 0) scale(0);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    100% {
        transform: translate(var(--tx), var(--ty)) scale(1);
        opacity: 0;
    }
}

/* ========== HOLOGRAPHIC DISPLAY ========== */
.holographic-line {
    position: fixed;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(100, 200, 255, 0.6) 50%,
        transparent 100%);
    pointer-events: none;
    z-index: 2;
    animation: holoScan 5s linear infinite;
    box-shadow: 0 0 10px rgba(100, 200, 255, 0.8);
}

@keyframes holoScan {
    0% { 
        top: 0%; 
        opacity: 0;
        filter: hue-rotate(0deg);
    }
    5% { opacity: 1; }
    95% { opacity: 1; }
    100% { 
        top: 100%; 
        opacity: 0;
        filter: hue-rotate(360deg);
    }
}

/* ========== GLITCH EFFECT OVERLAY ========== */
.glitch-overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 4;
    background: 
        repeating-linear-gradient(
            0deg,
            transparent 0px,
            rgba(255, 255, 255, 0.01) 1px,
            transparent 2px,
            transparent 4px
        );
    animation: glitchScan 10s steps(100) infinite;
    mix-blend-mode: overlay;
}

@keyframes glitchScan {
    0%, 100% { transform: translateY(0); opacity: 0.05; }
    50% { transform: translateY(-100%); opacity: 0.1; }
}

/* ========== DIGITAL RAIN ========== */
.digital-rain {
    position: fixed;
    width: 2px;
    height: 80px;
    background: linear-gradient(180deg,
        transparent 0%,
        rgba(100, 200, 255, 0.8) 50%,
        transparent 100%);
    pointer-events: none;
    z-index: 2;
    animation: rainFall 5s linear infinite;
    box-shadow: 0 0 10px rgba(100, 200, 255, 0.6);
}

@keyframes rainFall {
    0% {
        transform: translateY(-100%);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translateY(calc(100vh + 100px));
        opacity: 0;
    }
}

/* ========== AURORA RIBBONS ========== */
.aurora-ribbon {
    position: fixed;
    width: 100%;
    height: 300px;
    pointer-events: none;
    z-index: 1;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(255, 50, 200, 0.15) 25%,
        rgba(50, 200, 255, 0.15) 50%,
        rgba(150, 50, 255, 0.15) 75%,
        transparent 100%);
    filter: blur(50px);
    animation: ribbonFlow 20s ease-in-out infinite;
    transform-origin: center;
}

@keyframes ribbonFlow {
    0%, 100% {
        transform: translateX(-10%) skewY(-5deg) scaleY(1);
        opacity: 0.5;
    }
    50% {
        transform: translateX(10%) skewY(5deg) scaleY(1.2);
        opacity: 0.8;
    }
}

/* ========== GLASS MORPHISM CARDS ========== */
.glass-card {
    background: rgba(20, 20, 50, 0.4);
    backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(100, 200, 255, 0.3);
    border-radius: 24px;
    padding: 30px;
    margin: 20px auto;
    max-width: 1000px;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.1),
        0 0 60px rgba(100, 200, 255, 0.1);
    transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
    z-index: 10;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle,
        rgba(100, 200, 255, 0.1) 0%,
        transparent 70%);
    animation: cardGlow 8s ease-in-out infinite;
}

@keyframes cardGlow {
    0%, 100% {
        transform: translate(0, 0);
        opacity: 0.3;
    }
    50% {
        transform: translate(20%, 20%);
        opacity: 0.6;
    }
}

.glass-card:hover {
    transform: translateY(-10px) scale(1.02);
    border-color: rgba(255, 50, 200, 0.5);
    box-shadow: 
        0 20px 60px rgba(255, 50, 200, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        0 0 80px rgba(255, 50, 200, 0.2);
}

/* ========== FUTURISTIC TYPOGRAPHY ========== */
.header {
    font-family: 'Audiowide', cursive;
    font-size: 6rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, 
        #64c8ff 0%, 
        #ff50c8 25%,
        #9650ff 50%,
        #ff9650 75%,
        #64c8ff 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 15px;
    text-transform: uppercase;
    margin: 100px 0 20px;
    animation: headerShine 8s ease-in-out infinite;
    position: relative;
    z-index: 10;
    text-shadow: 0 0 80px rgba(100, 200, 255, 0.5);
    filter: drop-shadow(0 0 30px rgba(255, 50, 200, 0.6));
}

@keyframes headerShine {
    0%, 100% { 
        background-position: 0% 50%;
        filter: drop-shadow(0 0 30px rgba(255, 50, 200, 0.6)) brightness(1);
    }
    50% { 
        background-position: 100% 50%;
        filter: drop-shadow(0 0 50px rgba(100, 200, 255, 0.8)) brightness(1.3);
    }
}

.subtitle {
    text-align: center;
    color: #64c8ff;
    font-family: 'Iceland', cursive;
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: 8px;
    text-transform: uppercase;
    margin-bottom: 80px;
    animation: subtitleFloat 5s ease-in-out infinite;
    text-shadow: 
        0 0 20px rgba(100, 200, 255, 0.8),
        0 0 40px rgba(255, 50, 200, 0.4);
    position: relative;
    z-index: 10;
}

@keyframes subtitleFloat {
    0%, 100% { 
        transform: translateY(0);
        opacity: 0.9;
    }
    50% { 
        transform: translateY(-8px);
        opacity: 1;
    }
}

/* ========== STATS CARDS ========== */
.stats-card {
    background: rgba(20, 20, 50, 0.5);
    backdrop-filter: blur(25px);
    border: 2px solid rgba(100, 200, 255, 0.3);
    border-radius: 20px;
    padding: 28px;
    margin: 18px 0;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
    overflow: hidden;
}

.stats-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(100, 200, 255, 0.2) 50%,
        transparent 100%);
    animation: cardSwipe 4s ease-in-out infinite;
}

@keyframes cardSwipe {
    0%, 100% { left: -100%; }
    50% { left: 100%; }
}

.stats-card:hover {
    transform: translateY(-10px) scale(1.05) rotateY(5deg);
    border-color: rgba(255, 50, 200, 0.6);
    box-shadow: 
        0 20px 50px rgba(255, 50, 200, 0.4),
        inset 0 0 40px rgba(255, 50, 200, 0.15);
}

.stats-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    color: #64c8ff;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 12px;
    font-weight: 600;
    text-shadow: 0 0 10px rgba(100, 200, 255, 0.6);
}

.stats-value {
    font-family: 'Audiowide', cursive;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #64c8ff, #ff50c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 12px;
    filter: drop-shadow(0 0 20px rgba(100, 200, 255, 0.6));
}

.status-active {
    animation: statusPulse 1.2s ease-in-out infinite;
}

.status-idle {
    animation: statusBreathe 3s ease-in-out infinite;
}

@keyframes statusPulse {
    0%, 100% { 
        transform: scale(1);
        filter: drop-shadow(0 0 20px rgba(0, 255, 100, 0.8));
    }
    50% { 
        transform: scale(1.1);
        filter: drop-shadow(0 0 40px rgba(0, 255, 100, 1));
    }
}

@keyframes statusBreathe {
    0%, 100% { opacity: 0.8; }
    50% { opacity: 1; }
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, 
        rgba(100, 200, 255, 0.3) 0%, 
        rgba(255, 50, 200, 0.3) 100%) !important;
    backdrop-filter: blur(20px);
    color: #ffffff !important;
    border: 2px solid rgba(100, 200, 255, 0.5) !important;
    border-radius: 18px !important;
    padding: 18px 40px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    text-transform: uppercase !important;
    letter-spacing: 4px !important;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
    box-shadow: 
        0 10px 35px rgba(100, 200, 255, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent 70%);
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
    border-radius: 50%;
}

.stButton > button:hover::before {
    width: 400px;
    height: 400px;
}

.stButton > button:hover {
    transform: translateY(-8px) scale(1.05);
    border-color: rgba(255, 50, 200, 0.8) !important;
    box-shadow: 
        0 20px 60px rgba(255, 50, 200, 0.6),
        inset 0 1px 0 rgba(255, 255, 255, 0.3),
        0 0 40px rgba(255, 50, 200, 0.4);
    background: linear-gradient(135deg, 
        rgba(100, 200, 255, 0.4) 0%, 
        rgba(255, 50, 200, 0.4) 100%) !important;
}

.stButton > button:active {
    transform: translateY(-4px) scale(1.02);
}

/* ========== INPUT FIELDS ========== */
.stTextInput > div > div > input {
    background: rgba(15, 15, 40, 0.7) !important;
    backdrop-filter: blur(25px);
    border: 2px solid rgba(100, 200, 255, 0.4) !important;
    border-radius: 18px !important;
    color: #ffffff !important;
    padding: 22px !important;
    font-size: 1.25rem !important;
    font-family: 'Space Grotesk', sans-serif;
    transition: all 0.4s ease !important;
    box-shadow: 
        inset 0 2px 20px rgba(0, 0, 0, 0.4),
        0 4px 30px rgba(100, 200, 255, 0.2);
}

.stTextInput > div > div > input::placeholder {
    color: rgba(100, 200, 255, 0.5) !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(255, 50, 200, 0.8) !important;
    box-shadow: 
        inset 0 2px 30px rgba(255, 50, 200, 0.2),
        0 0 60px rgba(255, 50, 200, 0.5) !important;
    background: rgba(20, 20, 50, 0.9) !important;
    transform: scale(1.02);
}

/* ========== AI RESPONSE BUBBLE ========== */
.ai-response-bubble {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    line-height: 1.9;
    color: #ffffff;
    padding: 28px 35px;
    background: linear-gradient(135deg, 
        rgba(100, 200, 255, 0.15) 0%, 
        rgba(150, 50, 255, 0.15) 100%);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(100, 200, 255, 0.3);
    border-left: 5px solid #64c8ff;
    animation: bubbleSlideIn 0.8s cubic-bezier(0.23, 1, 0.32, 1);
    margin: 25px 0;
    box-shadow: 
        0 10px 40px rgba(100, 200, 255, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.ai-response-bubble::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg,
        transparent 0%,
        rgba(100, 200, 255, 0.1) 50%,
        transparent 100%);
    transform: translateX(-100%);
    animation: bubbleShimmer 3s ease-in-out infinite;
}

@keyframes bubbleSlideIn {
    from {
        opacity: 0;
        transform: translateX(-40px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateX(0) scale(1);
    }
}

@keyframes bubbleShimmer {
    0%, 100% { transform: translateX(-100%); }
    50% { transform: translateX(100%); }
}

.ai-response-bubble:hover {
    border-color: rgba(255, 50, 200, 0.5);
    border-left-color: #ff50c8;
    box-shadow: 
        0 15px 50px rgba(255, 50, 200, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transform: translateY(-3px);
}

/* ========== STATUS INDICATOR ========== */
.status {
    text-align: center;
    font-family: 'Audiowide', cursive;
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin: 30px 0;
    padding: 20px;
    border-radius: 18px;
    background: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(20px);
    border: 2px solid;
    position: relative;
    z-index: 10;
}

/* ========== SECTIONS ========== */
.history-section, .commands-section {
    margin: 35px 0;
    position: relative;
    z-index: 10;
}

.history-title, .commands-title {
    font-family: 'Audiowide', cursive;
    font-size: 2rem;
    font-weight: 700;
    color: #64c8ff;
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 25px;
    text-shadow: 
        0 0 25px rgba(100, 200, 255, 0.8),
        0 0 50px rgba(255, 50, 200, 0.4);
    filter: drop-shadow(0 5px 15px rgba(100, 200, 255, 0.3));
}

/* ========== EXPANDERS ========== */
.streamlit-expanderHeader {
    background: rgba(20, 20, 50, 0.5) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(100, 200, 255, 0.3) !important;
    border-radius: 15px !important;
    color: #64c8ff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.4s ease !important;
}

.streamlit-expanderHeader:hover {
    border-color: rgba(255, 50, 200, 0.5) !important;
    box-shadow: 0 10px 40px rgba(255, 50, 200, 0.3);
    background: rgba(25, 25, 60, 0.6) !important;
    transform: translateY(-2px);
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
    width: 14px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 15, 40, 0.5);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #64c8ff 0%, #ff50c8 50%, #9650ff 100%);
    border-radius: 10px;
    border: 2px solid rgba(15, 15, 40, 0.5);
    box-shadow: 0 0 10px rgba(100, 200, 255, 0.5);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #ff50c8 0%, #9650ff 50%, #64c8ff 100%);
    box-shadow: 0 0 20px rgba(255, 50, 200, 0.8);
}

/* ========== HIDE STREAMLIT ELEMENTS ========== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ========== INFO BOX ========== */
.stInfo {
    background: rgba(100, 200, 255, 0.1) !important;
    backdrop-filter: blur(20px);
    border-left: 5px solid #64c8ff !important;
    border-radius: 15px !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    box-shadow: 0 5px 25px rgba(100, 200, 255, 0.2);
}
</style>
""", unsafe_allow_html=True)

# === STUNNING BACKGROUND GRAPHICS ===
st.markdown("""
<!-- Gradient Blobs -->
<div class="gradient-blob" style="top: 10%; left: 15%; width: 300px; height: 300px; background: radial-gradient(circle, rgba(100, 200, 255, 0.4), transparent); animation-delay: 0s;"></div>
<div class="gradient-blob" style="top: 60%; left: 75%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(255, 50, 200, 0.4), transparent); animation-delay: -7s;"></div>
<div class="gradient-blob" style="top: 80%; left: 20%; width: 250px; height: 250px; background: radial-gradient(circle, rgba(150, 50, 255, 0.4), transparent); animation-delay: -14s;"></div>
<div class="gradient-blob" style="top: 30%; left: 80%; width: 350px; height: 350px; background: radial-gradient(circle, rgba(255, 150, 50, 0.3), transparent); animation-delay: -10s;"></div>

<!-- Geometric Shapes -->
<div class="geometric-shape" style="top: 15%; left: 25%; width: 80px; height: 80px; border-color: rgba(100, 200, 255, 0.4); border-radius: 10px; animation-delay: 0s;"></div>
<div class="geometric-shape" style="top: 70%; left: 65%; width: 100px; height: 100px; border-color: rgba(255, 50, 200, 0.4); clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%); animation-delay: -8s;"></div>
<div class="geometric-shape" style="top: 40%; left: 10%; width: 60px; height: 60px; border-color: rgba(150, 50, 255, 0.4); border-radius: 50%; animation-delay: -15s;"></div>
<div class="geometric-shape" style="top: 55%; left: 85%; width: 70px; height: 70px; border-color: rgba(255, 150, 50, 0.4); clip-path: polygon(50% 0%, 0% 100%, 100% 100%); animation-delay: -5s;"></div>
<div class="geometric-shape" style="top: 25%; left: 70%; width: 90px; height: 90px; border-color: rgba(100, 200, 255, 0.3); transform: rotate(45deg); animation-delay: -12s;"></div>

<!-- Lightning Bolts -->
<div class="lightning" style="top: 10%; left: 30%; animation-delay: 0s;"></div>
<div class="lightning" style="top: 5%; left: 75%; animation-delay: 3s;"></div>
<div class="lightning" style="top: 15%; left: 50%; animation-delay: 6s;"></div>

<!-- Digital Rain -->
<div class="digital-rain" style="left: 15%; animation-delay: 0s;"></div>
<div class="digital-rain" style="left: 35%; animation-delay: 1.5s;"></div>
<div class="digital-rain" style="left: 55%; animation-delay: 3s;"></div>
<div class="digital-rain" style="left: 75%; animation-delay: 0.5s;"></div>
<div class="digital-rain" style="left: 25%; animation-delay: 2.5s;"></div>
<div class="digital-rain" style="left: 85%; animation-delay: 4s;"></div>
<div class="digital-rain" style="left: 45%; animation-delay: 1s;"></div>
<div class="digital-rain" style="left: 65%; animation-delay: 3.5s;"></div>

<!-- Constellation Network -->
<div class="constellation">
    <div class="constellation-dot" style="top: 20%; left: 30%; animation-delay: 0s;"></div>
    <div class="constellation-dot" style="top: 25%; left: 45%; animation-delay: 0.5s;"></div>
    <div class="constellation-dot" style="top: 35%; left: 60%; animation-delay: 1s;"></div>
    <div class="constellation-dot" style="top: 50%; left: 25%; animation-delay: 1.5s;"></div>
    <div class="constellation-dot" style="top: 55%; left: 70%; animation-delay: 2s;"></div>
    <div class="constellation-dot" style="top: 65%; left: 40%; animation-delay: 2.5s;"></div>
    <div class="constellation-dot" style="top: 75%; left: 55%; animation-delay: 3s;"></div>
    <div class="constellation-dot" style="top: 80%; left: 75%; animation-delay: 3.5s;"></div>
    <div class="constellation-dot" style="top: 40%; left: 80%; animation-delay: 1.2s;"></div>
    <div class="constellation-dot" style="top: 60%; left: 15%; animation-delay: 2.8s;"></div>
</div>

<!-- Energy Waves -->
<div class="energy-wave"></div>

<!-- Aurora Ribbons -->
<div class="aurora-ribbon" style="top: 15%; animation-delay: 0s;"></div>
<div class="aurora-ribbon" style="bottom: 20%; animation-delay: -10s;"></div>

<!-- Holographic Lines -->
<div class="holographic-line" style="animation-delay: 0s;"></div>
<div class="holographic-line" style="animation-delay: 2.5s;"></div>

<!-- Glitch Overlay -->
<div class="glitch-overlay"></div>

<!-- Particle Explosion (emanating from center) -->
<div class="particle" style="top: 50%; left: 50%; --tx: 200px; --ty: -150px; animation-delay: 0s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: -180px; --ty: -120px; animation-delay: 0.5s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: 150px; --ty: 180px; animation-delay: 1s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: -220px; --ty: 100px; animation-delay: 1.5s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: 100px; --ty: -200px; animation-delay: 2s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: -150px; --ty: 180px; animation-delay: 2.5s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: 250px; --ty: 50px; animation-delay: 3s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: -100px; --ty: -180px; animation-delay: 3.5s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: 180px; --ty: 120px; animation-delay: 4s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: -200px; --ty: -80px; animation-delay: 4.5s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: 120px; --ty: -160px; animation-delay: 5s;"></div>
<div class="particle" style="top: 50%; left: 50%; --tx: -160px; --ty: 140px; animation-delay: 5.5s;"></div>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="header">Julie Ai Assisstant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">◇ Advanced Neural Interface System ◇</p>', unsafe_allow_html=True)

# Layout: Two columns - Left for stats, right for main content
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<div class="stats-card"><div class="stats-label">Commands Processed</div><div class="stats-value">{}</div></div>'.format(st.session_state.commands_processed), unsafe_allow_html=True)
    status_emoji = "🔴" if st.session_state.is_listening else "🟢"
    status_text = "ACTIVE" if st.session_state.is_listening else "STANDBY"
    status_class = "status-active" if st.session_state.is_listening else "status-idle"
    st.markdown(f'<div class="stats-card"><div class="stats-label">Neural Status</div><div class="stats-value {status_class}">{status_emoji} {status_text}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="stats-card"><div class="stats-label">Response Time</div><div class="stats-value">{:.0f}ms</div></div>'.format(st.session_state.avg_response), unsafe_allow_html=True)

with col2:
    # Mic button and status
    if st.button("🎙 ACTIVATE VOICE", key="mic_btn", help="Toggle Neural Interface"):
        st.session_state.is_listening = not st.session_state.is_listening
        st.rerun()
    
    status_text_full = f"{status_emoji} {'NEURAL INTERFACE ONLINE - LISTENING MODE' if st.session_state.is_listening else 'SYSTEM READY - AWAITING COMMAND'}"
    st.markdown(f'<p class="status {status_class}" style="border-color: {"rgba(0, 255, 100, 0.6)" if st.session_state.is_listening else "rgba(100, 200, 255, 0.4)"}; color: {"#00ff64" if st.session_state.is_listening else "#64c8ff"};">{status_text_full}</p>', unsafe_allow_html=True)

    # Transcript input
    transcript = st.text_input("", key="transcript_input", placeholder="◇ Enter neural command or speak naturally...", label_visibility="collapsed")
    if transcript:
        result, resp_time = process_command(transcript)
        st.session_state.commands_processed += 1
        st.session_state.avg_response = (st.session_state.avg_response * (st.session_state.commands_processed - 1) + resp_time) / st.session_state.commands_processed if st.session_state.commands_processed > 0 else resp_time
        st.session_state.history.append({"command": transcript, "response": result, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})
        simulate_speak(result)
        st.rerun()

    # Response display
    if st.session_state.history:
        last_response = st.session_state.history[-1]["response"]
        st.markdown(f'<div class="ai-response-bubble">{last_response}</div>', unsafe_allow_html=True)

    # Quick Commands
    st.markdown('<div class="commands-section"><div class="commands-title">⚡ QUICK ACCESS COMMANDS</div></div>', unsafe_allow_html=True)
    col_cmd1, col_cmd2, col_cmd3 = st.columns(3)
    with col_cmd1:
        if st.button("⏰ TIME"):
            result, resp_time = process_command("What time is it?")
            st.session_state.commands_processed += 1
            st.session_state.avg_response = (st.session_state.avg_response * (st.session_state.commands_processed - 1) + resp_time) / st.session_state.commands_processed if st.session_state.commands_processed > 0 else resp_time
            st.session_state.history.append({"command": "What time is it?", "response": result, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})
            simulate_speak(result)
            st.rerun()
    with col_cmd2:
        if st.button("📅 DATE"):
            result, resp_time = process_command("What's the date?")
            st.session_state.commands_processed += 1
            st.session_state.avg_response = (st.session_state.avg_response * (st.session_state.commands_processed - 1) + resp_time) / st.session_state.commands_processed if st.session_state.commands_processed > 0 else resp_time
            st.session_state.history.append({"command": "What's the date?", "response": result, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})
            simulate_speak(result)
            st.rerun()
    with col_cmd3:
        if st.button("🔢 CALCULATE"):
            result, resp_time = process_command("Calculate 15 plus 23")
            st.session_state.commands_processed += 1
            st.session_state.avg_response = (st.session_state.avg_response * (st.session_state.commands_processed - 1) + resp_time) / st.session_state.commands_processed if st.session_state.commands_processed > 0 else resp_time
            st.session_state.history.append({"command": "Calculate 15 plus 23", "response": result, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})
            simulate_speak(result)
            st.rerun()

    col_cmd4, col_cmd5, col_cmd6 = st.columns(3)
    with col_cmd4:
        if st.button("☁ WEATHER"):
            result, resp_time = process_command("Weather today")
            st.session_state.commands_processed += 1
            st.session_state.avg_response = (st.session_state.avg_response * (st.session_state.commands_processed - 1) + resp_time) / st.session_state.commands_processed if st.session_state.commands_processed > 0 else resp_time
            st.session_state.history.append({"command": "Weather today", "response": result, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})
            simulate_speak(result)
            st.rerun()
    with col_cmd5:
        if st.button("🔍 SEARCH"):
            result, resp_time = process_command("Search for AI news")
            st.session_state.commands_processed += 1
            st.session_state.avg_response = (st.session_state.avg_response * (st.session_state.commands_processed - 1) + resp_time) / st.session_state.commands_processed if st.session_state.commands_processed > 0 else resp_time
            st.session_state.history.append({"command": "Search for AI news", "response": result, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})
            simulate_speak(result)
            st.rerun()
    with col_cmd6:
        if st.button("😄 HUMOR"):
            result, resp_time = process_command("Tell a joke")
            st.session_state.commands_processed += 1
            st.session_state.avg_response = (st.session_state.avg_response * (st.session_state.commands_processed - 1) + resp_time) / st.session_state.commands_processed if st.session_state.commands_processed > 0 else resp_time
            st.session_state.history.append({"command": "Tell a joke", "response": result, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})
            simulate_speak(result)
            st.rerun()

    # History
    st.markdown('<div class="history-section"><div class="history-title">◇ NEURAL HISTORY LOG ◇</div></div>', unsafe_allow_html=True)
    if st.session_state.history:
        for item in st.session_state.history[-8:]:
            with st.expander(f"[{item['timestamp']}] USER: {item['command'][:50]}{'...' if len(item['command']) > 50 else ''}"):
                st.markdown(f'<div class="ai-response-bubble"><strong>USER:</strong> {item["command"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="ai-response-bubble"><strong>🤖 NEXUS AI:</strong> {item["response"]}</div>', unsafe_allow_html=True)
    else:
        st.info("◇ Neural history empty. Initialize interface and execute commands to begin. ◇")