import speech_recognition as sr
import pyttsx3
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from fuzzywuzzy import fuzz
import subprocess
import os
import openai
from dotenv import load_dotenv 

load_dotenv()  
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

ibm_api_key = os.getenv("IBM_API_KEY")
ibm_service_url = os.getenv("IBM_SERVICE_URL")

authenticator = IAMAuthenticator(ibm_api_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(ibm_service_url)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech using IBM Watson Speech to Text
def recognize_speech_ibm_watson():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        
        audio_data = audio.get_wav_data()
        
        response = speech_to_text.recognize(
            audio=audio_data,
            content_type='audio/wav',
            model='en-US_BroadbandModel'
        ).get_result()
        
        text = response['results'][0]['alternatives'][0]['transcript']
        print(f"Recognized Text: {text}")  # Debugging: Show the recognized text
        return text.lower()

def execute_command(command):
    try:
        if 'open notepad' in command:
            speak("Opening Notepad")
            subprocess.Popen(["notepad.exe"])
        elif 'open browser' in command:
            speak("Opening your browser")
            browser_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            if os.path.exists(browser_path):
                subprocess.Popen([browser_path])
            else:
                speak("Browser not found.")
        elif 'play music' in command:
            music_dir = "C:\\Users\\YourUsername\\Music"
            if os.path.exists(music_dir) and os.listdir(music_dir):
                songs = os.listdir(music_dir)
                subprocess.Popen(["start", os.path.join(music_dir, songs[0])], shell=True)
                speak("Playing music")
            else:
                speak("No music found in the directory.")
        elif 'shutdown' in command:
            speak("Shutting down the system")
            subprocess.Popen(["shutdown", "/s", "/t", "1"])
        elif 'search' in command:
            query = command.replace('search', '').strip()
            speak(f"Searching {query}")
            subprocess.Popen(["start", f"https://www.google.com/search?q={query}"], shell=True)
        else:
            speak("Sorry, I don't know how to do that yet.")
    except Exception as e:
        speak(f"An error occurred: {e}")


def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use "gpt-4" or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Kyle."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Sorry, I couldn't process that. Error: {e}"

# Function to generate a response using fuzzy matching
def generate_response(prompt):
    responses = {
        "hello": "Hello! How are you today?",
        "how are you": "I'm just a program, but I'm doing great! How about you?",
        "what is your name": "My name is Kyle, your personal assistant.",
        "what can you do": "I can assist you with basic tasks and answer simple questions.",
        "thank you": "You're welcome! I'm here to help.",
        "goodbye": "Goodbye! Have a great day!",
    }

    # Use fuzzy matching to find the best match
    for key in responses.keys():
        if fuzz.ratio(prompt, key) > 90:  # 80 is the similarity threshold; adjust as needed
            return responses[key]

    return get_openai_response(prompt)

# Main loop
if __name__ == "__main__":
    speak("Hello, I am Kyle, your personal assistant. How can I help you today?")
    
    while True:
        try:
            command = recognize_speech_ibm_watson()
            if command:
                if "goodbye" in command or "bye" in command:
                    speak("Goodbye! Have a great day!")
                    break

                if any(keyword in command for keyword in ["open", "play", "shutdown", "search"]):
                    execute_command(command)
                else:
                    response = generate_response(command)
                    print(f"Kyle: {response}")
                    speak(response)
            else:
                speak("I didn't catch that. Please try again.")
        except Exception as e:
            speak(f"An error occurred: {e}")