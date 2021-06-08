import UI.ui_constants as ui_consts
import UI.ui as ui
import threading
from collections import namedtuple, deque
import main_constants as main_consts
from random import randint

filePath = ""
file = None
commentsQueue = deque()

def setFilePath(path):
    global filePath
    filePath = path

def commentsManagement():
    load_thread = threading.Thread(target=loadCommentsManagement)
    load_thread.start()

def loadCommentsManagement():
    global filePath
    global file
    print(filePath)
    try:
        file = open(filePath, "r")
        loadComments()
    except(IOError, FileNotFoundError, FileExistsError):
        ui.showErrorMsgBox(main_consts.EXCEPTION_MSG_TITLE, main_consts.FILE_EXCEPTION_MSG_TEXT)

def loadComments():
    global commentsQueue
    #Atenção: essa função considera que não é possível quebrar 
    # linha em uma mensagem no chat do BigBlueButton
    numLinha = 0
    for linha in file:
        if (numLinha == 0):
            abbreviatedAuthorName = linha
            abbreviatedAuthorName = abbreviatedAuthorName.rstrip("\n")
        if (numLinha == 1):
            authorName = linha
            authorName = authorName.rstrip("\n")
        if (numLinha == 2):
            time = linha
            time = time.rstrip("\n")
        if (numLinha == 3):
            text = linha
            text = text.rstrip("\n")
            colorAbbreviated = main_consts.COLORS_ABBREVIATED_AUTHOR_NAME[randint(0, 10)]
            comment = {"abbreviatedAuthorName": abbreviatedAuthorName, 
            "colorAbbreviated": colorAbbreviated, "authorName": authorName, "time": time, 
            "text": text, "state": main_consts.COMMENT_STATES[0]}
            commentsQueue.append(comment)
            ui.addComment(comment)
            numLinha = -1

        numLinha += 1    

if __name__ == "__main__":
    ui.executaUI()