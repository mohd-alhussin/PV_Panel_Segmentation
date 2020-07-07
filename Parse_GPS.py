import numpy as np
import srt
import re
import cv2
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def get_cartesian(lat=None,lon=None):
    lat, lon = np.deg2rad(lat), np.deg2rad(lon)
    R = 6371 # radius of the earth
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R *np.sin(lat)
    return (x,y)

def getGPSdata(filename='DJI_0057.srt'):
    with open(filename, 'r') as myfile:
        data = myfile.read()


    subtitle_generator = srt.parse(data)
    subtitles = list(subtitle_generator)

    GPS_seconds=[]
    for sub in subtitles:
        text =sub.content
        try:
            found = re.search(r'([-+]?[\d]{1,2}\.\d+),(\s*[-+]?[\d]{1,3}\.\d+)', text)
            latitude = float(found.group(1)) # apply your error handling
            longitude = float(found.group(2))
        except AttributeError:
            # AAA, ZZZ not found in the original string
            latitude = 0 # apply your error handling
            longitude = 0
        found.group(1)
        GPS_seconds.append((latitude,longitude))
    return GPS_seconds



def GPS_tracker(gps_data):
    curr_point=0
    curr_start=0
    direction=[(0,0) for i in range(len(gps_data))]
    for i in range(len(gps_data)):
        diff=tuple(x-y for x, y in zip(gps_data[i],gps_data[curr_point]))
        if (diff==(0,0)):
            pass
        else :
            for k in range(curr_point,i+1):
                direction[k]=tuple(np.sign(x-y) for x, y in zip(gps_data[i],gps_data[curr_point]))
            curr_point=i
    return direction

def GPS_unique_points(gps_data):
    curr_point=0
    curr_start=0
    unique=[]
    unique.append((curr_point,gps_data[curr_point]))
    for i in range(len(gps_data)):
        diff=tuple(x-y for x, y in zip(gps_data[i],gps_data[curr_point]))
        if (diff==(0,0)):
            pass
        else :
            curr_point=i
            unique.append((curr_point,gps_data[curr_point]))
            
    return unique


def GPS_interpolate_video_frames(video_filename,srt_filename):
    video=cv2.VideoCapture(video_filename)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    #print(total_frames)
    fps=  video.get(cv2.CAP_PROP_FPS)

    print(fps)
    duration= total_frames/fps


    with open(srt_filename, 'r') as myfile:
        data = myfile.read()
    subtitle_generator = srt.parse(data)
    subtitles = list(subtitle_generator)
    #total_Seconds=subtitles[-1].start
    #print(total_Seconds.seconds)

    gps_data=getGPSdata(srt_filename)
    unique_points=GPS_unique_points(gps_data)
    t,Coordinates=map(list, zip(*unique_points))
    latitude,longitude=map(list, zip(*Coordinates))
    #print(Coordinates)
    #print(t)
    #print(latitude)
    #print(longitude)
    get_lat_sec = interp1d(t, latitude, kind='linear',fill_value="extrapolate")
    get_long_sec = interp1d(t, longitude, kind='linear',fill_value="extrapolate")

    GPS_locations= []
    for i in range(total_frames):
        t= i/fps
        Lat =float(get_lat_sec(t))
        Lon =float(get_long_sec(t))
        GPS_locations.append(get_cartesian(Lat,Lon))
        #GPS_locations.append((Lat,Lon))

#    print(GPS_locations)
    return GPS_locations



print(get_cartesian(lat= 24.767652, lon=55.370478 ))

loc1=(24.767629, 55.370478)
loc2=(24.767623, 55.370984)
l1=get_cartesian(loc1[0],loc1[1])
l2=get_cartesian(loc2[0],loc2[1])
angle= np.arctan((np.abs(l2[1]-l1[1]))/(np.abs(l2[0]-l1[0])))
#angle *= 180 / np.pi
print(angle)
#GPS_interpolate_video_frames("DJI_0057.mov","DJI_0057.srt")



