# OCR And Database Comparison
import os # Access To Command Line
import re # Delete Unwanted Characters From String
import getpass # Fetch username
import sqlite3 # Enable Use Of SQL
from cv2 import * # Image Alteration
import pytesseract # Image To String
from PIL import Image # Load / Output Image


# A] Fetch User Details
username = getpass.getuser() # Fetches username
if os.path.exists('/Users/{}/Downloads/Pictures'.format(username)) == False: # Check if path exists
    os.mkdir('/Users/{}/Downloads/Pictures'.format(username))
os.chdir('/Users/{}/Downloads/Pictures'.format(username)) # Change working directory


# B] Take Picture
print ("Press 'Space' To Take A Picture \n"
        "Press 'Escape' To Exit")

cam = cv2.VideoCapture(0) # Open live video camera
cv2.namedWindow("Take Picture") # Name window
while True: # While the window is open
    ret, frame = cam.read()
    cv2.imshow("Take Picture", frame)
    if not ret:
        break
    wait = cv2.waitKey(1)

    if wait%256 == 27: # ESC pressed
        print("Escape hit, closing...")
        break
    elif wait%256 == 32: # SPACE pressed
        img_name = "Company_Name.png"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))

cam.release()
cv2.destroyAllWindows()
usr_pic = img_name

# C] Apply Filters To Image
image = cv2.imread('/Users/{}/Downloads/Pictures/{}'.format(username, usr_pic), 0) # Read image & convert to greyscale
gray = cv2.threshold(image, 0, 255, # Separate foreground and background
	   cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
gray = cv2.medianBlur(gray, 3) # Blur image to smoothen pixelation


# D] Store Image To Disk As Temporary File
filename = "/Users/{}/Downloads/Pictures/{}".format(username, usr_pic, os.getpid()) # Write image to disk
cv2.imwrite(filename, gray)


# E] Load Image - Apply OCR - Delete Image
text = pytesseract.image_to_string(Image.open(filename)) # Apply PyTesseract to image
text = re.sub('[!"#$%&()*+,-./:;<=>?@^_`{|}~123456789]', '', text) # Remove unwanted characters
text = text.strip() # Deletes whitespace
text = text.lower() # Converts all text to lowercase
os.remove(filename) # Delete temporary file
print(text)

# F] Compare Interpreted Text With Database
conn = sqlite3.connect('example_table.db') # Establish connection with SQL server
cnct = conn.cursor() # Create cursor object

try: # Attempt fetching company details
    result = cnct.execute ("SELECT * FROM Company \
                            WHERE NAME LIKE '%s'" % text)
    for row in result: # Print each row of the company's data
        print (row)

except Exception as ex: # If company cannot be found, identify error
    print(ex)

conn.commit()
conn.close()
