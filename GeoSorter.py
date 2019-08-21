from pygeocoder import Geocoder
from exif import Image
import os, pprint, shelve, shutil


GMapsAPIKey = 'AIzaSyBXHyXkaYJfV_b3lWfViibeQxC_85fL0Qo'
GEOAPI = Geocoder(api_key=GMapsAPIKey)

workingDir = r'C:\Users\User\Pictures\iPhone pics\Phone Pics\JPG Files\Taken By iPhone 7'
os.chdir(workingDir)

# Function to change from D-M-S system to Decimal Co-ords
def DMStoDecimal(DMSTuple):
    latitudeTuple = DMSTuple[0]
    latDegrees = latitudeTuple[0]
    latMins = latitudeTuple[1]
    latSecs = latitudeTuple [2]

    longitudeTuple = DMSTuple[1]
    longDegrees = longitudeTuple[0]
    longMins = longitudeTuple[1]
    longSecs = longitudeTuple [2]

    latDecimal = (latDegrees + (latMins / 60) + (latSecs / 3600))

    longDecimal = (longDegrees + (longMins / 60) + (longSecs / 3600))

    return (latDecimal, longDecimal)


# Versatile function to relocate files to new folder with custom name.
def moveFilesToNewFolder(listOfFiles, folderName):
    '''
    Relocate all files within 
    '''
    if listOfFiles:
        newFilePath = os.path.join('..\\', folderName)
        if os.path.exists(newFilePath):
            print(f'{newFilePath} folder already exists: skipping folder creation.')
        else:
            os.makedirs(newFilePath)
            print(f'{newFilePath} folder created.')
        print('Commencing file relocation...')
        for noGPSFile in listOfFiles:
            currentFilePath = os.path.join(workingDir, noGPSFile)
            destinationFilePath = os.path.join(newFilePath, noGPSFile)

            shutil.move(currentFilePath, destinationFilePath)
    else:
        print(f"There are no '{folderName}' files to move.")


# Function to extract EXIF GPS data, if it exists. Returns tuple separating files with and without GPS data.
def fetchGPSData(filelist):

    # Create dictionary of addresses for each image with that data  
    yesGPSImages = {}
    noGPSImages = []

        # Produce groups of files with and without GPS data

    for imageFile in filelist:
        with open(imageFile, 'rb') as loadedImage:
            currentImage = Image(loadedImage)
            print(f'Working on file {imageFile}.')

            try: # If the file has GPS data, list it as such        
                currentImageDMSCoords = (currentImage.gps_latitude, currentImage.gps_longitude)
                print(f'File {imageFile} has GPS Data: {currentImageDMSCoords}')

                yesGPSImages[imageFile] = currentImageDMSCoords

            except: # If the file has no GPS data, list it as such.
                print(f'File {imageFile} appears to have no GPS Data')
                noGPSImages.append(imageFile)

    return (yesGPSImages, noGPSImages)


# Function to gather address data from files with GPS data, via GMaps API
def getAddresses(dicOfFiles):
    imageAddresses = {}
        # Gather address data
    for imageFile in dicOfFiles.keys():
        currentImageFileCoords = dicOfFiles[imageFile]
                
        #Convert to Google-Friendly Decimal Co-ords
        currentImageDecimalCoords = DMStoDecimal(currentImageFileCoords)

        print(f'Collecting address data for {imageFile}...')
        APIresultAddress = GEOAPI.reverse_geocode(currentImageDecimalCoords[0], currentImageDecimalCoords[1])
        APIresultCountry = APIresultAddress[0].country
        print(f'For image {imageFile}...')
        
        addressAsList = addressBreaker(APIresultAddress[0])
        
        imageAddresses[imageFile] = addressAsList


    print('Address gathering complete.')

    return imageAddresses


def addressBreaker(APIResultObject):

    outputAddress = []

    countryResult = APIResultObject.country

    postalTownResult = APIResultObject.postal_town
    
    specialResult = APIResultObject.point_of_interest

    adminResults = {
        'level_1' : APIResultObject.administrative_area_level_1, 
        'level_2' : APIResultObject.administrative_area_level_2,
        'level_3' : APIResultObject.administrative_area_level_3,
        'level_4' : APIResultObject.administrative_area_level_4,
        'level_5' : APIResultObject.administrative_area_level_5
                                    
    }

    localityResults = APIResultObject.locality

    subLocResults = {
        'level_1' : APIResultObject.sublocality_level_1, 
        'level_2' : APIResultObject.sublocality_level_2,
        'level_3' : APIResultObject.sublocality_level_3,
        'level_4' : APIResultObject.sublocality_level_4,
        'level_5' : APIResultObject.sublocality_level_5
    }

    # pprint.pprint(APIResultObject.raw)

    # print(f'Country = {countryResult}')
    # for key in adminResults.keys():
    #     if adminResults[key]:
    #         print(f'admin {key} = {adminResults[key]}')
    #     # else:
    #     #     print(f'admin {key} has no data')


    # if localityResults:
    #     print(f'Locality = {localityResults}')

    # for key in subLocResults.keys():
    #     if subLocResults[key]:
    #         print(f'sublocality {key} = {subLocResults[key]}')
    #     # else:
    #     #     print(f'sublocality {key} has no data')

    # if specialResult:
    #     print(f'Point of interest = {specialResult}')
    # print('\n\n')


    #Adding results to meaningful list
    outputAddress.append(countryResult) # Add country

    if specialResult and localityResults:   # If it's a point of interest, it can have a simpler address 
        
        outputAddress.append(localityResults)
        outputAddress.append(specialResult)
    
    else:
        outputAddress.append(adminResults['level_1']) # Adding wide area result
        if adminResults['level_2']: 
            outputAddress.append(adminResults['level_2']) # Adding city/region result if exists

        if postalTownResult: # If it's the UK (or possibly USA), add this and skip 'sublocalities'
            outputAddress.append(postalTownResult)

        else: # Asian addresses may include sublocalities, so add those

            if subLocResults['level_1']: # In Korea, this is 'GU' level
                outputAddress.append(subLocResults['level_1'])

            if subLocResults['level_2']: # In Korea, this is 'DONG' level
                outputAddress.append(subLocResults['level_2'])


    return outputAddress
        



# Use this function if data already exists in the shelf.
def GPSgetFromShelf():
    # Load Data from PC instead of requesting from API.
    with shelve.open('imageAddressData') as shelfFile:
        addressDictionary = shelfFile['imageAddresses']
    pprint.pprint(addressDictionary)
    return (addressDictionary)


# Use this function for running the program for the first time
def APILocationTool():

    # Collect only JPG files into a list
    JPGFileList = [item for item in os.listdir() if os.path.splitext(item)[1] in ('.JPG', '.JPEG')]

    GPSFetchResults = fetchGPSData(JPGFileList)

    ImagesWithGPSData = GPSFetchResults[0]
    ImagesWithoutGPSData = GPSFetchResults[1]
    print(f'{len(ImagesWithoutGPSData)} files have no GPS data.')

    addressDictionary = getAddresses(ImagesWithGPSData)

    # with shelve.open('imageAddressData') as shelfFile:
    #     shelfFile['imageAddresses'] = addressDictionary
    # print('Addresses saved to shelve file.')

    # pprint.pprint(addressDictionary)


    moveFilesToNewFolder(ImagesWithoutGPSData, 'No Location Data')

    return(addressDictionary)


def moveToAddressFolder(addresses):

    for imageFile in addresses.keys():
        
        #Combine parts of list into a \\ padded path format
        try:
            foldersPath = '\\\\'.join(addresses[imageFile])
            print(foldersPath)
            destinationPath = os.path.join('..\\', foldersPath)
        except:
            destinationPath = os.path.join('..\\', 'Erratic Location Data')

        # Prepare destination path 

        sourcePath = os.path.join('.\\', imageFile)

        try:
            print(f'Creating folders at: {destinationPath}...')
            os.makedirs(destinationFolderPath, exist_ok=True)
        except:
            print(f'Folder {destinationPath} already exists')
        
        

        try:
            print(f'moving file {imageFile} into folder {destinationPath}...')
            shutil.move(sourcePath, destinationPath)
        except:
            try:
                print(f'Unexpected error when moving {imageFile}')
                print(f'Attempting to move to Erratic Location Data folder...')
                destinationPath = os.path.join('..\\', 'Erratic Location Data')
                shutil.move(sourcePath, destinationPath)
            except:
                print(f'Failed to move {imageFile}')
            
                
            

        
        






# APILocationTool()

workingDirDict = {
    'iPhone 7' : r'C:\Users\User\Pictures\iPhone pics\Phone Pics\JPG Files\Taken By iPhone 7',
    'iPhone 6' : r'C:\Users\User\Pictures\iPhone pics\Phone Pics\JPG Files\Taken By iPhone 6',
    'Samsung Galaxy' : r'C:\Users\User\Pictures\iPhone pics\Phone Pics\JPG Files\Taken By Samsung Galaxy',
    'QSS-32_33' : r'C:\Users\User\Pictures\iPhone pics\Phone Pics\JPG Files\Taken By QSS-32_33',
    'No-Camera' : r'C:\Users\User\Pictures\iPhone pics\Phone Pics\JPG Files\Taken By No Camera Specified'
}


for directory in workingDirDict.keys():
    workingDir = workingDirDict[directory]
    os.chdir(workingDir)
    addressDictionary = APILocationTool()
    moveToAddressFolder(addressDictionary)
    print(f'Operation completed for {directory}')

print('End of Operations')






