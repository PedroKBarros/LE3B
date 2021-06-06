from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk
import UI.ui_constants as ui_consts

def buildUI(master=None):
    labelFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE2)
    entryFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE1)
    buttonFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE2)

    defaultFgColor = ui_consts.DEFAULT_FG_COLOR
    defaultBgColor = ui_consts.DEFAULT_BG_COLOR

    fileContainer1 = Frame(master)
    fileContainer1["bg"] = defaultBgColor
    fileContainer1.pack()
    fileContainer1["padx"] = ui_consts.FILE_CONTAINER1_PADX
    fileContainer1["pady"] = ui_consts.FILE_CONTAINER1_PADY

    fileContainer2 = Frame(master)
    fileContainer2["bg"] = defaultBgColor
    fileContainer2.pack()
    fileContainer2["padx"] = ui_consts.FILE_CONTAINER2_PADX
    fileContainer2["pady"] = ui_consts.FILE_CONTAINER2_PADY

    controlsContainer3 = Frame(master)
    controlsContainer3["bg"] = ui_consts.CONTROLS_BG_COLOR
    controlsContainer3.pack()
    controlsContainer3["padx"] = 100
    controlsContainer3["pady"] = 2

    label1 = Label(fileContainer1)
    label1["bg"] = defaultBgColor
    label1["text"] = ui_consts.LABEL1_TEXT
    label1["fg"] = defaultFgColor
    label1["font"] = labelFont
    label1.pack()

    entry1 = Entry(fileContainer1)
    entry1["width"] = 30
    entry1["font"] = entryFont
    entry1["state"] = "readonly" #O estado pode ser disable, normal ou readonly. 
                                        #Para escrita por código ou pelo usuário, é necessário ser "normal"
    entry1.pack()

    load_image1 = Image.open(ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE)
    load_image1 = load_image1.resize((50, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image1 = ImageTk.PhotoImage(load_image1)

    button1 = Button(fileContainer2, image=render_image1)
    button1.image = render_image1
    button1["bd"] = 0 #Para definir a borda, tornando-a mínima
    button1["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
    button1.bind("<Enter>", lambda event, button=button1, imgName=ui_consts.IMAGE_PATH_BTN_OPEN_ENTER, size=(50, 50): handleEventMouseEnter(event, button, imgName, size))
    button1.bind("<Leave>", lambda event, button=button1, imgName=ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE, size=(50, 50): handleEventMouseLeave(event, button, imgName, size))
    button1.bind("<Button-1>", lambda event, widget=entry1: handleEventMouseLeftClick(event, widget))
    button1.pack()

    load_image2 = Image.open(ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE)
    load_image2 = load_image2.resize((20, 20), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image2 = ImageTk.PhotoImage(load_image2)

    button2 = Button(controlsContainer3, image=render_image2)
    button2.image = render_image2
    button2["bd"] = 0 #Para definir a borda, tornando-a mínima
    button2["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
    button2.bind("<Enter>", lambda event, button=button2, imgName=ui_consts.IMAGE_PATH_BTN_PLAY_ENTER, size=(20, 20): handleEventMouseEnter(event, button, imgName, size))
    button2.bind("<Leave>", lambda event, button=button2, imgName=ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE, size=(20, 20): handleEventMouseLeave(event, button, imgName, size))
    button2.pack(side=RIGHT)

    #self.list_box1 = Listbox(self.commentContainer3, selectmode=SINGLE)
    #self.list_box1.pack()
    

def handleEventMouseEnter(event, button, imgName, size):
    load_image2 = Image.open(imgName)
    load_image2 = load_image2.resize(size, Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image2 = ImageTk.PhotoImage(load_image2)
    button.configure(image=render_image2)
    button.image = render_image2
    print("MOUSE ENTER!")

def handleEventMouseLeave(event, button, imgName, size):
    load_image2 = Image.open(imgName)
    load_image2 = load_image2.resize(size, Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image2 = ImageTk.PhotoImage(load_image2)
    button.configure(image=render_image2)
    button.image = render_image2
    print("MOUSE LEAVE!")   

def handleEventMouseLeftClick(event, widget):
    filename = askopenfilename(filetypes=(('text files', 'txt'),))
    printEntry(widget, filename)        

def printEntry(wgEntry, string):
    originalState = wgEntry["state"]
    wgEntry["state"] = "normal"
    wgEntry.delete(0, END)
    wgEntry.insert(0, string)
    wgEntry["state"] = originalState

def executaUI():
    root = Tk()
    root.resizable(False, False)
    root.title(ui_consts.ROOT_TITLE + " " + ui_consts.VERSION)
    buildUI(root)
    root.mainloop()
    