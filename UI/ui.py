from tkinter import *
from PIL import Image, ImageTk

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
        self.fileContainer2["padx"] = 120
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

        self.load_image1 = Image.open("UI/open_file_btn.png")
        self.load_image1 = self.load_image1.resize((50, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
        self.render_image1 = ImageTk.PhotoImage(self.load_image1)

        self.button2 = Button(self.fileContainer2, image=self.render_image1)
        self.button2.image = self.render_image1
        self.button2["bd"] = 0 #Para definir a borda, tornando-a mínima
        self.button2["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
        self.button2.bind("<Enter>", lambda event, button=self.button2, imgName="open_file_btn_enter.png": self.handleEventMouseEnter(event, button, imgName))
        self.button2.bind("<Leave>", lambda event, button=self.button2, imgName="open_file_btn.png": self.handleEventMouseLeave(event, button, imgName))
        self.button2.pack()
        

    def handleEventMouseEnter(self, event, button, imgName):
        load_image2 = Image.open("UI/" + imgName)
        load_image2 = load_image2.resize((50, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
        render_image2 = ImageTk.PhotoImage(load_image2)
        button.configure(image=render_image2)
        button.image = render_image2
        print("MOUSE ENTER!")

    def handleEventMouseLeave(self, event, button, imgName):
        load_image2 = Image.open("UI/" + imgName)
        load_image2 = load_image2.resize((50, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
        render_image2 = ImageTk.PhotoImage(load_image2)
        button.configure(image=render_image2)
        button.image = render_image2
        print("MOUSE LEAVE!")        
    

def executaUI():
    root = Tk()
    Application(root)
    root.mainloop()