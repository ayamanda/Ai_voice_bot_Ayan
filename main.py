import speech_recognition as sr
import webbrowser
import time
import os
import random
import playsound
import requests
import datetime
import pyttsx3
import json
import wolframalpha
import pafy
import re, requests, subprocess, urllib.parse, urllib.request
from bs4 import BeautifulSoup
import vlc
import openai
class Backend:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.running = True

        # Setting the Voice
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

        # Setting the Volume
        volume = self.engine.getProperty('volume')
        self.engine.setProperty('volume', 10.0)

        # Setting the Speed
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 50)

    # Function to speak text
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

     # Function to listen and response to the user commands
    def my_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = r.listen(source)
            """the energy_threshold parameter is set to 300,
            which indicates that the microphone recognition system should stop listening as soon as
            the audio energy drops below this threshold.
            The pause_threshold parameter is set to 1 second, 
            which means that the system will wait 1 second after the user stops speaking 
            before considering the audio to be complete."""

        try:
            query = r.recognize_google(audio, language='en-in', show_all=True)
            print(f'User: {query}' + '\n')
            best_result = query["alternative"][0]["transcript"]
            print(f"Best Result: {best_result}")
        except sr.UnknownValueError:
            self.speak('Sorry, could not understand. Please try again.')
            query = self.my_command() # recursive call to the function to try again

        return best_result

    # Function to greet the user
    def greet_me(self):
        current_hour = int(datetime.datetime.now().hour)
        if 0 <= current_hour < 6:
            self.speak("Good night! Ayan")
        elif 6 <= current_hour < 12:
            self.speak("Good morning! Ayan")
        elif 12 <= current_hour < 18:
            self.speak("Good afternoon! Ayan")
        else:
            self.speak("Good evening! Ayan")

        greetings = ["How can I help you today?", "What can I do for you?", "How can I assist you?", "What do you need?", "Is there anything I can help you with?"]
        self.speak(random.choice(greetings))

   

    # Function to search YouTube
    def youtubeSearch(self,query):
        self.speak("Hold on, I will search YouTube for you.")
        query = query.replace("search", "")
        query = query.replace("YouTube", "")
        clip2 = self.urlext(query) # the function `urlext` is not defined in the code
        if len(clip2)>0:
            webbrowser.open(clip2)
        else:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


    # Function to open websites
    def openWebsite(self,query):
        query = query.lower()
        self.speak("Hold on, I will open the website for you.")
        if "pw" in query:
            url = "https://www.pw.live/study/batches/arjuna-jee-2023-426578/batch-overview"
            try:
                webbrowser.open(url)
                return
            except Exception as e:
                self.speak("Sorry, I was unable to open the website. Could you please check the link and try again?")
                print(e)

        query = query.replace("open website", "")
        # check if query contains specific TLDs
        if all(
            ext not in query
            for ext in [".com", ".org", ".edu", ".gov", ".in", ".live", ".io", ".ly", ".ai", ".app", ".dev", ".ac", ".ag", ".am", ".at", ".be", ".biz", ".bz", ".cc", ".cn", ".de", ".dk", ".es", ".eu", ".fm", ".fr", ".gs", ".info", ".it", ".jobs", ".jp", ".li", ".me", ".mobi", ".ms", ".name", ".net", ".nl", ".nu", ".pl", ".pro", ".pt", ".ru", ".se", ".sg", ".sh", ".tv", ".tw", ".us", ".co", ".uk"]
        ):
            query += ".com"
        if "https" not in query and "http" not in query:
            query = f"https://{query}"
        try:
            webbrowser.open(query)
        except Exception as e:
            self.speak("Sorry, I was unable to open the website. Could you please check the spelling and try again?")
            print(e)


    # Function to speak the date and time
    def speakDateTime(self):
        now = datetime.datetime.now()
        self.speak("Current date is "+ now.strftime("%B %d, %Y")+ " and the time is "+ now.strftime("%H:%M:%S"))

    # Function to talk like a friend

    def friendTalk(self):
        greetings = ["What's up? How are you doing today?", "How's your day going?", "How are you feeling today?", "What's on your mind?", "What have you been up to?"]
        self(random.choice(greetings))


    # Function to get the results from Dictionary
    def getDefinition(self,query):
        self.speak("Hold on, I will get the definition for you.")
        query = query.replace("define", "")
        api_key = "c92aa04d-b4d7-4b96-90eb-d8088950fca0" # replace with your own API key
        topic = "" # initialize as empty
        if "in" in query:
            words = query.split(" ")
            topic = words[-1] # last word should be the topic
            query= " ".join(words[:-1])
        url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={api_key}&topic={topic}"
        response = requests.get(url)
        data = json.loads(response.text)
        if "shortdef" in data[0]:
            definition = data[0]["shortdef"][0]
            if topic:
                self.speak(f"Definition of {query} in {topic} : {definition}")
            else:
                self.speak(f"Definition of {query}: {definition}")
            print(definition)
        elif topic:
            self.speak(f"Sorry, I couldn't find a definition for {query} in topic {topic}.")
        else:
            self.speak(f"Sorry, I couldn't find a definition for {query}.")


    # Function to get answers from WolframAlpha
    def getWolframAlpha(self,query):
        app_id = "KP3R8E-EEKW7P86HJ"
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        self.speak(answer)

    def exitCommand(self, my_command,query):
        query = query.lower()
        if "quit" in query or "exit" in query:
            self.speak("Bye! Have a nice day.")
            self.speak("Do you want me to turn off or keep running in the background?")
            query = my_command()
            query = query.lower()
            if "off" in query or "turn off" in query:
                self.speak("Turning off, have a good day.")
                exit()
            elif "background" in query:
                self.speak("I will keep running in the background.")
            else:
                self.speak("Invalid command, I will keep running in the background.")

    def play_song(self,query):
        query = query.replace("play music", "")
        music_name = query
        clip2 = self.urlext(music_name)
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
            r = sr.Recognizer()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Say something!")
                r.energy_threshold = 300
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
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
                print("Sorry, I did not understand what you said.")
            except sr.RequestError as e:
                print(f"Error occured during request: {e}")

    # TODO Rename this here and in `youtubeSearch` and `play_song`
    def urlext(self, arg0):
        query_string = urllib.parse.urlencode({"search_query": arg0})
        formatUrl = urllib.request.urlopen(
            f"https://www.youtube.com/results?{query_string}"
        )
        search_results = re.findall("watch\?v=(\S{11})", formatUrl.read().decode())
        clip = requests.get(f"https://www.youtube.com/watch?v={search_results[0]}")
        result = f"https://www.youtube.com/watch?v={search_results[0]}"
        print(result)
        return result

    # Function to get answers from GPT-3
    def get_gpt_response(self,query):
        openai.api_key = "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"
        response = openai.Completion.create(
        engine="text-davinci-002", prompt=query, max_tokens=1024)
        answer = response["choices"][0]["text"]
        self.speak(answer)
   
