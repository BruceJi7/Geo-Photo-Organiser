# Geo-Photo-Organiser
Includes program to sort a folder's contents into new folders by type, a program to organise photos by what camera it was taken by, and a program to organise photos with location data into folders based on location 

GEO PHOTO ORGANISER
Currently exists as three separate files.


RAW_JPG_PNG_Sorter: Takes a folder as an argument, finds all file types, and places them into folders based on that type.

ExifSorter: Sorts all images in a folder based on type, and then sorts images based on EXIF data, namely, what device it was taken with.

Geo_Sorter: Sorts all images in a folder, first checking for the existence of location EXIF data, and then, creates folders based on key address data and moves photos there.


TODO:

- Add import to Geo Sorter to allow it to perform RAW-JPG and Exif Sorter tasks before performing its own:
    - Add name-main statements to raw-jpg and exif sorter to help this.
    
- Test Geo Sorter with more addresses - It works with Korean, Japanese and UK addresses, but it may be necessary to create a module holding the necessary instructions for different address protocols so that it can always sort effectively.


