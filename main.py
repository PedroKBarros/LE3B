from UI.ui import *
import threading
from collections import namedtuple, deque
import main_constants as main_consts

filePath = ""
Comment = namedtuple("Comment", "abbreviatedAuthorName colorAbbreviated authorName time text state")
commentsQueue = deque()

def setFilePath(path):
    filePath = path

def commentsManagement():
    load_thread = threading.Thread(target=loadComments)
    load_thread.start()

def loadComments():
    pass
    #try:
    #file = open(filePath, "r")
    #except(IOError, FileNotFoundError, FileExistsError):
    #pass
    #else: #Caso ocorra uma exceção, mas não seja nenhuma das definidas
    

if __name__ == "__main__":
    executaUI()