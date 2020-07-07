# import the necessary packages
import re
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
from random import randint
import numpy as np
from detection import detect
from Parse_GPS import GPS_interpolate_video_frames
from Scale import unique_id
from numpy.linalg import norm
import math
from collections import deque

def draw_box(img,newbox,lbl):
    p1 = (int(newbox[1]), int(newbox[0]))  # newbox[0] = x position , newbox[1] = y position ,newbox[2] = Width , newbox[3]= Height
   # p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
    p2 = (int(newbox[3]), int(newbox[2])) 
    cv2.rectangle(img, p1, p2,(0,0,255),3, 1) #draw the box with the crossponding colour
    #id=unique_id(p2,gps_coor)
    center=(int(0.5*(p1[0]+p2[0])),int(0.5*(p1[1]+p2[1])))
    txt=" #{}".format(lbl)
    cv2.putText(image, txt, (center[0]-60,center[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,default="./DJI_0057.mov",
help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
help="OpenCV object tracker type")
args = vars(ap.parse_args())

(major, minor) = cv2.__version__.split(".")[:2]
if int(major) == 3 and int(minor) < 3:
    tracker = cv2.Tracker_create(args["tracker"].upper())
else:
    OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
    }

# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])


bboxes = [] # list of bounding boxes of individual panels
#Detect=CellsDetector() # Initilize the panel Detector
frame=vs.read() #read a single frame from the sequence
# grab the current frame, then handle if we are using a
# VideoStream or VideoCapture object
frame = frame[1] if args.get("video", False) else frame

frame = imutils.resize(frame, width=1500) #resize the frame
#frame=cv2.resize(frame,(1280,720))
(H, W) = frame.shape[:2] # get the frame dimensions 
fourcc =cv2.VideoWriter_fourcc(*'XVID') # output video format5
video_hight=720 # Output video Width
video_width=1280 # Output video Height
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (video_width,video_hight)) #output video

Detected=False # flag used to control the flow of the program (start and end the detecting phase)
Tracking =False # flag used to control the flow of the program (start and end the tracking phase)
Counter=0 # a variable that tracks the number of detected solar panels
Finish_line=H*0.8# The Finish line where we stop tracking old panels and search for new ones


gps_loc=GPS_interpolate_video_frames(args.get("video", False),"DJI_0057.srt")
index=0
    
ref_frame_axies_deq = deque(maxlen=7)
ref_frame_label_deq = deque(maxlen=7)
min_distance = 30
label_cnt = 1
# loop over frames from the video stream
while True:
    # grab the current frame, then handle if we are using a
    # VideoStream or VideoCapture object
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    # check to see if we have reached the end of the stream
    if frame is None:
        break
    # resize the frame (so we can process it faster) and grab the
    # frame dimensions
    frame = imutils.resize(frame, width=1500) #resize the frame
    #frame=cv2.resize(frame,(1280,720))
    (H, W) = frame.shape[:2] # get the frame dimensions 
    image=frame.copy() # take a copy from the frame
    #frame=cv2.GaussianBlur(frame,(3,3),1)
    #frame=cv2.blur(frame,(3,3))

    bboxes,masks,scores=detect(frame) # detect solar panels on the region of interestadjust_gamma
    conf_box_count=0
    cur_frame_axies = []
    cur_frame_label = []
    for idx,box in enumerate(bboxes):
        x=box[0]
        y=box[1]
        W=box[2]-box[0]
        H=box[3]-box[1]
        aspect_ratio=H/W
        area=H*W
        if(scores[idx]>= 0.995 and area >6000 and (0.7<=aspect_ratio<=2.2) ) :
            conf_box_count+=1
    label_list=list(ref_frame_label_deq)
    axies_list=list(ref_frame_axies_deq)
    ref_frame_label=[item for sublist in label_list for item in sublist]
    ref_frame_axies=[item for sublist in axies_list for item in sublist]
    if conf_box_count >=4: 
        pass# Detected=True # if the number of detected panels >=1 trigger the "deteced" flag
        for idx,box in enumerate(bboxes):
            #cv2.drawContours(image, [cnt], 0, (0,255,255), 5,offset= (-30,-30 )) 
            x=box[0]
            y=box[1]
            W=box[2]-box[0]
            H=box[3]-box[1]
            aspect_ratio=H/W
            area=H*W
            cx=(box[0]+box[2])/2
            cy=(box[1]+box[3])/2
            if(scores[idx]>=0.995 and area >8000 and (0.7<=aspect_ratio<=2.2) ):
                lbl = float('nan')
                if(len(ref_frame_label) > 0):
                    b = np.array([(cx,cy)])
                    a = np.array(ref_frame_axies)
                    distance = norm(a-b,axis=1)
                    min_value = distance.min()
                    if(min_value < min_distance):
                        idx = np.where(distance==min_value)[0][0]
                        lbl = ref_frame_label[idx]
                if(math.isnan(lbl)):
                    lbl = label_cnt
                    label_cnt += 1
                cur_frame_label.append(lbl)
                cur_frame_axies.append((cx,cy))
                draw_box(image,box,lbl)
    ref_frame_label_deq.append(cur_frame_label)
    ref_frame_axies_deq.append(cur_frame_axies)
            
    #print(scores)
        #for a in areas:
        #    print(a)


    text= "# {} GPS ({})".format(Counter,gps_loc[index]) # print the number of panels on the image
    index+=1
    #cv2.putText(image, text, (10, H - 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)  # print the number of panels on the image          
    #cv2.imshow("Image", image) # show the image
    video=cv2.resize(image,(video_width,video_hight))
    cv2.imshow("Video", video)
    out.write(video)
    key = cv2.waitKey(1) & 0xFF # delay to control FPS
    if key == ord("s"):
        out.release()
        vs.release()
        cv2.destroyAllWindows()
    if key ==ord("p"):
         cv2.waitKey()

         print(index,gps_loc[index])
         cv2. imwrite("Sample_Tracking.png",video) 

    if(index in range(400,800)):
        name="IMG_{}.png".format(index)
        cv2. imwrite(name,image) 
out.release()
vs.release()
cv2.destroyAllWindows()



