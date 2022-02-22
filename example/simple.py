from tkinter import Tk, Frame, BOTH
from tkinter.ttk import Button

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def start(no_use):
            print('111111111', no_use)

    def initUI(self):
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=130, y=40)

        startButton = Button(self, text="Start", command=self.start)
        startButton.place(x=30, y=40)
  
root = Tk()
root.geometry("230x120+300+300")
app = Example(root)
root.mainloop()