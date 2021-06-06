from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk
import UI.ui_constants as ui_consts

class Application:
    def __init__(self, master = None):
        self.labelFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE2)
        self.entryFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE1)
        self.buttonFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE2)

        self.defaultFgColor = ui_consts.DEFAULT_FG_COLOR
        self.defaultBgColor = ui_consts.DEFAULT_BG_COLOR

        self.fileContainer1 = Frame(master)
        self.fileContainer1["bg"] = self.defaultBgColor
        self.fileContainer1.pack()
        self.fileContainer1["padx"] = ui_consts.FILE_CONTAINER1_PADX
        self.fileContainer1["pady"] = ui_consts.FILE_CONTAINER1_PADY

        self.fileContainer2 = Frame(master)
        self.fileContainer2["bg"] = self.defaultBgColor
        self.fileContainer2.pack()
        self.fileContainer2["padx"] = ui_consts.FILE_CONTAINER2_PADX
        self.fileContainer2["pady"] = ui_consts.FILE_CONTAINER2_PADY

        self.controlsContainer3 = Frame(master)
        self.controlsContainer3["bg"] = ui_consts.CONTROLS_BG_COLOR
        self.controlsContainer3.pack()
        self.controlsContainer3["padx"] = 100
        self.controlsContainer3["pady"] = 2

        self.label1 = Label(self.fileContainer1)
        self.label1["bg"] = self.defaultBgColor
        self.label1["text"] = ui_consts.LABEL1_TEXT
        self.label1["fg"] = self.defaultFgColor
        self.label1["font"] = self.labelFont
        self.label1.pack()

        self.entry1 = Entry(self.fileContainer1)
        self.entry1["width"] = 30
        self.entry1["font"] = self.entryFont
        self.entry1["state"] = "readonly" #O estado pode ser disable, normal ou readonly. 
                                          #Para escrita por código ou pelo usuário, é necessário ser "normal"
        self.entry1.pack()

        self.load_image1 = Image.open(ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE)
        self.load_image1 = self.load_image1.resize((50, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
        self.render_image1 = ImageTk.PhotoImage(self.load_image1)

        self.button1 = Button(self.fileContainer2, image=self.render_image1)
        self.button1.image = self.render_image1
        self.button1["bd"] = 0 #Para definir a borda, tornando-a mínima
        self.button1["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
        self.button1.bind("<Enter>", lambda event, button=self.button1, imgName=ui_consts.IMAGE_PATH_BTN_OPEN_ENTER, size=(50, 50): self.handleEventMouseEnter(event, button, imgName, size))
        self.button1.bind("<Leave>", lambda event, button=self.button1, imgName=ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE, size=(50, 50): self.handleEventMouseLeave(event, button, imgName, size))
        self.button1.bind("<Button-1>", self.handleEventMouseLeftClick)
        self.button1.pack()

        self.load_image2 = Image.open(ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE)
        self.load_image2 = self.load_image2.resize((20, 20), Image.ANTIALIAS) #Alterando as dimensões da imagem
        self.render_image2 = ImageTk.PhotoImage(self.load_image2)

        self.button2 = Button(self.controlsContainer3, image=self.render_image2)
        self.button2.image = self.render_image2
        self.button2["bd"] = 0 #Para definir a borda, tornando-a mínima
        self.button2["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
        self.button2.bind("<Enter>", lambda event, button=self.button2, imgName=ui_consts.IMAGE_PATH_BTN_PLAY_ENTER, size=(20, 20): self.handleEventMouseEnter(event, button, imgName, size))
        self.button2.bind("<Leave>", lambda event, button=self.button2, imgName=ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE, size=(20, 20): self.handleEventMouseLeave(event, button, imgName, size))
        self.button2.pack(side=RIGHT)

        #self.list_box1 = Listbox(self.commentContainer3, selectmode=SINGLE)
        #self.list_box1.pack()
        

    def handleEventMouseEnter(self, event, button, imgName, size):
        load_image2 = Image.open(imgName)
        load_image2 = load_image2.resize(size, Image.ANTIALIAS) #Alterando as dimensões da imagem
        render_image2 = ImageTk.PhotoImage(load_image2)
        button.configure(image=render_image2)
        button.image = render_image2
        print("MOUSE ENTER!")

    def handleEventMouseLeave(self, event, button, imgName, size):
        load_image2 = Image.open(imgName)
        load_image2 = load_image2.resize(size, Image.ANTIALIAS) #Alterando as dimensões da imagem
        render_image2 = ImageTk.PhotoImage(load_image2)
        button.configure(image=render_image2)
        button.image = render_image2
        print("MOUSE LEAVE!")   

    def handleEventMouseLeftClick(self, event):
        filename = askopenfilename(filetypes=(('text files', 'txt'),))
        self.printEntry(self.entry1, filename)        

    def printEntry(self, wgEntry, string):
        originalState = wgEntry["state"]
        wgEntry["state"] = "normal"
        wgEntry.delete(0, END)
        wgEntry.insert(0, string)
        wgEntry["state"] = originalState

def executaUI():
    root = Tk()
    root.resizable(False, False)
    root.title(ui_consts.ROOT_TITLE + " " + ui_consts.VERSION)
    Application(root)
    root.mainloop()
    