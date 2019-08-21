import os, pprint, shutil
from exif import Image




workingDir = r'C:\Users\User\Pictures\iPhone pics\Phone Pics\JPG Files'

os.chdir(workingDir)

# JPGFileList = [item for item in os.listdir()]
JPGFileList = [item for item in os.listdir() if os.path.splitext(item)[1] in ('.JPG', '.JPEG')]


imageCameras = {
    'No Camera Specified' : [],
}

for JPGFile in JPGFileList:
    with open(JPGFile, 'rb') as image_file:
        my_image = Image(image_file)
    try:
        camera = my_image.model
        if 'SM-G' in camera:
            camera = 'Samsung Galaxy'
        if camera in imageCameras:
            imageCameras[camera].append(JPGFile)
        else:
            imageCameras[camera] = [JPGFile]
        
    except:
        imageCameras['No Camera Specified'].append(JPGFile)

for cameraType in imageCameras.keys():
    print(f'Working on {cameraType}...')
    folderName = f'Taken By {str(cameraType)}'
    folderPath = os.path.join(workingDir, folderName)
    print(folderPath)
    if not os.path.exists(folderPath):
        os.makedirs(folderName)

    for item in imageCameras[cameraType]:
        sourcePath = os.path.join(workingDir, item)
        destinationPath = os.path.join(workingDir, folderName, item)
        shutil.move(sourcePath, destinationPath)
