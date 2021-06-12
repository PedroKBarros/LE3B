import UI.ui_constants as ui_consts
import UI.ui as ui
import threading
from collections import deque
import main_constants as main_consts
import time

filePath = ""
file = None
commentsQueue = deque()
commentsQueueData = {"indexLastCommentRead": -1}
timeData = {"initialTime": 0.0, "currentTime": 0.0, "totalTime": 0.0, "velocity": 1, "state": main_consts.STOP_TIME_STATE}

def resetVariables():
    resetCommentsQueue()
    resetCommentQueueData()
    resetTimeData()

def resetCommentsQueue():
    global commentsQueue

    commentsQueue.clear()

def resetCommentQueueData():
    global commentsQueueData

    commentsQueueData["indexLastCommentRead"] = -1    

def resetTimeData():
    global timeData

    timeData["initialTime"] = 0.0
    timeData["currentTime"] = 0.0
    timeData["totalTime"] = 0.0
    timeData["velocity"] = 1
    timeData["state"] = main_consts.STOP_TIME_STATE


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
    if (len(commentsQueue) == 0):
        ui.updateUITotalTime(ui_consts.LABEL4_INITIAL_TEXT)
        return
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

def updateTimeVelocityByUI(newVelocity):
    global timeData
    timeData["velocity"] = newVelocity

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
        checkNextCommentToRead()
        time.sleep(1 / timeData["velocity"]) #espera 1 segundo
        timeData["currentTime"] += 1
        timeDiff = timeData["currentTime"] - timeData["initialTime"]
        ui.updateUICurrentTime(convertsecondsToUIFormat(timeDiff))
        updateCurrentTimeBar()
    
    if (isEndTime()):
        checkNextCommentToRead() #Para colocar o último comentário no estado read, caso ele tenha o time igual ao totalTime
        ui.handleEventPlayPauseButtonMouseLeftClick()
        ui.updateUICurrentTimeBar(ui_consts.IMAGE_PATH_TIME_BAR_SIZE_MAX[0])

def checkCommentsToChangeStateByCurrentTimeUserInput():
    #Essa função só é chamada após a ui validar o novo currentTime e atualizar o currentTime do timeData
    global timeData
    global commentsQueue
    global commentsQueueData

    if (isTimeLastCommentReadMoreThanCurrentTime()):
        print("READ TO LOADED")
        putCommentsReadToLoadedByCurrentTime()
        #Nesse caso, há pelo menos um comentário que deve ter seu estado alterado de read para loaded_state
    
    if (isTimeLastCommentReadLessThanCurrentTime()):
        print("LOADED TO READ")
        putCommentsLoadedToReadByCurrentTime()
        #Nesse caso, há ou não pelo menos um comentário que deve ter seu estado alterado de loaded para read

def putCommentsReadToLoadedByCurrentTime():
    global timeData
    global commentsQueue
    global commentsQueueData
    lastIndex = commentsQueueData["indexLastCommentRead"]
    currentTime = timeData["currentTime"]

    for i in range(lastIndex, -1, -1): #[lastIndex, -1[
        comment = commentsQueue[i]
        time = convertStrTimeToSeconds(comment["time"])
        if (time > currentTime):
            setCommentState(comment, 1)
            ui.formatCommentForLoaded(i)
            commentsQueueData["indexLastCommentRead"] = i - 1
        else:
            ui.positionsScrbarByUIComment(i)
            break #Se não é maior, é pq nenhum outro comentário anterior será

def putCommentsLoadedToReadByCurrentTime():
    global timeData
    global commentsQueue
    global commentsQueueData
    lastIndex = commentsQueueData["indexLastCommentRead"]
    currentTime = timeData["currentTime"]

    for i in range(lastIndex + 1, len(commentsQueue)): #[lastIndex + 1, len()[
        comment = commentsQueue[i]
        time = convertStrTimeToSeconds(comment["time"])
        if (time <= currentTime):
            setCommentState(comment, 2)
            ui.formatCommentForRead(i)
            commentsQueueData["indexLastCommentRead"] = i
        else:
            ui.positionsScrbarByUIComment(i)
            break #Se não é menor ou igual, é pq nenhum outro comentário seguinte será       

def isTimeLastCommentReadLessThanCurrentTime():
    global timeData
    global commentsQueue
    global commentsQueueData

    indexLastCommentRead = commentsQueueData["indexLastCommentRead"]
    if (indexLastCommentRead == -1):
        return True
    lastCommentRead = commentsQueue[indexLastCommentRead]
    lastTimeSecs = convertStrTimeToSeconds(lastCommentRead["time"])
    return lastTimeSecs < timeData["currentTime"]

def isTimeLastCommentReadMoreThanCurrentTime():
    global timeData
    global commentsQueue
    global commentsQueueData
    
    indexLastCommentRead = commentsQueueData["indexLastCommentRead"]
    if (indexLastCommentRead == -1):
        return False

    lastCommentRead = commentsQueue[indexLastCommentRead]
    lastTimeSecs = convertStrTimeToSeconds(lastCommentRead["time"])
    return lastTimeSecs > timeData["currentTime"]

def checkNextCommentToRead():
    global commentsQueue
    global commentsQueueData
    global timeData
    index = commentsQueueData["indexLastCommentRead"] + 1
    if (index == len(commentsQueue)):
        return
    nextComment = commentsQueue[index]
    timeNextComment = convertStrTimeToSeconds(nextComment["time"])
    if (timeNextComment != timeData["currentTime"]):
        return
    ui.formatCommentForRead(index)
    setCommentState(nextComment, 2)
    commentsQueueData["indexLastCommentRead"] = index
    ui.positionsScrbarByUIComment(index)


def setCurrentTime(newCurrentTime):
    global timeData
    if (newCurrentTime > timeData["totalTime"] or newCurrentTime < 0):
        return

    timeData["currentTime"] = newCurrentTime
    

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
        resetVariables()
        ui.resetVariables()
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
           
            comment = {"abbreviatedAuthorName": abbreviatedAuthorName, 
            "authorName": authorName, "time": time, 
            "text": text, "state": ""}
            setCommentState(comment, 0)
            commentsQueue.append(comment)
            ui.addComment(comment)
            lineNum = -1

        ui.updateStatusBar(main_consts.STATUS_BAR_LOAD_COMMENTS_TEXT + str(round((currentNumChars / totalChars), 2) * 100) + "%")
        lineNum += 1
        line = file.readline()
    
    ui.updateStatusBar(str(len(commentsQueue)) + main_consts.STATUS_BAR_LOADED_COMMENTS_TEXT)
    timeManagement()

def setCommentState(comment, numState):
    if (numState < 0 or numState > 2):
        return
    comment["state"] = main_consts.COMMENT_STATES[numState]

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