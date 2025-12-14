from logic.quiz import Quiz
from logic.timer import QuizTimer
from gui import sukurti_gui
import tkinter as tk

def on_timeout():

    pass

def main():
    root = tk.Tk()
    quiz = Quiz()
    timer = QuizTimer(root, on_timeout)
    sukurti_gui(root, quiz, timer)
    root.mainloop()

if __name__ == "__main__":
    main()