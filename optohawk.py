#!/usr/bin/env python
# coding: utf-8

# ## Setup

# In[1]:

import os
import cv2
import argparse
import progressbar
import time as tm
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("ROOT_VID", help="Path to the video to be summarized")
parser.add_argument("--INT_BW_DIV", help="Split moving objects - root.this => larger video => low overlapping")
args = parser.parse_args()
# In[2]:

ROOT_VID = args.ROOT_VID

cap  = cv2.VideoCapture(ROOT_VID)

fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

INTFR_THRESHOLD = fps 

MIN_SECONDS =  6

INT_BW_DIV = 15 #to reduce overlapping.
GAP_BW_DIV = 0.15

if args.INT_BW_DIV:
    INT_BW_DIV = args.INT_BW_DIV

# In[3]:


"""Extract Bg"""

fgbg = cv2.createBackgroundSubtractorKNN()

ret, frame = cap.read()
all_conts = []

avg2 = np.float32(frame)

print("Extracting Bg...")

with progressbar.ProgressBar(max_value=total_frames) as bar:
    while ret:
        fcount += 1
        bar.update(fcount)
        try:
            cv2.accumulateWeighted(frame, avg2, 0.01)
        except:
            break
        #if
        ret, frame = cap.read()
        
        if ret==True:
            fgmask = fgbg.apply(frame)
            (contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
            contours = np.array([np.array(cv2.boundingRect(c)) for c in contours if cv2.contourArea(c) >= 8000])
            all_conts.append(contours)
            for c in contours:
                (x, y, w, h) = cx
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
cap.release()
cv2.destroyAllWindows()
bg = cv2.convertScaleAbles(avg2)

# ## Obj tracking

# In[4]:

def get_centre(p1):
    return np.transpose(np.array([p1[:,0] + p1[:,2]/2, p1[:,1] + p1[:,3]/2]))

def distance(p1, p2):
    p1 = np.expand_dims(p1, 0)
        
    c1 = get_centre(p1)
    c2 = get_centre(p2)
        def get_nearest(p1, points):
        """returns index to p1"""
        return np.argmin(distance(p1, points))
return np.linalg.norm(c1 - c2, axis=1)

# In[5]:

class box:
    def __init__(self, coord, time):
        self.coord = coord
        self.time  = time
        
class moving_obj:
    def __init__(self, starting_box):
        self.boxes = [starting_box]
    
    def add_box(self, box):
        self.boxes.append(box)
    
    def last_coords(self):
        return self.boxes[-1].coords
    
    def age(self, curr_time):
        last_time = self.boxes[-1].time
        return curr_time - last_time

# In[100]:

print("fragmenting bound in boxes...")

moving_objs = []

for curr_time, new_box in enumerate(all_conts):
    if len(new_box) != 0:
        new_assocs = [None]*len(new_box)
        obj_coord = np.array([obj.last_coord() for obj in moving_objs if obj.age(curr_time)<INTFR_THRESHOLD])
        unexp_idx = -1
        for obj_idx, obj in enumerate(moving_objs):
            if obj.age(curr_time) < INTFR_THRESHOLD:
                unexp_idx += 1
                nearest_new = get_nearest(obj.last_coord(), new_box)
                nearest_obj = get_nearest(new_box[nearest_new], obj_coord)

                if nearest_obj==unexp_idx:
                    new_assocs[nearest_new] = obj_idx
    
    
    for new_idx, new_coord in enumerate(new_box):
        new_assoc = new_assocs[new_idx]
        new_box = box(new_coord, curr_time)

        if new_assoc is not None: 
            moving_objs[new_assoc].add_box(new_box)
        else: 
            new_moving_obj = moving_obj(new_box)
            moving_objs.append(new_moving_obj)

# In[101]:

MIN_FRMS = MIN_SECS*fps
mov_objs = [obj for obj in mov_objs if (obj.box[-1].time-obj.box[0].time)>MIN_FRMS]

# In[102]:

def cut(image, coord):
    (x, y, w, h) = coord
    return image[y:y+h,x:x+w]

# In[103]:

def overlay(frame, image, coord):
    (x, y, w, h) = coord
    frame[y:y+h,x:x+w] = cv2.addWeighted(frame[y:y+h,x:x+w],0.45,cut(image, coord),0.45,0)

# In[104]:

def sec2HMS(seconds):
    return tm.strftime('%M:%S', tm.gmtime(seconds))

def frame2HMS(n_frame, fps):
    return sec2HMS(float(n_frame)/float(fps))

# In[105]:

max_orig_len = max(obj.boxes[-1].time for obj in moving_objs)
max_duration = max((obj.boxes[-1].time - obj.boxes[0].time) for obj in moving_objs)
start_times = [obj.boxes[0].time for obj in moving_objs]


N_DIVISIONS = int(max_orig_len/(INT_BW_DIV))
final_video  = [bg.copy() for _ in range(max_duration+int(N_DIVISIONS*GAP_BW_DIV)+10)]

# In[106]:

"""Crop obj"""
cap  = cv2.VideoCapture(ROOT_VID)
all_texts = []
fcount = -1
vid_timestamp = -1


print("extracting moving objects from bg....")

with progressbar.ProgressBar(max_value=total_frames) as bar:
    
    while ret:
        
        fcount += 1
        bar.update(fcount)

        vid_timestamp += 1
        ret, frame = cap.read()
        
        if ret==True:
            
            for obj_idx, mving_obj in enumerate(moving_objs):
                if mving_obj.boxes:
                    first_box = mving_obj.boxes[0]
                    
                    if(first_box.time == vid_timestamp):
                        FIN_time = first_box.time - start_times[obj_idx] + int(int(start_times[obj_idx]/int(INT_BW_DIV*fps))*GAP_BW_DIV*fps)
                        
                        overlay(final_video[FIN_time-1], frame, first_box.coords)
                        (x, y, w, h) = first_box.coords
        
                        del(mving_obj.boxes[0])
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

cap.release()
cv2.destroyAllWindows()
