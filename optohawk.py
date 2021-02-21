#!/usr/bin/env python
# coding: utf-8

# ## Setup

# In[1]:

import os
import cv2
import argparse
import progressbar

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

with progressbar.ProgressBar(max_value=total_frames) as bar:
   
        #if
        ret, frame = cap.read()
        
        if ret==True:
            fgmask = fgbg.apply(frame)
            (contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
            while ret:
                fcount += 1
                bar.update(fcount)
                try:
                    cv2.accumulateWeighted(frame, avg2, 0.01)
                except:
            break

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
