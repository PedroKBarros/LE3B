from tkinter import *

class Application:
    def __init__(self, master = None):
        self.labelFont = ("Verdana", "11")
        self.entryFont = ("Verdana", "10")
        self.buttonFont = ("Verdana", "11")

        self.defaultFgColor = "#4E5A66"
        self.defaultBgColor = "#FFFFFF"

        self.fileContainer1 = Frame(master)
        self.fileContainer1["bg"] = self.defaultBgColor
        self.fileContainer1.pack()
        self.fileContainer1["padx"] = 40
        self.fileContainer1["pady"] = 10

        self.fileContainer2 = Frame(master)
        self.fileContainer2["bg"] = self.defaultBgColor
        self.fileContainer2.pack()
        self.fileContainer2["padx"] = 90
        self.fileContainer2["pady"] = 10

        self.label1 = Label(self.fileContainer1)
        self.label1["bg"] = self.defaultBgColor
        self.label1["text"] = "Enter the full path of the txt file:"
        self.label1["fg"] = self.defaultFgColor
        self.label1["font"] = self.labelFont
        self.label1.pack()

        self.entry1 = Entry(self.fileContainer1)
        self.entry1["width"] = 30
        self.entry1["font"] = self.entryFont
        self.entry1.pack()

        self.button1 = Button(self.fileContainer2)
        self.button1["text"] = "Browse"
        self.button1["width"] = 15
        self.button1["font"] = self.buttonFont
        self.button1.pack()

        



def executaUI():
    root = Tk()
    Application(root)
    root.mainloop()