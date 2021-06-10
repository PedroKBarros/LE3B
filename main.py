import UI.ui_constants as ui_consts
import UI.ui as ui
import threading
from collections import deque
import main_constants as main_consts
from random import randint
import time

filePath = ""
file = None
commentsQueue = deque()
timeData = {"initialTime": 0.0, "currentTime": 0.0, "totalTime": 0.0, "velocity": 1, "state": main_consts.STOP_TIME_STATE}

def timeManagement():
    global timeData

    updateTotalTime()
    if (not isTimeStatePlay() or isEndTime()):
        return
    time_thread = threading.Thread(target=countTime)
    time_thread.start()

def updateTotalTime():
    #Atenção: essa função é chamada ao final da função 
    # que carrega os comentários na fila e na ui
    global timeData
    global commentsQueue
    strTotalTime = commentsQueue[len(commentsQueue) - 1]["time"]
    timeData["totalTime"] = convertStrTimeToSeconds(strTotalTime)
    ui.updateUITotalTime(" / " + strTotalTime)

def updateCurrentTimeBar():
    global timeData

    maxWidthCurrentTimeBar = ui_consts.IMAGE_PATH_TIME_BAR_SIZE_MAX[0]
    pastTimeRazon = timeData["currentTime"] / timeData["totalTime"]
    currentTimeBarWidth = maxWidthCurrentTimeBar * pastTimeRazon
    ui.updateUICurrentTimeBar(int(currentTimeBarWidth))

def convertStrTimeToSeconds(strTime):
    h, m, s = strTime.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def isTimeStatePlay():
    global timeData
    return timeData["state"]

def setTimeStateToPlay():
    global timeData
    timeData["state"] = main_consts.PLAY_TIME_STATE

def setTimeStateToStop():
    global timeData
    timeData["state"] = main_consts.STOP_TIME_STATE

def setTimeState():
    global timeData
    timeData["state"] = not timeData["state"]

def countTime():
    global timeData
    while(timeData["state"] and not isEndTime()):
        time.sleep(1) #espera 1 segundo
        timeData["currentTime"] += timeData["velocity"]
        timeDiff = timeData["currentTime"] - timeData["initialTime"]
        ui.updateUICurrentTime(convertsecondsToUIFormat(timeDiff))
        updateCurrentTimeBar()
    
    if (isEndTime()):
        ui.handleEventPlayPauseButtonMouseLeftClick()
        ui.updateUICurrentTimeBar(ui_consts.IMAGE_PATH_TIME_BAR_SIZE_MAX[0])

def isEndTime():
    global timeData
    return timeData["currentTime"] == timeData["totalTime"]

def convertsecondsToUIFormat(sec):
    conversion = time.strftime("%H:%M:%S", time.gmtime(sec))
    print(conversion)
    return conversion
    
    
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
        file = open(filePath, "r", encoding="utf8")
        ui.deleteAllComments()
        loadComments()
        file.close()
    except(IOError, FileNotFoundError, FileExistsError):
        ui.showErrorMsgBox(main_consts.EXCEPTION_MSG_TITLE, main_consts.FILE_EXCEPTION_MSG_TEXT)

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
    timeManagement()

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