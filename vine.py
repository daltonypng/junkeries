from os import walk
import queue
import threading
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

encodingsList = ["utf8", "cp1252", "iso-8859-1", "iso-8859-2"]
maxExcondingsSuported = len(encodingsList)

search_queue = queue.Queue()
event = threading.Event()

def try_open(file, n):

    try:
        currentEncoding = encodingsList[n]
        currentFile = open(file,encoding=currentEncoding)
        fileContent = currentFile.readlines()
        if fileContent:
            return fileContent
    except:
 
        n += 1
        if n < maxExcondingsSuported:
            return try_open(file, n)
 
    return ""
 
def search_worker():

    while True: 

        if event.is_set() and search_queue.empty():
            return 

        item = search_queue.get()
        fileContent = try_open(item, 0)
        n = 0
        
        for line in fileContent:
            n += 1
            if search_pattern in line: 
                print(bcolors.OKCYAN + item + ":" + bcolors.ENDC + bcolors.OKGREEN + str(n) + bcolors.ENDC + "\n" + 
                      line.lstrip())

def seek_and_destroy(path, extension):

    search_len = len(extension) * -1
    
    for (dirpath, dirnames, filenames) in walk(path):
        if dirnames:
            for sub_dir in dirnames:
                seek_and_destroy(path + sub_dir + "/", extension)

        for fileName in filenames:
            if fileName[search_len:] == extension:
                search_queue.put(dirpath + fileName)

    event.set()

def vine():

    path = input("File path: ")
    extension = input("File extension *.")

    if not path:
        path = "."

    if extension:
        extension = "." + extension

    print("---------------------")

    threading.Thread(target=search_worker).start()

    seek_and_destroy(path, extension)

if __name__ == "__main__":

    search_pattern = input("Search pattern: ")
    vine()

