import kivy
import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from main import Backend


class MyApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical")
        label = Label(text="Welcome to my App")
        start_button = Button(text="Start", on_press=self.start)
        root.add_widget(label)
        root.add_widget(start_button)
        return root


    def start(self, instance):
        backend = Backend()
        
        # Front-end code
        while backend.running:
            if __name__ == '__main__':

                query = backend.my_command();
                query = query.lower()
                
                # Logic to execute tasks based on the query
                if 'open youtube' in query:
                    backend.youtubeSearch(query)

                elif 'open website'in query:
                    backend.openWebsite(query)

                elif 'date and time' in query:
                    backend.speakDateTime()

                elif 'talk like a friend' in query:
                    backend.friendTalk()

                elif 'define' in query:
                    backend.getDefinition(query)

                elif 'wolf' in query:
                    backend.getWolframAlpha(query)
                

                elif 'quit' in query:
                    backend.exitCommand()
                
                elif "play music" in query:
                    backend.play_song(query)
                    
                else:
                    backend.get_gpt_response(query)
if __name__ == "__main__":
    MyApp().run()

 