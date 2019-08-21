import os, shutil
from os.path import splitext

# Type Working Directory here
os.chdir(r"C:\Users\User\Pictures\iPhone pics\Phone Pics")

# Load contents of directory
dirContents = os.listdir('.\\')

# Define function to list all extension types.
def extensionsPresent(sourceList):
    print('Listing all present file types...')
    if not sourceList:
        print('No files present')
        return None
    else:
        extensionsList = []
        for item in sourceList:
            filename, extension = splitext(item)
            if extension not in extensionsList:
                extensionsList.append(extension)
        print('File types present: {}'.format(extensionsList))    
        return extensionsList    
        

# Main function - creates folder for an extension and moves files into it.
def pickyList(sourceList, extension):
    oneFolderCreation(extension)
    destinationPath = ('.\\{} Files\\'.format(extension[1:]))
    movedFileCount = 0
    for item in sourceList:
        
        itemFilename, itemExtension = splitext(item)
        
        if itemExtension == extension:
            shutil.move(item, destinationPath)
            movedFileCount += 1
    print('Moved {} files to {}'.format(movedFileCount, destinationPath))
    movedFileCount = 0
# Define a function to create a new folder for each extension type.
def folderCreation(extensionsList):
    for item in extensionsList:
        foldername = ('{} Files'.format(item[1:]))
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            print('{} folder created'.format(foldername))
        
def oneFolderCreation(extension):
        foldername = ('{} Files'.format(extension[1:]))
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            print('{} folder created'.format(foldername))
    

   
extensionsInFolder = extensionsPresent(dirContents) # Make as a variable, else it will run this function each time

folderCreation(extensionsInFolder)

for item in extensionsInFolder:
    pickyList(dirContents, item)
    