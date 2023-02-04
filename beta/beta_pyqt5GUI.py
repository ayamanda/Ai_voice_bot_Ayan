import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout
from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtCore import Qt, QSize
from beta_main import Backend

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
        label.setStyleSheet("font-family: Arial; font-size: 14px;")
        self.text_input = QTextEdit(self)
        self.text_input.setStyleSheet("background-color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.text_input.setPlaceholderText("Enter a command here...")
        self.text_input.installEventFilter(self)

        # Adding the Output Box
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        self.output_box.setStyleSheet("background-color: #F2F2F2; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.output_box.setPlaceholderText("Output...")

        # Adding the start button
        mic_button = QPushButton(self)
        mic_button.setIcon(QIcon('D:\python\ai voice bot\mic.png'))
        mic_button.setIconSize(QSize(20, 20))
        mic_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-size: 14px;")
        mic_button.clicked.connect(self.start_voice_input)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(mic_button)
        
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.text_input)
        vbox.addWidget(self.output_box)
        vbox.addLayout(hbox)
        
        self.setCentralWidget(QLabel(self))
        self.centralWidget().setLayout(vbox)
        self.show()
        
    def process_query(self, query):
        try:
            old_stdout = sys.stdout
            sys.stdout = self
            self.backend.process(query)
            sys.stdout = old_stdout

        except Exception as e:
            print("Error occurred while processing command: ", e)

    def start_text_input(self):
        query = self.text_input.toPlainText().strip()
        self.backend.process_query(query)
        self.text_input.clear()

    def start_voice_input(self):
        query = self.backend.my_command()
        self.backend.process_query(query)

    def closeEvent(self, event):
        event.accept()


    
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

    def eventFilter(self, obj, event):
        # sourcery skip: merge-comparisons, merge-nested-ifs
        if event.type() == QtCore.QEvent.KeyPress and obj == self.text_input:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.start_text_input()
                return True
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
