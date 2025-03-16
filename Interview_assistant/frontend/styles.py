#frontend/styles.py
import streamlit as st
def apply_dark_theme():
    st.markdown("""
    <style>
    /* Dark theme for the entire app */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Message layout container */
    .message-container {
        display: flex;
        width: 100%;
        margin-bottom: 25px;  /* Increased from 15px */
    }
    
    /* Style chat bubbles */
    .chat-bubble {
        padding: 12px;
        border-radius: 8px;
        color: white;
        word-wrap: break-word;
        margin-bottom: 20px;  /* Added margin to separate bubbles */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);  /* Added shadow for depth */
    }
    
    /* Human message container - right aligned, 50% width */
    .human-container {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin-bottom: 20px;  /* Added margin between containers */
    }
    
    /* Human bubble - right aligned, blue background */
    .human-bubble {
        background-color: #1E3A8A;
        margin-left: auto;
        width: 50%; /* Set to exactly half the width */
        text-align: right;
    }
    
    /* AI bubble - left aligned, dark gray background */
    .ai-bubble {
        background-color: #3C3C3C;
        width: 90%; /* Slightly wider for questions */
        margin-right: auto;
        margin-bottom: 20px;  /* Extra space after AI messages */
    }
    
    /* Input area styling */
    .stTextInput input, .stTextArea textarea {
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #444;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #2C5EF7;
        color: white;
        border: none;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: white !important;
    }
    
    /* Loading animation */
    @keyframes thinking {
        0% { transform: scale(0.8); opacity: 0.3; }
        50% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0.8); opacity: 0.3; }
    }
    
    .thinking-dot {
        width: 12px;
        height: 12px;
        background-color: #4CAF50;
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: thinking 1s infinite;
    }
    
    .thinking-dot:nth-child(1) { animation-delay: 0s; }
    .thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dot:nth-child(3) { animation-delay: 0.4s; }
    
    .thinking-container {
        padding: 10px;
        border-radius: 8px;
        background-color: #1E1E1E;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    /* Form styling */
    .stForm {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
    }
    
    /* Chat container scrolling */
    .chat-container {
        height: 65vh;
        overflow-y: auto;
        padding: 10px;
        margin-bottom: 15px;
    }
    
    /* Code blocks in messages */
    pre {
        background-color: #2D2D2D;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
        color: #E0E0E0;
    }
    
    code {
        font-family: monospace;
        background-color: #2D2D2D;
        padding: 2px 4px;
        border-radius: 3px;
        color: #E0E0E0;
    }
    
    /* Tab warning effect */
    @keyframes red-pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 20px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
    
    .warning-active {
        animation: red-pulse 2s infinite;
        border: 2px solid red;
    }
    
    /* Warning text */
    .warning-text {
        color: #ff4040;
        font-weight: bold;
        padding: 10px;
        background-color: rgba(255, 0, 0, 0.1);
        border-radius: 5px;
        margin-bottom: 15px;
        display: none;
    }
    
    .warning-text.visible {
        display: block;
    }
    </style>
    
    <script>
    // Tab visibility detection
    var warningVisible = false;
    
    document.addEventListener('visibilitychange', function() {
        const mainContainer = document.querySelector('.stApp');
        const warningText = document.getElementById('tab-warning');
        
        if (document.hidden) {
            // User switched away from tab - add warning class
            mainContainer.classList.add('warning-active');
            localStorage.setItem('tabHidden', 'true');
            warningVisible = true;
        } else {
            // User returned to tab - keep warning until acknowledged
            if (warningVisible && warningText) {
                warningText.classList.add('visible');
            }
        }
    });
    
    // Function to acknowledge warning
    function acknowledgeWarning() {
        const mainContainer = document.querySelector('.stApp');
        const warningText = document.getElementById('tab-warning');
        
        mainContainer.classList.remove('warning-active');
        if (warningText) {
            warningText.classList.remove('visible');
        }
        
        localStorage.setItem('tabHidden', 'false');
        warningVisible = false;
    }
    
    // Add event listener once DOM is fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Check on page load if we need to show the warning
        if (localStorage.getItem('tabHidden') === 'true') {
            document.querySelector('.stApp').classList.add('warning-active');
            document.getElementById('tab-warning').classList.add('visible');
            warningVisible = true;
        }
        
        // Add click handler for acknowledge button
        const ackButton = document.getElementById('acknowledge-btn');
        if (ackButton) {
            ackButton.addEventListener('click', acknowledgeWarning);
        }
    });
    </script>
    """, unsafe_allow_html=True)
