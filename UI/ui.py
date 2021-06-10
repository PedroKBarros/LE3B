from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import UI.ui_constants as ui_consts
import main as main
import os.path
from os import path

root = None
currentCommentsUIRow = 0
totalComments = 0
commentsFrame = None
lblStatusBar = None
etrCurrentTime = None
lblTotalTime = None
lblCurrentTimeBar = None

def buildUI(root):
    root.geometry('338x500')
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
    label1.place(x=15, y=0)

    entry1 = Entry(root)
    entry1["width"] = 36
    entry1["font"] = entryFont
    entry1["state"] = "readonly" #O estado pode ser disable, normal ou readonly. 
                                        #Para escrita por código ou pelo usuário, é necessário ser "normal"
    entry1.place(x=15, y=20)

    load_image1 = Image.open(ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE)
    load_image1 = load_image1.resize((50, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image1 = ImageTk.PhotoImage(load_image1)

    button1 = Button(root, image=render_image1)
    button1.image = render_image1
    button1["bd"] = 0 #Para definir a borda, tornando-a mínima
    button1["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
    #Mouse Leave e Enter:
    imgData1 = (ui_consts.IMAGE_PATH_BTN_OPEN_ENTER, (50, 50), None, None)
    imgData2 = (ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE, (50, 50), None, None)
    button1.bind("<Enter>", lambda event, wgControl=button1, borderSize=0, 
    borderColor="white", imgData1=imgData1: 
    handleEventMouseEnter(event, wgControl, borderSize, borderColor, imgData1))
    button1.bind("<Leave>", lambda event, wgControl=button1, borderSize=0, 
    borderColor="white", imgData1=imgData2: 
    handleEventMouseLeave(event, wgControl, borderSize, borderColor, imgData1))
    button1.bind("<Button-1>", lambda event, wgControl=button1, borderSize=0, 
    borderColor="white", function=loadCommentsByTxtFile: 
    handleEventMouseLeftClick(event, wgControl, borderSize, borderColor, None, None, function(entry1)))
    button1.place(x=135, y=50)

    load_image2 = Image.open(ui_consts.IMAGE_PATH_CONTROLS_BAR)
    load_image2 = load_image2.resize((318, 50), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image2 = ImageTk.PhotoImage(load_image2)

    label2 = Label(root, image=render_image2)
    label2.image = render_image2
    label2.place(x=0, y=110)

    load_image3 = Image.open(ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE)
    load_image3 = load_image3.resize((22, 22), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image3 = ImageTk.PhotoImage(load_image3)

    button2 = Button(root, image=render_image3)
    button2.image = render_image3
    button2["bd"] = 0 #Para definir a borda, tornando-a mínima
    button2["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
    #Mouse Leave e Enter:
    imgData1 = (ui_consts.IMAGE_PATH_BTN_PLAY_ENTER, (22, 22), main.isTimeStatePlay, False)
    imgData2 = (ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE, (22, 22), main.isTimeStatePlay, False)
    imgData3 = (ui_consts.IMAGE_PATH_BTN_PAUSE_ENTER, (22, 22), main.isTimeStatePlay, True)
    imgData4 = (ui_consts.IMAGE_PATH_BTN_PAUSE_LEAVE, (22, 22), main.isTimeStatePlay, True)
    #Button-1:
    imgData6 = (ui_consts.IMAGE_PATH_BTN_PAUSE_ENTER, (22, 22), main.isTimeStatePlay, False)
    imgData7 = (ui_consts.IMAGE_PATH_BTN_PLAY_ENTER, (22, 22), main.isTimeStatePlay, True)
    button2.bind("<Enter>", lambda event, wgControl=button2, borderSize=0, borderColor="white", 
    imgData1=imgData1, imgData2=imgData3: handleEventMouseEnter(event, wgControl, borderSize, 
    borderColor, imgData1, imgData2))
    button2.bind("<Leave>", lambda event, wgControl=button2, borderSize=0, borderColor="white", 
    imgData1=imgData2, imgData2=imgData4: handleEventMouseLeave(event, wgControl, borderSize, 
    borderColor, imgData1, imgData2))
    button2.bind("<Button-1>", lambda event, wgControl=button2, borderSize=0, 
    borderColor="white", imgData1=imgData6, imgData2=imgData7, 
    function = handleEventPlayPauseButtonMouseLeftClick, execConditionFunc=main.isEndTime, execConditionValue=False: 
    handleEventMouseLeftClick(event, wgControl, borderSize, borderColor, 
    imgData1, imgData2, function, execConditionFunc, execConditionValue))
    button2.place(x=7, y=117)

    load_image4 = Image.open(ui_consts.IMAGE_PATH_TIME_BAR)
    load_image4 = load_image4.resize(ui_consts.IMAGE_PATH_TIME_BAR_SIZE_MIN, Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image4 = ImageTk.PhotoImage(load_image4)

    label3 = Label(root, image=render_image4)
    label3.image = render_image4
    label3["bd"] = 0
    label3["highlightthickness"] = 0
    #Mouse Leave e Enter:
    imgData1 = (ui_consts.IMAGE_PATH_TIME_BAR, ui_consts.IMAGE_PATH_TIME_BAR_SIZE_MAX, None, None)
    imgData2 = (ui_consts.IMAGE_PATH_TIME_BAR, ui_consts.IMAGE_PATH_TIME_BAR_SIZE_MIN, None, None)
    label3.bind("<Enter>", lambda event, wgControl=label3, borderSize=0,
    borderColor="white", imgData1=imgData1: 
    handleEventMouseEnter(event, wgControl, borderSize, borderColor, imgData1))
    label3.bind("<Leave>", lambda event, wgControl=label3, borderSize=0, 
    borderColor="white", imgData1=imgData2: 
    handleEventMouseLeave(event, wgControl, borderSize, borderColor, imgData1))
    label3.place(x=10, y=145)

    global lblTotalTime
    lblTotalTime = Label(root)
    lblTotalTime["bg"] = ui_consts.SECOND_BG_COLOR
    lblTotalTime["text"] = ui_consts.LABEL4_INITIAL_TEXT
    lblTotalTime["fg"] = ui_consts.SECOND_FG_COLOR
    lblTotalTime["font"] = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE1)
    lblTotalTime.place(x=140, y=118)

    global etrCurrentTime
    etrCurrentTime = Entry(root)
    etrCurrentTime["width"] = 8
    etrCurrentTime["bg"] = ui_consts.SECOND_BG_COLOR
    etrCurrentTime["fg"] = ui_consts.SECOND_FG_COLOR
    etrCurrentTime["font"] = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE1)
    etrCurrentTime["state"] = "normal"
    etrCurrentTime.bind("<Enter>", lambda event, wgControl=etrCurrentTime, borderSize=0.5, 
    borderColor=ui_consts.SECOND_BC_HIGHLIGHT_COLOR: 
    handleEventMouseEnter(event, wgControl, borderSize, borderColor))
    etrCurrentTime.bind("<Leave>", lambda event, wgControl=etrCurrentTime, borderSize=0: 
    handleEventMouseLeave(event, wgControl, borderSize))
    etrCurrentTime.place(x=72, y=119)
    printEntry(etrCurrentTime, "00:00:00", CENTER)

    defaultOptionMenuValue = StringVar()
    defaultOptionMenuValue.set(ui_consts.DEFAULT_OPTION_MENU1_VALUE)
    optionMenu1 = OptionMenu(root, defaultOptionMenuValue, *ui_consts.OPTION_MENU1_VALUES, command=handleOptionMenuSelectChange)
    optionMenu1["font"] = (ui_consts.FONT_NAME, ui_consts.FONT_SIZE1)
    optionMenu1["bg"] = ui_consts.CONTROLS_BG_COLOR
    optionMenu1["fg"] = ui_consts.SECOND_FG_COLOR
    optionMenu1["bd"] = 0
    optionMenu1["direction"] = "above"
    optionMenu1["highlightthickness"] = 0
    optionMenu1["relief"] = GROOVE
    optionMenu1["width"] = 4
    optionMenu1["height"] = 1
    optionMenu1.place(x=247, y=117)

    load_image5 = Image.open(ui_consts.IMAGE_PATH_CURRENT_TIME_BAR)
    load_image5 = load_image5.resize((1, 4), Image.ANTIALIAS) #Alterando as dimensões da imagem
    render_image5 = ImageTk.PhotoImage(load_image5)

    global lblCurrentTimeBar
    lblCurrentTimeBar = Label(root, image=render_image5)
    lblCurrentTimeBar.image = render_image5
    lblCurrentTimeBar["bd"] = 0
    lblCurrentTimeBar["highlightthickness"] = 0
    lblCurrentTimeBar.place(x=10, y=145)

    #UI responsável pela apresentação dos comentários:    
    canvas1 = Canvas(root)
    canvas1["width"] = 318
    canvas1["height"] = 320
    canvas1["highlightthickness"] = 0
    canvas1["bg"] = ui_consts.DEFAULT_BG_COLOR
    canvas1.place(x=2, y=163)

    global commentsFrame
    commentsFrame = Frame(canvas1, background = "#FFFFFF")
    scrollbar1 = Scrollbar(root, orient = "vertical", command = canvas1.yview)
    canvas1.configure(yscrollcommand = scrollbar1.set)
    scrollbar1.pack(side="right", fill="y")
    canvas1.create_window((4,4), window=commentsFrame, anchor="nw")
    commentsFrame.bind("<Configure>", lambda event, canvas=canvas1: onFrameConfigure(canvas))

    global lblStatusBar
    lblStatusBar = Label(root)
    lblStatusBar["bg"] = ui_consts.CONTROLS_BG_COLOR
    lblStatusBar["width"] = 45
    lblStatusBar["fg"] = ui_consts.SECOND_FG_COLOR
    lblStatusBar["anchor"] = W
    lblStatusBar.place(x=0, y=480)
    
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def handleEventMouseEnter(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), função condição, valor condição)
    if (execConditionFunc != None or execConditionValue != None):
        if (execConditionFunc() != execConditionValue):
            return

    changeImg = False
    if (imgData1 != None):
        if (imgData1[2] != None):
            if (imgData1[2]() == imgData1[3]):
                load_image = Image.open(imgData1[0])
                load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
                changeImg = True
        else:
            load_image = Image.open(imgData1[0])
            load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
            changeImg = True
    if (imgData2 != None and not changeImg):
        if (imgData2[2] != None):
            if (imgData2[2]() == imgData2[3]):
                load_image = Image.open(imgData2[0])
                load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
        else:
            load_image = Image.open(imgData2[0])
            load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
    wgControl["highlightthickness"] = borderSize
    wgControl["highlightbackground"] = borderColor

    if (function != None):
        function()

    print("MOUSE ENTER!")

def handleEventMouseLeave(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), função condição, valor condição)
    if (execConditionFunc != None or execConditionValue != None):
        if (execConditionFunc() != execConditionValue):
            return

    changeImg = False
    if (imgData1 != None):
        if (imgData1[2] != None):
            if (imgData1[2]() == imgData1[3]):
                load_image = Image.open(imgData1[0])
                load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
                changeImg = True
        else:
            load_image = Image.open(imgData1[0])
            load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
            changeImg = True
    if (imgData2 != None and not changeImg):
        if (imgData2[2] != None):
            if (imgData2[2]() == imgData2[3]):
                load_image = Image.open(imgData2[0])
                load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
        else:
            load_image = Image.open(imgData2[0])
            load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
    wgControl["highlightthickness"] = borderSize
    wgControl["highlightbackground"] = borderColor

    if (function != None):
        function()
    print("MOUSE LEAVE!")

def handleEventMouseLeftClick(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), função condição, valor condição)
    if (execConditionFunc != None or execConditionValue != None):
        if (execConditionFunc() != execConditionValue):
            return

    changeImg = False
    if (imgData1 != None):
        if (imgData1[2] != None):
            if (imgData1[2]() == imgData1[3]):
                load_image = Image.open(imgData1[0])
                load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
                changeImg = True
        else:
            load_image = Image.open(imgData1[0])
            load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
            changeImg = True
    if (imgData2 != None and not changeImg):
        if (imgData2[2] != None):
            if (imgData2[2]() == imgData2[3]):
                load_image = Image.open(imgData2[0])
                load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
        else:
            load_image = Image.open(imgData2[0])
            load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimensões da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
    wgControl["highlightthickness"] = borderSize
    wgControl["highlightbackground"] = borderColor

    if (function != None):
        function()

def loadCommentsByTxtFile(entryFilePath):
    filepath = askopenfilename(filetypes=(('text files', 'txt'),))
    printEntry(entryFilePath, filepath)

    #Apesar da GUI de seleção de arquivos do Windows impedir a inserção de caminhos 
    #inválidos, não dá pra garantir que tal validação acontecerá em outros SOs, 
    #por isso se faz a validação
    if (not isValidFilePath(filepath)):
        return
    
    main.setFilePath(filepath)
    main.commentsManagement()

def isValidFilePath(filepath):
    return os.path.exists(filepath)  

def printEntry(wgEntry, string, aligment = "left"):
    originalState = wgEntry["state"]
    wgEntry["state"] = "normal"
    wgEntry.delete(0, END)
    wgEntry.insert(0, string)
    wgEntry["justify"] = aligment
    wgEntry["state"] = originalState

def showInfoMsgBox(title, message, callbackFunction=None, callbackCondition=None):
    msgReturn = messagebox.showinfo(title=title, message=message)
    runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def showWarningMsgBox(title, message, callbackFunction=None, callbackCondition=None):
    msgReturn = messagebox.showwarning(title=title, message=message)
    runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def showErrorMsgBox(title, message, callbackFunction=None, callbackCondition=None):
    msgReturn = messagebox.showerror(title=title, message=message)
    runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def showAskOkCancelMsgBox(title, message, callbackFunction=None, callbackCondition=None):
    msgReturn = messagebox.askokcancel(title=title, message=message)
    runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def showAskYesNoMsgBox(title, message, callbackFunction=None, callbackCondition=None):
    msgReturn = messagebox.askyesno(title=title, message=message)
    runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)
    
def runMsgBoxCallback(msgBoxReturn, callbackFunction, callbackCondition):
    if (callbackCondition == None or callbackFunction == None):
        return

    if (msgBoxReturn == callbackCondition):
        callbackFunction()

def addComment(comment):
    global currentCommentsUIRow
    global commentsFrame
    global totalComments

    message1 = Message(commentsFrame, width = 16, font=('Verdana', 8, 'normal'), bg=comment["colorAbbreviated"], fg="#FFFFFF", bd=0)
    message1["text"] = comment["abbreviatedAuthorName"]
    message1.grid(row=currentCommentsUIRow, column=0)

    message2 = Message(commentsFrame, font=('Verdana', 10, 'bold'), bg="#FFFFFF", fg="#000000", bd=0, width=200)
    message2["text"] = comment["authorName"]
    message2.grid(row=currentCommentsUIRow, column=1)
    message2["padx"] = 10

    message3 = Message(commentsFrame, font=('Verdana', 8, 'normal'), bg="#FFFFFF", fg="#808080", bd=0, width=100)
    message3["text"] = comment["time"]
    message3.grid(row=currentCommentsUIRow, column=2)

    currentCommentsUIRow += 1
    
    message4 = Message(commentsFrame, font=('Verdana', 10, 'normal'), bg="#FFFFFF", fg="#000000", bd=0, width=200)
    message4["text"] = comment["text"]
    message4.grid(row=currentCommentsUIRow, column=1)
    message4["padx"] = 10

    currentCommentsUIRow += 1
    totalComments += 1


def updateStatusBar(text):
    global lblStatusBar
    global root
    lblStatusBar["text"] = text
    root.update() #Para atualizar qualquer mudança visual na barra de status
    
def deleteAllComments():
    global currentCommentsUIRow
    global totalComments
    global commentsFrame
    for widgets in commentsFrame.winfo_children():
        widgets.destroy()
    currentCommentsUIRow = 0
    totalComments = 0

def configPauseTime():
    main.setTimeStateToStop()

def configPlayTime():
    main.setTimeStateToPlay()

def handleEventPlayPauseButtonMouseLeftClick():
    if(main.isTimeStatePlay()):
        configPauseTime()
    else:
        configPlayTime()
    
    main.timeManagement()

def updateUICurrentTime(text):
    global etrCurrentTime
    global root
    printEntry(etrCurrentTime, text, aligment="center")
    root.update()

def updateUICurrentTimeBar(width):
    global lblCurrentTimeBar

    if (width == 0):
        lblCurrentTimeBar.place_forget() #Para torna não visível o widget
        return

    lblCurrentTimeBar.place(x=10, y=145)
    load_image = Image.open(ui_consts.IMAGE_PATH_CURRENT_TIME_BAR)
    load_image = load_image.resize((width, lblCurrentTimeBar.image.height()), Image.ANTIALIAS)
    render_image = ImageTk.PhotoImage(load_image)

    lblCurrentTimeBar = Label(root, image=render_image)
    lblCurrentTimeBar.image = render_image
    lblCurrentTimeBar["bd"] = 0
    lblCurrentTimeBar["highlightthickness"] = 0

def updateUITotalTime(text):
    global lblTotalTime
    global root
    lblTotalTime["text"] = text
    root.update()

def handleOptionMenuSelectChange(value):
    main.updateTimeVelocityByUI(float(value.rstrip("x")))

def executaUI():
    global root
    root = Tk()
    buildUI(root)
    root.mainloop()
    