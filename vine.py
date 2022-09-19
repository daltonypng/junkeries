from os import walk
import queue

encodingsList = ["utf8", "cp1252", "iso-8859-1", "iso-8859-2"]
maxExcondingsSuported = len(encodingsList)

search_queue = queue.Queue()
result_queue = queue.Queue()

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

    while not search_queue.empty():
        
        item = search_queue.get_nowait()
        fileContent = try_open(item, 0)
        n = 0
        
        for line in fileContent:
            n += 1
            if search_pattern in line: 
                result_queue.put(item + ":" + str(n) + " " + line)
        
def seek_and_destroy(path, extension):

    search_len = len(extension) * -1
    
    for (dirpath, dirnames, filenames) in walk(path):
        if dirnames:
            for sub_dir in dirnames:
                seek_and_destroy(path + sub_dir + "/", extension)

        for fileName in filenames:
            if fileName[search_len:] == extension:
                search_queue.put(dirpath + fileName)
    
def vine():

    path = input("File path: ")
    extension = input("File extension *.")

    if not path:
        path = "."

    if extension:
        extension = "." + extension

    seek_and_destroy(path, extension)
    search_worker()

    print("---------------------")
 
    while not result_queue.empty():
        print(result_queue.get_nowait())

if __name__ == "__main__":

    search_pattern = input("Search pattern: ")
    vine()
