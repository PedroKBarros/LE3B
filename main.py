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
    #try:
    file = open(filePath, "r", encoding="utf8")
    loadComments()
    #except(IOError, FileNotFoundError, FileExistsError):
        #ui.showErrorMsgBox(main_consts.EXCEPTION_MSG_TITLE, main_consts.FILE_EXCEPTION_MSG_TEXT)

def loadComments():
    global commentsQueue
    #Atenção: essa função considera que só é possível quebrar 
    # linha em uma mensagem no chat do BigBlueButton, mas não 
    # nos demais atributos do comentário
    lineNum = 0
    totalChars = len(file.read())
    currentNumChars = 0
    file.seek(0) #Colocando o stram position do inicio do arquivo novamente
    line = file.readline()
    while line:
        if (lineNum == 0):
            abbreviatedAuthorName = line
            currentNumChars += len(abbreviatedAuthorName)
            abbreviatedAuthorName = abbreviatedAuthorName.rstrip("\n")
        if (lineNum == 1):
            authorName = line
            currentNumChars += len(authorName)
            authorName = authorName.rstrip("\n")
        if (lineNum == 2):
            time = line
            currentNumChars += len(time)
            time = time.rstrip("\n")
        if (lineNum == 3):
            text = line
            line2 = file.readline()
            while line2 and not isAbbreviatedAuthorNameLine(line2):
                text += line2
                line2 = file.readline()
            
            s = file.tell()
            file.seek(s - 4)

            currentNumChars += len(text)
            text = text.rstrip("\n")
            comment2 = searchCommentByAuthorName(authorName)
            if (comment2 == None):
                colorAbbreviated = main_consts.COLORS_ABBREVIATED_AUTHOR_NAME[randint(0, 10)]
            else:
                #Para manter a mesma cor do(s) comentário(s) anterior(s) do mesmo autor
                colorAbbreviated = comment2["colorAbbreviated"]
            comment = {"abbreviatedAuthorName": abbreviatedAuthorName, 
            "colorAbbreviated": colorAbbreviated, "authorName": authorName, "time": time, 
            "text": text, "state": main_consts.COMMENT_STATES[0]}
            commentsQueue.append(comment)
            ui.addComment(comment)
            lineNum = -1

        ui.updateStatusBar(main_consts.STATUS_BAR_LOAD_COMMENTS_TEXT + str(round((currentNumChars / totalChars), 2) * 100) + "%")
        lineNum += 1
        line = file.readline()
    
    ui.updateStatusBar(str(ui.totalComments) + main_consts.STATUS_BAR_LOADED_COMMENTS_TEXT)

def isAbbreviatedAuthorNameLine(linha):
    return len(linha.rstrip("\n")) == 2

def searchCommentByAuthorName(authorName):
    for i in range(commentsQueue.__len__()):
        comment = commentsQueue.__getitem__(i)
        if (comment["authorName"] == authorName):
            return comment
    return None

if __name__ == "__main__":
    ui.executaUI()