
# coding: utf-8

# In[8]:


# Decomposes a video into component frames
# A specific timeframe of the video must be chosen
# The frames may also be cropped to specification

# Inputs
import cv2
import numpy as np
import os

##### Setting up all the paramaters and video for the splitters

captureInterval = 2 # Frame interval to be saved (in seconds)
startSecond = -1 # Start time in seconds
stopSecond = 10 # End time in seconds
trim = False # Indicates whether the video should be trimmed
crop = True # Indicates whether the frames should be cropped

video_destination = 'stable_melt.mp4' # File destination for the video to be analyzed

# Loading video
cap = cv2.VideoCapture(video_destination)

# Checking destination for saving images
try:
    if not os.path.exists(image_destination):
        os.makedirs(image_destination)
except OSError:
    print ('Error: Creating directory of data')
    
# Calculating start and stop in terms of frames
fps = cap.get(cv2.CAP_PROP_FPS)
if trim == True:
    startFrame = round(startSecond * fps)
    stopFrame = round(stopSecond * fps)
else:
    startFrame = 0
    stopFrame = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    stopFrame = 10000
    
########### splitting the frame to extract the actual image of the furnace!

print("start")

image_destination = 'data_frames' # Folder destination where the frames should be saved
xStartPct = .65 # Paramters of the cropped image in percentage of the frame
xStopPct = 0.95
yStartPct = .1
yStopPct = .5

# Calculating cropping parameters in terms of frames
if crop == True:
    xStartCell = round(xStartPct * cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    xStopCell = round(xStopPct * cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    yStartCell = round(yStartPct * cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    yStopCell = round(yStopPct * cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
else:
    xStartCell = 0
    xStopCell = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    yStartCell = 0
    yStopCell = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calculating capture interval in frames
frameInterval = captureInterval * round(fps)

# Iterating through the frames of the video
currentFrame = 0
nameFrame = 0
ret = True
while(ret):

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Saves only those images in the given timeframe and capture interval
    if currentFrame < startFrame or currentFrame%frameInterval != 0:
        currentFrame += 1
        continue

    # Saves image of the current frame in jpg file
    elif currentFrame < stopFrame:
        name = './' + image_destination + '/frame' + str(nameFrame) + '.jpg'
        cv2.imwrite(name, frame[yStartCell:yStopCell, xStartCell:xStopCell])
        nameFrame += 1
    # Breaks out of the loop if the stopFrame parameter is exceeded
    else:
        break
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print("done")


# In[18]:


########### splitting the frame to extract the present value parameter!

print("start")

image_destination = 'data_frames_present_value' # Folder destination where the frames should be saved

xStartPct = .69 # Paramaters of the cropped image in percentage of the frame
xStopPct = 0.73
yStartPct = .53
yStopPct = .56

# Calculating cropping parameters in terms of frames
if crop == True:
    xStartCell = round(xStartPct * cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    xStopCell = round(xStopPct * cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    yStartCell = round(yStartPct * cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    yStopCell = round(yStopPct * cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
else:
    xStartCell = 0
    xStopCell = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    yStartCell = 0
    yStopCell = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calculating capture interval in frames
frameInterval = captureInterval * round(fps)

# Iterating through the frames of the video
currentFrame = 0
nameFrame = 0
ret = True
while(ret):

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Saves only those images in the given timeframe and capture interval
    if currentFrame < startFrame or currentFrame%frameInterval != 0:
        currentFrame += 1
        continue

    # Saves image of the current frame in jpg file
    elif currentFrame < stopFrame:
        name = './' + image_destination + '/frame' + str(nameFrame) + '.jpg'
        cv2.imwrite(name, frame[yStartCell:yStopCell, xStartCell:xStopCell])
        nameFrame += 1
    # Breaks out of the loop if the stopFrame parameter is exceeded
    else:
        break
    currentFrame += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print("done")


# In[ ]:


######### splitting the frame to extract all the other parameters... (TO-DO)


# In[31]:


######### extracting the parameters and filling up the database

from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Image Treatment-5b3bb079ba4e.json'
from SciServer import CasJobs, Files, Authentication

casjobs_context='MyDB'
subject_name="Ali Rachidi"
    
class landmarkedimage:
    def __init__(self, presentValue): 
        self.presentValue = presentValue

    def print_landmarkedimage(self):
        print("Frame Number: " + self.frameNumber + '\n')
        print("upper_shaft_speed: ")
        print(self.upper_shaft_speed)
        print('\n')
        print(type(self.upper_shaft_speed))
        print("lower_shaft_speed: ")
        print(self.lower_shaft_speed)
        print('\n')
        print(type(self.lower_shaft_speed))

    frameNumber = ''
    points = dict(list())
    presentValue = 0.0
    setValue = 0.0
    
def detect_text(path):
   
    client = vision.ImageAnnotatorClient()
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description

files = [pos[:-4] for pos in os.listdir('data_frames_present_value') if pos.endswith('.jpg')]
for file in files:
    temp = detect_text('data_frames_present_value/' + file + '.jpg')
    print(temp)
    li = landmarkedimage(temp)
    insert_query = '''INSERT INTO furnaceStateHistory
                (presentValue)
                VALUES
                ({0})'''.format(temp)
    insert_query = '''insert into furnaceStateImages (image) 
                SELECT BulkColumn 
                FROM Openrowset( Bulk 'data_frames/frame1.jpg', Single_Blob) as img'''
    CasJobs.executeQuery(sql=insert_query, context=casjobs_context)


# In[29]:


insert_query = '''ALTER DATABASE [MyDB] SET TRUSTWORTHY ON'''
CasJobs.executeQuery(sql=insert_query, context=casjobs_context)

