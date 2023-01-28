import speech_recognition as sr
import webbrowser
import time
import os
import random
import playsound
import requests
import datetime
import pyttsx3
import wikipedia
import json
import wolframalpha
import pafy
from bs4 import BeautifulSoup
import re, requests, subprocess, urllib.parse, urllib.request
from bs4 import BeautifulSoup
import vlc
import openai



engine = pyttsx3.init('sapi5')

# Setting the Voice
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Setting the Volume
volume = engine.getProperty('volume')
engine.setProperty('volume', 10.0)

# Setting the Speed
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)

# Listening for the User Commands
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to Greet the user
def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if(currentH >= 0 and currentH < 6):
        speak("Good night!  Ayan")
    elif(currentH >= 6 and currentH < 12):
        speak("Good morning! Ayan")
    elif(currentH >= 12 and currentH < 18):
        speak("Good afternoon! Ayan")
    elif(currentH >= 18 and currentH < 24):
        speak("Good evening! Ayan")
    greetings = ["How can I help you today?", "What can I do for you?", "How can I assist you?", "What do you need?", "Is there anything I can help you with?"]
    speak(random.choice(greetings))

greetMe()


# Function to listen and response to the user commands
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
    except sr.UnknownValueError:
        speak('Sorry, could not understand. Please try again.')
        query = myCommand() # recursive call to the function to try again

    return query


# Function to search YouTube
def youtubeSearch(query):
    speak("Hold on, I will search YouTube for you.")
    query = query.replace("search", "")
    query = query.replace("YouTube", "")
    query_string = urllib.parse.urlencode({"search_query": query})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    print(clip2)
    if len(clip2)>0:
        webbrowser.open(clip2)
    else:
        webbrowser.open("https://www.youtube.com/results?search_query=" + query)


# Function to open websites
def openWebsite(query):
    query = query.lower()
    speak("Hold on, I will open the website for you.")
    if "pw" in query:
        url = "https://www.pw.live/study/batches/arjuna-jee-2023-426578/batch-overview"
        try:
            webbrowser.open(url)
            return
        except Exception as e:
            speak("Sorry, I was unable to open the website. Could you please check the link and try again?")
            print(e)

    query = query.replace("open website", "")
    # check if query contains specific TLDs
    if not any(ext in query for ext in [".com", ".org", ".edu", ".gov",".in",".live",".io",".ly",".ai",".app",".dev",".ac",".ag",".am",".at",".be",".biz",".bz",".cc",".cn",".com",".de",".dk",".es",".eu",".fm",".fr",".gs",".in",".info",".io",".it",".jobs",".jp",".li",".me",".mobi",".ms",".name",".net",".nl",".nu",".org",".pl",".pro",".pt",".ru",".se",".sg",".sh",".tv",".tw",".us",".co",".uk"]):
        query += ".com"
    if "https" not in query and "http" not in query:
        query = "https://" + query
    try:
        webbrowser.open(query)
    except Exception as e:
        speak("Sorry, I was unable to open the website. Could you please check the spelling and try again?")
        print(e)


# Function to speak the date and time
def speakDateTime():
    now = datetime.datetime.now()
    speak("Current date is " + now.strftime("%B %d, %Y") + " and the time is " + now.strftime("%H:%M:%S"))

# Function to talk like a friend

def friendTalk():
    greetings = ["What's up? How are you doing today?", "How's your day going?", "How are you feeling today?", "What's on your mind?", "What have you been up to?"]
    speak(random.choice(greetings))


# Function to get the results from Dictionary
def getDefinition(query):
    speak("Hold on, I will get the definition for you.")
    query = query.replace("define", "")
    api_key = "c92aa04d-b4d7-4b96-90eb-d8088950fca0" # replace with your own API key
    topic = "" # initialize as empty
    if "in" in query:
        words = query.split(" ")
        topic = words[-1] # last word should be the topic
        query = " ".join(words[:-1]) # all words except last one should be the word to define
    url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={api_key}&topic={topic}"
    response = requests.get(url)
    data = json.loads(response.text)
    if "shortdef" in data[0]:
        definition = data[0]["shortdef"][0]
        if topic:
            speak(f"Definition of {query} in {topic} : {definition}")
        else:
            speak(f"Definition of {query}: {definition}")
    else:
        if topic:
            speak(f"Sorry, I couldn't find a definition for {query} in topic {topic}.")
        else:
            speak(f"Sorry, I couldn't find a definition for {query}.")


# Function to get answers from WolframAlpha
def getWolframAlpha(query):
    app_id = "KP3R8E-EEKW7P86HJ"
    client = wolframalpha.Client(app_id)
    res = client.query(query)
    answer = next(res.results).text
    speak(answer)

def exitCommand(query):
    query = query.lower()
    if "quit" in query or "exit" in query:
        speak("Bye! Have a nice day.")
        speak("Do you want me to turn off or keep running in the background?")
        query = myCommand()
        query = query.lower()
        if "off" in query or "turn off" in query:
            speak("Turning off, have a good day.")
            exit()
        elif "background" in query:
            speak("I will keep running in the background.")
        else:
            speak("Invalid command, I will keep running in the background.")

def play_song(query):
    query = query.replace("play music", "")
    music_name = query
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    print(clip2)

    url = str(clip2)
    video = pafy.new(url)
    bestaudio = video.getbestaudio()
    playurl = bestaudio.url
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(playurl)
    player.set_media(media)
    player.play()

    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            if 'pause' in command:
                player.pause()
                print("Audio Paused")
            elif 'resume' in command:
                player.play()
                print("Audio Resumed")
            elif 'volume up' in command:
                current_volume = player.audio_get_volume()
                player.audio_set_volume(current_volume + 10)
                print("Volume increased")
            elif 'volume down' in command:
                current_volume = player.audio_get_volume()
                player.audio_set_volume(current_volume - 10)
                print("Volume decreased")
            elif 'next song' in command:
                player.stop()
                current_song = playurl
                next_song = "https://www.youtube.com/watch?v=NEXT_SONG_URL"
                media = instance.media_new(next_song)
                player.set_media(media)
                player.play()
                print("Playing next song")
            elif 'exit' in command:
                player.stop()
                print("Exiting program")
                break
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))


# Function to get answers from GPT-3
def get_gpt_response(query):
    openai.api_key = "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"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query,
        max_tokens=1024
    )
    answer = response["choices"][0]["text"]
    speak(answer)

# Main Program
while(True):
    if __name__ == '__main__':

        query = myCommand();
        query = query.lower()
        
        # Logic to execute tasks based on the query
        if 'open youtube' in query:
            youtubeSearch(query)

        elif 'open website'in query:
            openWebsite(query)

        elif 'date and time' in query:
            speakDateTime()

        elif 'talk like a friend' in query:
            friendTalk()

        elif 'define' in query:
            getDefinition(query)

        elif 'wolf' in query:
            getWolframAlpha(query)
        

        elif 'quit' in query:
            exitCommand(query)
        
        elif "play music" in query:
            play_song(query)
            
        else:
            get_gpt_response(query)

