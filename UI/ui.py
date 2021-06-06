from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import UI.ui_constants as ui_consts

def buildUI(root):
    root.geometry('300x300')
    root.resizable(False, False)
    root.title(ui_consts.ROOT_TITLE + " " + ui_consts.VERSION)
    root["bg"] = ui_consts.DEFAULT_BG_COLOR

    labelFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE2)
    entryFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE1)
    buttonFont = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE2)

    defaultFgColor = ui_consts.DEFAULT_FG_COLOR
    defaultBgColor = ui_consts.DEFAULT_BG_COLOR

    #fileContainer1 = Frame(master)
    #fileContainer1["bg"] = defaultBgColor
    #fileContainer1.pack()
    #fileContainer1["padx"] = ui_consts.FILE_CONTAINER1_PADX
    #fileContainer1["pady"] = ui_consts.FILE_CONTAINER1_PADY

    #fileContainer2 = Frame(master)
    #fileContainer2["bg"] = defaultBgColor
    #fileContainer2.pack()
    #fileContainer2["padx"] = ui_consts.FILE_CONTAINER2_PADX
    #fileContainer2["pady"] = ui_consts.FILE_CONTAINER2_PADY

    #controlsContainer3 = Frame(master)
    #controlsContainer3["bg"] = ui_consts.CONTROLS_BG_COLOR
    #controlsContainer3.pack()
    #controlsContainer3["padx"] = 170
    #controlsContainer3["pady"] = 2
    #controlsContainer3.grid(row=3, column=0)

    label1 = Label(root)
    label1["bg"] = defaultBgColor
    label1["text"] = ui_consts.LABEL1_TEXT
    label1["fg"] = defaultFgColor
    label1["font"] = labelFont
    label1.place(x=17, y=0)

    entry1 = Entry(root)
    entry1["width"] = 33
    entry1["font"] = entryFont
    entry1["state"] = "readonly" #O estado pode ser disable, normal ou readonly. 
                                        #Para escrita por código ou pelo usuário, é necessário ser "normal"
    entry1.place(x=17, y=20)

    load_image1 = Image.open(ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE)
    load_image1 = load_image1.resize((50, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image1 = ImageTk.PhotoImage(load_image1)

    button1 = Button(root, image=render_image1)
    button1.image = render_image1
    button1["bd"] = 0 #Para definir a borda, tornando-a mínima
    button1["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
    button1.bind("<Enter>", lambda event, wgControl=button1, imgName=ui_consts.IMAGE_PATH_BTN_OPEN_ENTER, size=(50, 50), borderSize=0: handleEventMouseEnter(event, wgControl, imgName, size, borderSize))
    button1.bind("<Leave>", lambda event, wgControl=button1, imgName=ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE, size=(50, 50), borderSize=0: handleEventMouseLeave(event, wgControl, imgName, size, borderSize))
    button1.bind("<Button-1>", lambda event, widget=entry1: handleEventMouseLeftClick(event, widget))
    button1.place(x=133, y=50)

    load_image2 = Image.open(ui_consts.IMAGE_PATH_CONTROLS_BAR)
    load_image2 = load_image2.resize((296, 30), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image2 = ImageTk.PhotoImage(load_image2)

    label2 = Label(root, image=render_image2)
    label2.image = render_image2
    label2.place(x=0, y=110)

    load_image3 = Image.open(ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE)
    load_image3 = load_image3.resize((20, 20), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image3 = ImageTk.PhotoImage(load_image3)

    button2 = Button(root, image=render_image3)
    button2.image = render_image3
    button2["bd"] = 0 #Para definir a borda, tornando-a mínima
    button2["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
    button2.bind("<Enter>", lambda event, wgControl=button2, imgName=ui_consts.IMAGE_PATH_BTN_PLAY_ENTER, size=(20, 20), borderSize=0: handleEventMouseEnter(event, wgControl, imgName, size, borderSize))
    button2.bind("<Leave>", lambda event, wgControl=button2, imgName=ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE, size=(20, 20), borderSize=0: handleEventMouseLeave(event, wgControl, imgName, size, borderSize))
    button2.place(x=6, y=117)

    load_image4 = Image.open(ui_consts.IMAGE_PATH_TIME_BAR)
    load_image4 = load_image4.resize((80, 6), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image4 = ImageTk.PhotoImage(load_image4)

    label3 = Label(root, image=render_image4)
    label3.image = render_image4
    label3["bd"] = 0
    label3["highlightthickness"] = 0
    label3.bind("<Enter>", lambda event, wgControl=label3, imgName=ui_consts.IMAGE_PATH_TIME_BAR, size=(80, 8), borderSize=0: handleEventMouseEnter(event, wgControl, imgName, size, borderSize))
    label3.bind("<Leave>", lambda event, wgControl=label3, imgName=ui_consts.IMAGE_PATH_TIME_BAR, size=(80, 6), borderSize=0: handleEventMouseLeave(event, wgControl, imgName, size, borderSize))
    label3.place(x=30, y=124)

    label4 = Label(root)
    label4["bg"] = ui_consts.SECOND_BG_COLOR
    label4["text"] = ui_consts.LABEL4_INITIAL_TEXT
    label4["fg"] = ui_consts.SECOND_FG_COLOR
    label4["font"] = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE3)
    label4.place(x=173, y=118)

    entry2 = Entry(root)
    entry2["width"] = 8
    entry2["bg"] = ui_consts.SECOND_BG_COLOR
    entry2["fg"] = ui_consts.SECOND_FG_COLOR
    entry2["font"] = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE3)
    entry2["state"] = "normal"
    entry2.bind("<Enter>", lambda event, wgControl=entry2, imgName="", size=(0, 0), borderSize=0.5, borderColor=ui_consts.SECOND_BC_HIGHLIGHT_COLOR: handleEventMouseEnter(event, wgControl, imgName, size, borderSize, borderColor))
    entry2.bind("<Leave>", lambda event, wgControl=entry2, imgName="", size=(0, 0), borderSize=0: handleEventMouseLeave(event, wgControl, imgName, size, borderSize))
    entry2.place(x=115, y=119)
    printEntry(entry2, "00:00:00", CENTER)

    defaultOptionMenuValue = StringVar()
    defaultOptionMenuValue.set(ui_consts.DEFAULT_OPTION_MENU1_VALUE)
    optionMenu1 = OptionMenu(root, defaultOptionMenuValue, *ui_consts.OPTION_MENU1_VALUES)
    optionMenu1["font"] = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE1)
    optionMenu1["bg"] = ui_consts.CONTROLS_BG_COLOR
    optionMenu1["fg"] = ui_consts.SECOND_FG_COLOR
    optionMenu1["direction"] = "above"
    optionMenu1["highlightthickness"] = 0
    optionMenu1["relief"] = GROOVE
    optionMenu1["width"] = 1
    optionMenu1["height"] = 1
    optionMenu1.place(x=242, y=113)

    #self.list_box1 = Listbox(self.commentContainer3, selectmode=SINGLE)
    #self.list_box1.pack()
    

def handleEventMouseEnter(event, wgControl, imgName, size, borderSize, borderColor = "black"):
    if (imgName != ""):
        load_image2 = Image.open(imgName)
        load_image2 = load_image2.resize(size, Image.ANTIALIAS) #Alterando as dimensões da imagem
        render_image2 = ImageTk.PhotoImage(load_image2)
        wgControl.configure(image=render_image2)
        wgControl.image = render_image2
    wgControl["highlightthickness"] = borderSize
    wgControl["highlightbackground"] = borderColor
    print("MOUSE ENTER!")

def handleEventMouseLeave(event, wgControl, imgName, size, borderSize, borderColor = "black"):
    if (imgName != ""):
        load_image2 = Image.open(imgName)
        load_image2 = load_image2.resize(size, Image.ANTIALIAS) #Alterando as dimensões da imagem
        render_image2 = ImageTk.PhotoImage(load_image2)
        wgControl.configure(image=render_image2)
        wgControl.image = render_image2
    wgControl["highlightthickness"] = borderSize
    wgControl["highlightbackground"] = borderColor
    print("MOUSE LEAVE!")   

def handleEventMouseLeftClick(event, widget):
    filename = askopenfilename(filetypes=(('text files', 'txt'),))
    printEntry(widget, filename)        

def printEntry(wgEntry, string, aligment = "left"):
    originalState = wgEntry["state"]
    wgEntry["state"] = "normal"
    wgEntry.delete(0, END)
    wgEntry.insert(0, string)
    wgEntry["justify"] = aligment
    wgEntry["state"] = originalState

def executaUI():
    root = Tk()
    buildUI(root)
    root.mainloop()
    