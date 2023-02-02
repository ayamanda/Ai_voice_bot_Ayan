import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
from main import Backend

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Welcome to my App")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)

        # Adding the text box
        label = QLabel("Enter a command:", self)
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter a command here...")

        # Adding the Output Box
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Output...")
        

        # Adding the start button
        start_button = QPushButton("Start", self)
        start_button.clicked.connect(self.start)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(start_button)
        
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.text_input)
        vbox.addWidget(self.output_box)
        vbox.addLayout(hbox)
        
        self.setCentralWidget(QLabel(self))
        self.centralWidget().setLayout(vbox)
        self.show()
        
    def start(self):
        if self.text_input.toPlainText().strip() == "":
            query = self.backend.my_command()
        else:
            query = self.text_input.toPlainText().strip()
            
        query = query.lower()
        old_stdout = sys.stdout
        sys.stdout = self
        
        if 'open youtube' in query:
            self.backend.youtubeSearch(query)

        elif 'open website'in query:
            self.backend.openWebsite(query)

        elif 'date and time' in query:
            self.backend.speakDateTime()

        elif 'talk like a friend' in query:
            self.backend.friendTalk()

        elif 'define' in query:
            self.backend.getDefinition(query)

        elif 'calculate' in query:
            self.backend.getWolframAlpha(query)

        elif 'quit' in query:
            self.backend.exitCommand()
        
        elif "play music" in query:
            self.backend.play_song(query)
            
        else:
            self.backend.get_gpt_response(query)
        sys.stdout = old_stdout

    def closeEvent(self, event):
        # stop any background threads
        self.stopThreads()

        # release any resources
        self.releaseResources()

        # accept the close event to close the window
        event.accept()

    def stopThreads(self):
        for thread in self.threads:
            thread.stop()
        for thread in self.threads:
            thread.wait()
    
    def releaseResources(self):
        # close any open files
        for  player in self.backend.play_song:
            player.close()


    # Define the write method to capture the print statements
    def write(self, message):
        cursor = self.output_box.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(message)
        self.output_box.setTextCursor(cursor)
        self.output_box.ensureCursorVisible()

    # Assign the sys.stdout back to the original value
    def __del__(self):
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
