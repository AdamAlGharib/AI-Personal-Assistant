# Kyle – AI Personal Voice Assistant

Kyle is a Python-based voice assistant that combines speech recognition, AI-driven natural language responses, and command execution to help users automate everyday tasks via voice. Built with IBM Watson and OpenAI GPT, Kyle understands spoken commands and intelligently responds or performs actions on your system.

## Features

- Voice recognition with IBM Watson Speech-to-Text
- Intelligent dialogue generation using OpenAI GPT
- Local command execution (open apps, play music, web search, etc.)
- Fuzzy logic for matching spoken phrases
- Secure configuration using environment variables

## Technologies Used

- Python
- speech_recognition
- pyttsx3
- ibm-watson
- openai
- fuzzywuzzy
- python-dotenv

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/AdamAlGharib/AI-Personal-Assistant.git
   cd AI-Personal-Assistant
   
2. Install the required dependencies:
  
   pip install -r requirements.txt

3. Create a .env file in the project root with your API credentials:
   
   OPENAI_API_KEY=your-openai-api-key
   IBM_API_KEY=your-ibm-api-key
   IBM_SERVICE_URL=your-ibm-service-url

4. Run the assistant:

   python kyle.py
