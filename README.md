AI Interview Assistant
An AI chatbot to assist in initial technical screening interviews.
Problem Statement
Initial technical screening rounds are often inefficient due to manual question crafting, inconsistent evaluations, and time constraints. This AI Technical Interview Assistant automates the screening process, provides structured feedback, and ensures a fair evaluation experience.
Technical Stack

Python: Application logic, data processing (scikit-learn), and UI (Streamlit)
JavaScript: Tab-switching detection and UI enhancements
Data Storage: JSON files for chat history and candidate details
AI and NLP: LangChain, Ollama (llama3.2 model), scikit-learn (TF-IDF)
UI: Streamlit with custom CSS/JavaScript

Installation and Setup
Prerequisites

Python 3.8+
Ollama (for running the local LLM)
Git

Steps

Clone the Repository
bashCopygit clone https://github.com/[your-username]/AI-Technical-Interview-Assistant.git
cd AI-Technical-Interview-Assistant

Set Up Virtual Environment
bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies
bashCopypip install -r requirements.txt

Install and Configure Ollama

Download and install Ollama from ollama.ai
Pull the llama3.2 model:
bashCopyollama pull llama3.2

Start Ollama:
bashCopyollama serve



Run the Application
bashCopystreamlit run app.py


Usage

Onboarding: Input candidate details (name, experience, tech stack, focus areas)
Conducting the Interview: The AI generates questions based on responses
Assessment: After 10 questions, get structured feedback on performance

Key Features

Adaptive Question Generation: Tailors questions to candidate responses
Real-Time Integrity Monitoring: Detects tab-switching for fair assessment
Structured Assessments: Provides actionable feedback
Cost-Free Solution: Uses open-source tools for accessibility
Professional UI: Dark theme with interactive elements

Methodology

Candidate Onboarding: Gather and store candidate details
Dynamic Question Generation: Create relevant questions with LangChain and Ollama
Interview Assessment: Analyze responses and provide structured feedback
Integrity Monitoring: Detect distractions during the interview
UI and Styling: Professional interface for interviewers

Contributing
Contributions welcome! Fork the repository, create a new branch, and submit a pull request.
License
This project is licensed under the MIT License.
