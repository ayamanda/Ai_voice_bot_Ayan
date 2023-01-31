from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import threading
from main import backend


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.text_input = TextInput(text='Enter your query here', size_hint=(1, 0.2))
        self.label = Label(text='Output:')
        layout.add_widget(self.text_input)
        layout.add_widget(self.label)
        start_button = Button(text='Start', size_hint=(1, 0.2), on_press=self.start)
        layout.add_widget(start_button)
        return layout

    def start(self, instance):
        query = self.text_input.text
        thread = threading.Thread(target=self.process_query, args=(query,))
        thread.start()

    def process_query(self, query):
        while(True):
            query = self.backend.myCommand();
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

if __name__ == '__main__':
    MyApp().run()
