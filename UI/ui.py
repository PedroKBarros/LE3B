from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import UI.ui_constants as ui_consts
import main as main
import os.path
from os import path
from collections import deque
from random import randint

root = None
currentCommentsUIRow = 0
commentsFrame = None
lblStatusBar = None
etrCurrentTime = None
lblTotalTime = None
lblCurrentTimeBar = None
lastWidgetFocusIn = None
btnPlayPause = None
UICommentsQueue = deque()
cnvComments = None
scrbarCanvasComment = None
CkbScrollbarAutoMoveVar = None

def buildUI(root):
    load_image = Image.open("UI/icon.png")
    #load_image = load_image.resize((90, 90), Image.ANTIALIAS)
    render_image = ImageTk.PhotoImage(load_image)
    root.iconphoto(True, render_image)

    root.geometry('338x531')
    root.resizable(False, False)
    root.title(main.getSoftwareName() + " " + main.getSoftwareVersion())
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
                                        #Para escrita por c??digo ou pelo usu??rio, ?? necess??rio ser "normal"
    entry1.place(x=15, y=20)

    load_image1 = Image.open(ui_consts.IMAGE_PATH_BTN_OPEN_LEAVE)
    load_image1 = load_image1.resize((50, 50), Image.ANTIALIAS) #Alterando as dimens??es da imagem
    render_image1 = ImageTk.PhotoImage(load_image1)

    button1 = Button(root, image=render_image1)
    button1.image = render_image1
    button1["bd"] = 0 #Para definir a borda, tornando-a m??nima
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
    load_image2 = load_image2.resize((318, 50), Image.ANTIALIAS) #Alterando as dimens??es da imagem
    render_image2 = ImageTk.PhotoImage(load_image2)

    label2 = Label(root, image=render_image2)
    label2.image = render_image2
    label2.place(x=0, y=110)

    load_image3 = Image.open(ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE)
    load_image3 = load_image3.resize((22, 22), Image.ANTIALIAS) #Alterando as dimens??es da imagem
    render_image3 = ImageTk.PhotoImage(load_image3)

    global btnPlayPause
    btnPlayPause = Button(root, image=render_image3)
    btnPlayPause.image = render_image3
    btnPlayPause["bd"] = 0 #Para definir a borda, tornando-a m??nima
    btnPlayPause["highlightthickness"] = 0 #Para definir a espessura de destaque, retirando de fato a borda
    #Mouse Leave e Enter:
    imgData1 = (ui_consts.IMAGE_PATH_BTN_PLAY_ENTER, (22, 22), main.isTimeStatePlay, False)
    imgData2 = (ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE, (22, 22), main.isTimeStatePlay, False)
    imgData3 = (ui_consts.IMAGE_PATH_BTN_PAUSE_ENTER, (22, 22), main.isTimeStatePlay, True)
    imgData4 = (ui_consts.IMAGE_PATH_BTN_PAUSE_LEAVE, (22, 22), main.isTimeStatePlay, True)
    #Button-1:
    imgData6 = (ui_consts.IMAGE_PATH_BTN_PAUSE_ENTER, (22, 22), main.isTimeStatePlay, False)
    imgData7 = (ui_consts.IMAGE_PATH_BTN_PLAY_ENTER, (22, 22), main.isTimeStatePlay, True)
    btnPlayPause.bind("<Enter>", lambda event, wgControl=btnPlayPause, borderSize=0, borderColor="white", 
    imgData1=imgData1, imgData2=imgData3: handleEventMouseEnter(event, wgControl, borderSize, 
    borderColor, imgData1, imgData2))
    btnPlayPause.bind("<Leave>", lambda event, wgControl=btnPlayPause, borderSize=0, borderColor="white", 
    imgData1=imgData2, imgData2=imgData4: handleEventMouseLeave(event, wgControl, borderSize, 
    borderColor, imgData1, imgData2))
    btnPlayPause.bind("<Button-1>", lambda event, wgControl=btnPlayPause, borderSize=0, 
    borderColor="white", imgData1=imgData6, imgData2=imgData7, 
    function = handleEventPlayPauseButtonMouseLeftClick, execConditionFunc=main.isEndTime, execConditionValue=False: 
    handleEventMouseLeftClick(event, wgControl, borderSize, borderColor, 
    imgData1, imgData2, function, execConditionFunc, execConditionValue))
    btnPlayPause.place(x=7, y=117)

    load_image4 = Image.open(ui_consts.IMAGE_PATH_TIME_BAR)
    load_image4 = load_image4.resize(ui_consts.IMAGE_PATH_TIME_BAR_SIZE_MIN, Image.ANTIALIAS) #Alterando as dimens??es da imagem
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
    var = StringVar()
    var.trace("w", lambda name, index,mode, var=var: handleEtrCurrentTimeChange(var))
    #Com a vari??vel var e o m??todo trace, ?? poss??vel associar uma fun????o de callback toda vez
    # que o valor da etrCurrentTime for modificado.
    etrCurrentTime = Entry(root, textvariable=var, name=ui_consts.ETR_CURRENT_TIME_NAME) #Colocado o nome para que possamos saber se o evento FocusIn foi disparado por esse widget
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
    imgData1 = (ui_consts.IMAGE_PATH_BTN_PLAY_LEAVE, (22, 22), main.isTimeStatePlay, True)
    etrCurrentTime.bind("<FocusIn>", lambda event, wgControl=btnPlayPause, borderSize=0, 
    borderColor="white", imgData1=imgData1: 
    handleEventFocusIn(event, wgControl, borderSize, borderColor, imgData1, None, 
    function=configPauseTime)) 
    #Obs1.: Utilizei configPauseTime() ao inv??s de handleEventButtonPlayPauseLeftClick(), 
    # pois essa ??ltima passa o foco para o bot??o play pause, retirando o foco da etrCurrentTime. 
    # Al??m disso, ela chama a main.timeManagement(), o que n??o ?? necess??riod
    #Obs2.: ?? necess??rio o evento FocusIn, apesar de termos o trace com a StringVar, pois a
    # handleEventFocusIn seta a vari??vel lastWidgetFocusIn com o widget 
    # que pertence ao evento.
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
    load_image5 = load_image5.resize((1, 4), Image.ANTIALIAS) #Alterando as dimens??es da imagem
    render_image5 = ImageTk.PhotoImage(load_image5)

    global lblCurrentTimeBar
    lblCurrentTimeBar = Label(root, image=render_image5)
    lblCurrentTimeBar.image = render_image5
    lblCurrentTimeBar["bd"] = 0
    lblCurrentTimeBar["highlightthickness"] = 0
    lblCurrentTimeBar.place(x=10, y=145)

    #UI respons??vel pela apresenta????o dos coment??rios: 
    global cnvComments   
    cnvComments = Canvas(root)
    cnvComments["width"] = 318
    cnvComments["height"] = 320
    cnvComments["highlightthickness"] = 0
    cnvComments["bg"] = ui_consts.DEFAULT_BG_COLOR
    cnvComments.place(x=2, y=163)

    global commentsFrame
    global scrbarCanvasComment
    commentsFrame = Frame(cnvComments, background = "#FFFFFF")
    scrbarCanvasComment = Scrollbar(root, orient = "vertical", command = cnvComments.yview)
    cnvComments.configure(yscrollcommand = scrbarCanvasComment.set)
    scrbarCanvasComment.pack(side="right", fill="y")
    cnvComments.create_window((4,4), window=commentsFrame, anchor="nw")
    commentsFrame.bind("<Configure>", lambda event, canvas=cnvComments: onFrameConfigure(canvas))

    global CkbScrollbarAutoMoveVar
    CkbScrollbarAutoMoveVar = IntVar()
    CkbScrollbarAutoMove = Checkbutton(root, variable=CkbScrollbarAutoMoveVar, command=handleCkbScrollbarAutoMove)
    CkbScrollbarAutoMove["text"] = "Mover automaticamente para Coment??rio"
    CkbScrollbarAutoMove["font"] = entryFont
    CkbScrollbarAutoMove["bg"] = ui_consts.DEFAULT_BG_COLOR
    CkbScrollbarAutoMove.place(x=0, y=480)

    global lblStatusBar
    lblStatusBar = Label(root)
    lblStatusBar["bg"] = ui_consts.CONTROLS_BG_COLOR
    lblStatusBar["width"] = 45
    lblStatusBar["fg"] = ui_consts.SECOND_FG_COLOR
    lblStatusBar["anchor"] = W
    lblStatusBar.place(x=0, y=510)
    
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def handleEventMouseEnter(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, 
function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), fun????o condi????o, valor condi????o)
    handleEvent(event, wgControl, borderSize, borderColor, imgData1, imgData2, function, execConditionFunc, execConditionValue)
    print("MOUSE ENTER!")

def handleEventFocusIn(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, 
function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), fun????o condi????o, valor condi????o)
    global lastWidgetFocusIn
    lastWidgetFocusIn = str(event.widget)
    handleEvent(event, wgControl, borderSize, borderColor, imgData1, imgData2, function, execConditionFunc, execConditionValue)
    print("FOCUS IN!")

def handleEventFocusOut(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, 
function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), fun????o condi????o, valor condi????o)
    handleEvent(event, wgControl, borderSize, borderColor, imgData1, imgData2, function, execConditionFunc, execConditionValue)

def handleEvent(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, 
function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), fun????o condi????o, valor condi????o)
    if (execConditionFunc != None and execConditionValue != None):
        if (execConditionFunc() != execConditionValue):
            return

    changeImg = False
    if (imgData1 != None):
        if (imgData1[2] != None):
            if (imgData1[2]() == imgData1[3]):
                load_image = Image.open(imgData1[0])
                load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimens??es da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
                changeImg = True
        else:
            load_image = Image.open(imgData1[0])
            load_image = load_image.resize(imgData1[1], Image.ANTIALIAS) #Alterando as dimens??es da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
            changeImg = True
    if (imgData2 != None and not changeImg):
        if (imgData2[2] != None):
            if (imgData2[2]() == imgData2[3]):
                load_image = Image.open(imgData2[0])
                load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimens??es da imagem
                render_image = ImageTk.PhotoImage(load_image)
                wgControl.configure(image=render_image)
                wgControl.image = render_image
        else:
            load_image = Image.open(imgData2[0])
            load_image = load_image.resize(imgData2[1], Image.ANTIALIAS) #Alterando as dimens??es da imagem
            render_image = ImageTk.PhotoImage(load_image)
            wgControl.configure(image=render_image)
            wgControl.image = render_image
    wgControl["highlightthickness"] = borderSize
    wgControl["highlightbackground"] = borderColor

    if (function != None):
        function()
    

def handleEventMouseLeave(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, 
function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), fun????o condi????o, valor condi????o)
    handleEvent(event, wgControl, borderSize, borderColor, imgData1, imgData2, function, execConditionFunc, execConditionValue)
    print("MOUSE LEAVE!")

def handleEventMouseLeftClick(event, wgControl, borderSize = 1, borderColor = "black", imgData1 = None, imgData2 = None, 
function = None, execConditionFunc = None, execConditionValue = None):
    #Estrutura de uma imgData: (caminho da imagem, (width, height), fun????o condi????o, valor condi????o)
    handleEvent(event, wgControl, borderSize, borderColor, imgData1, imgData2, function, execConditionFunc, execConditionValue)
    print("CLIQUE")

def loadCommentsByTxtFile(entryFilePath):
    filepath = askopenfilename(filetypes=(('text files', 'txt'),))
    printEntry(entryFilePath, filepath)

    #Apesar da GUI de sele????o de arquivos do Windows impedir a inser????o de caminhos 
    #inv??lidos, n??o d?? pra garantir que tal valida????o acontecer?? em outros SOs, 
    #por isso se faz a valida????o
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

def showInfoMsgBox(title, message, showMsgFuncCondition = None, showMsgValueCondition = None, 
callbackFunction=None, callbackCondition=None):
    if (isRunMsgBox(showMsgFuncCondition, showMsgValueCondition)):
        msgReturn = messagebox.showinfo(title=title, message=message)
        runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def isRunMsgBox(showMsgFuncCondition = None, showMsgValueCondition = None):
    return ((showMsgFuncCondition == None or showMsgValueCondition == None) or 
    (showMsgFuncCondition() == showMsgValueCondition))

def showWarningMsgBox(title, message, showMsgFuncCondition = None, showMsgValueCondition = None, 
callbackFunction=None, callbackCondition=None):
    if (isRunMsgBox(showMsgFuncCondition, showMsgValueCondition)):
        msgReturn = messagebox.showwarning(title=title, message=message)
        runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def showErrorMsgBox(title, message, showMsgFuncCondition = None, showMsgValueCondition = None, 
callbackFunction=None, callbackCondition=None):
    if (isRunMsgBox(showMsgFuncCondition, showMsgValueCondition)):
        msgReturn = messagebox.showerror(title=title, message=message)
        runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def showAskOkCancelMsgBox(title, message, showMsgFuncCondition = None, showMsgValueCondition = None, 
callbackFunction=None, callbackCondition=None):
    if (isRunMsgBox(showMsgFuncCondition, showMsgValueCondition)):
        msgReturn = messagebox.askokcancel(title=title, message=message)
        runMsgBoxCallback(msgReturn, callbackFunction, callbackCondition)

def showAskYesNoMsgBox(title, message, showMsgFuncCondition = None, showMsgValueCondition = None, 
callbackFunction=None, callbackCondition=None):
    if (isRunMsgBox(showMsgFuncCondition, showMsgValueCondition)):
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
    global UICommentsQueue

    colorAbbreviated = defineBackgroundColorAbbreviatedNameComment(comment) #Define a cor de fundo do widget com o nome do autor do coment??rio abreviado
    
    message1 = Message(commentsFrame)
    message1["text"] = comment["abbreviatedAuthorName"]
    message1.grid(row=currentCommentsUIRow, column=0)

    message2 = Message(commentsFrame)
    message2["text"] = comment["authorName"]
    message2.grid(row=currentCommentsUIRow, column=1)

    message3 = Message(commentsFrame)
    message3["text"] = comment["time"]
    message3.grid(row=currentCommentsUIRow, column=2)

    currentCommentsUIRow += 1
    
    message4 = Message(commentsFrame)
    message4["text"] = comment["text"]
    message4.grid(row=currentCommentsUIRow, column=1)

    currentCommentsUIRow += 1

    main.setCommentState(comment, 1)
    UIComment = {"wgAbbreviatedAuthorName": message1, 
    "colorAbbreviated": colorAbbreviated, 
    "wgAuthorName": message2, "wgTime": message3,
     "wgText": message4}
    UICommentsQueue.append(UIComment)
    formatCommentForLoaded(len(UICommentsQueue) - 1)

def defineBackgroundColorAbbreviatedNameComment(comment):
    comment2 = searchUICommentByAuthorName(comment["authorName"])
    if(comment2 == None):
        colorAbbreviated = ui_consts.COLORS_ABBREVIATED_AUTHOR_NAME[randint(0, 10)]
    else:
        colorAbbreviated = comment2["colorAbbreviated"]

    return colorAbbreviated

def searchUICommentByAuthorName(authorName):
    global UICommentsQueue
    for i in range(len(UICommentsQueue)):
        UIComment = UICommentsQueue[i]
        if (UIComment["wgAuthorName"]["text"] == authorName):
            return UIComment
    return None

def formatCommentForRead(index):
    global UICommentsQueue
    UIComment = UICommentsQueue[index]
    UIComment["wgAbbreviatedAuthorName"]["bg"] = UIComment["colorAbbreviated"]
    UIComment["wgAuthorName"]["fg"] = ui_consts.THRID_FG_COLOR
    UIComment["wgTime"]["fg"] = ui_consts.TIME_COMMENT_FG_COLOR_READ_STATE
    UIComment["wgText"]["fg"] = ui_consts.THRID_FG_COLOR

def formatCommentForLoaded(index):
    global UICommentsQueue
    UIComment = UICommentsQueue[index]
    UIComment["wgAbbreviatedAuthorName"].configure(width = 16, font=('Verdana', 8, 'normal'), 
    bg=ui_consts.COMMENT_FG_COLOR_LOADED_STATE, fg="#FFFFFF", bd=0)
    UIComment["wgAuthorName"].configure(font=('Verdana', 10, 'bold'), bg="#FFFFFF", 
    fg=ui_consts.COMMENT_FG_COLOR_LOADED_STATE, bd=0, width=200, padx=10)
    UIComment["wgTime"].configure(font=('Verdana', 8, 'normal'), bg="#FFFFFF", 
    fg=ui_consts.COMMENT_FG_COLOR_LOADED_STATE, bd=0, width=100)
    UIComment["wgText"].configure(font=('Verdana', 10, 'normal'), bg="#FFFFFF",
    fg=ui_consts.COMMENT_FG_COLOR_LOADED_STATE, bd=0, width=200, padx=10)    

def updateStatusBar(text, backGroundColor = ui_consts.CONTROLS_BG_COLOR, fontColor = ui_consts.SECOND_FG_COLOR):
    global lblStatusBar
    global root
    lblStatusBar["text"] = text
    lblStatusBar["bg"] = backGroundColor
    lblStatusBar["fg"] = fontColor
    root.update() #Para atualizar qualquer mudan??a visual na barra de status    

def resetVariables():
    resetPositionScrbarCommentCanvas() 
    resetCommentsFrame()
    resetCurrentCommentsUIRow() #Essa fun????o tem que ser chamada apenas depois da resetCommentsFrame()
    resetUICommentsQueue() #Essa fun????o tem que ser chamada apenas depois da resetPositionScrbarCommentCanvas()
    resetEtrCurrentTime()

def resetCurrentCommentsUIRow():
    global currentCommentsUIRow

    currentCommentsUIRow = 0

def resetUICommentsQueue():
    global UICommentsQueue

    UICommentsQueue.clear()

def resetCommentsFrame():
    #Deletando widgets dentro do frame:
    global currentCommentsUIRow
    global commentsFrame
    for widgets in commentsFrame.winfo_children():
        widgets.destroy()
    currentCommentsUIRow = 0

def resetEtrCurrentTime():
    global etrCurrentTime

    printEntry(etrCurrentTime, "00:00:00")
    etrCurrentTime.focus_set() #Para disparar o evento 

def resetPositionScrbarCommentCanvas():
    positionsScrbarByUIComment(0)


def configPauseTime():
    main.setTimeStateToStop()

def configPlayTime():
    main.setTimeStateToPlay()

def handleEventPlayPauseButtonMouseLeftClick():
    global root
    global btnPlayPause
    focusOnPlayPauseButton(btnPlayPause) #Para retirar o foco do etrCurrentTime, caso o usu??rio tenha clicado nele
    if(not validateCurrentTime()):
        return #Valida o valor que est?? em etrCurrentTime, caso o usu??rio tenha alterado
    if(main.isTimeStatePlay()):
        configPauseTime()
    else:
        configPlayTime()
    
    main.timeManagement()

def validateCurrentTime():
    global etrCurrentTime
    if (not isEtrCurrentTimeLastWidgetFocusIn()):
        etrCurrentTime["fg"] = "white"
        updateStatusBar("")
        return True
    
    isvalidNumberSeparators = validateTotalNumberSeparatorsCurrentTime()
    if(not isvalidNumberSeparators):
        etrCurrentTime["fg"] = "red"
        updateStatusBar(ui_consts.ETR_CURRENT_TIME_WARNING_TEXT_MSG, "red")
        #showWarningMsgBox(ui_consts.ETR_CURRENT_TIME_WARNING_TITLE_MSG, ui_consts.ETR_CURRENT_TIME_WARNING_TEXT_MSG)
        return False #N??o d?? para colocar os dois valores booleanos em um if s??, pois ter um n??mero de separadores inv??lido gera bug na valida????o seguinte
    isvalidNumbers = validateNumbersCurrentTime()
    if (not isvalidNumbers):
        etrCurrentTime["fg"] = "red"
        updateStatusBar(ui_consts.ETR_CURRENT_TIME_WARNING_TEXT_MSG, "red")
        return False        
        #showWarningMsgBox(ui_consts.ETR_CURRENT_TIME_WARNING_TITLE_MSG, ui_consts.ETR_CURRENT_TIME_WARNING_TEXT_MSG)  

    etrCurrentTime["fg"] = "white"
    updateStatusBar("")

    main.setCurrentTime(main.convertStrTimeToSeconds(etrCurrentTime.get()))
    main.checkCommentsToChangeStateByCurrentTimeUserInput()
    return True  

def validateTotalNumberSeparatorsCurrentTime():
    global etrCurrentTime
    return etrCurrentTime.get().count(ui_consts.ETR_CURRENT_TIME_SEPARATOR) == 2

def validateNumbersCurrentTime():
    global etrCurrentTime
    h, m, s = etrCurrentTime.get().split(':')
    if (not h.isnumeric() or not m.isnumeric() or not s.isnumeric()):
        #A fun????o isnumeric() retorna False se a string for vazia
        return False

    totalTime = main.timeData["totalTime"]
    strCurrentTime = h + ":" + m + ":" + s
    currentTime = main.convertStrTimeToSeconds(strCurrentTime)

    return  currentTime <= totalTime

def focusOnPlayPauseButton(buttonPlayPause):
    buttonPlayPause.focus_set()

def updateUICurrentTime(text):
    global etrCurrentTime
    global root
    printEntry(etrCurrentTime, text, aligment="center")
    root.update()

def updateUICurrentTimeBar(width):
    global lblCurrentTimeBar
    global root

    if (width == 0):
        lblCurrentTimeBar.place_forget() #Para torna n??o vis??vel o widget
        return

    lblCurrentTimeBar.place(x=10, y=145)
    load_image = Image.open(ui_consts.IMAGE_PATH_CURRENT_TIME_BAR)
    load_image = load_image.resize((width, lblCurrentTimeBar.image.height()), Image.ANTIALIAS)
    render_image = ImageTk.PhotoImage(load_image)

    #lblCurrentTimeBar.configure(image="") #Deletando imagem anterior
    lblCurrentTimeBar.configure(image=render_image)
    lblCurrentTimeBar.image = render_image
    lblCurrentTimeBar["bd"] = 0
    lblCurrentTimeBar["highlightthickness"] = 0
    root.update()

def updateUITotalTime(text):
    global lblTotalTime
    global root
    lblTotalTime["text"] = text
    root.update()

def handleOptionMenuSelectChange(value):
    main.updateTimeVelocityByUI(float(value.rstrip("x")))

def handleEtrCurrentTimeChange(var):
    global etrCurrentTime
    if (not isEtrCurrentTimeLastWidgetFocusIn()):
        return

    content = var.get()
    if (len(content) == 0):
        return
    if (not content.isascii()): #Verifica se todos os caracteres s??o ascii
        var.set("")
    lastCharInput = content[len(content) - 1]
    if (not isCharAsciiNumber(lastCharInput)):
        var.set(content[0:len(content) - 1])
    if(len(content) > 8):
        var.set(content[0:len(content) - 1])

    if (len(content) == 2 or len(content) == 5):
        etrCurrentTime.insert(END, ":")

def getUIComment(index):
    global UICommentsQueue
    if (index < 0 or index >= len(UICommentsQueue)):
        return None
    
    return UICommentsQueue[index]

def positionsScrbarByUIComment(UIcommentIndex):
    global scrbarCanvasComment
    global cnvComments

    if (not main.isScrollBarAutoMoveEnabled()):
        return

    UIComment = getUIComment(UIcommentIndex)
    if (UIComment == None):
        return
    xWgAbbName = UIComment["wgAbbreviatedAuthorName"].winfo_x()
    yWgAbbName = UIComment["wgAbbreviatedAuthorName"].winfo_y()
    fraction = scrbarCanvasComment.fraction(xWgAbbName, yWgAbbName)
    print("FRACTION = " + str(fraction))
    cnvComments.yview_moveto(fraction)

def isCharAsciiNumber(char):
    return ord(char) >= 48 and ord(char) <= 57
    
def isEtrCurrentTimeLastWidgetFocusIn():
    global lastWidgetFocusIn
    return lastWidgetFocusIn == "." + ui_consts.ETR_CURRENT_TIME_NAME

def handleCkbScrollbarAutoMove():
    global CkbScrollbarAutoMoveVar
    print(CkbScrollbarAutoMoveVar.get())
    main.updateConfigScrollBarAutoMove(CkbScrollbarAutoMoveVar.get())

def defineRootProtocols():
    global root

    root.wm_protocol("WM_DELETE_WINDOW", lambda title=ui_consts.MSG_BOX_CLOSE_PROGRAM_TITLE, 
    message=ui_consts.MSG_BOX_CLOSE_PROGRAM_TEXT, showMsgFuncCondition=None, 
    showMsgValueCondition=None, callbackFunction = handleEventcloseRoot, 
    callbackCondition = True: showAskYesNoMsgBox(title, message, showMsgFuncCondition, 
    showMsgValueCondition, callbackFunction, callbackCondition))

def handleEventcloseRoot():
    global root

    updateStatusBar(ui_consts.STATUS_BAR_CLOSE_PROGRAM)
    if (main.hasAliveThread()):    
        main.isCloseProgram = True
        root.after(1000, root.destroy) #1000ms ?? o tempo m??ximo que a thread que conta segundo ficar?? sem conferir a condi????o de seu loop
    else:
        root.destroy()

def executaUI():
    global root

    root = Tk()
    defineRootProtocols()
    buildUI(root)
    root.mainloop()

    