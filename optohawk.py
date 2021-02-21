#!/usr/bin/env python
# coding: utf-8

# ## Setup

# In[1]:

import os
import cv2
import argparse

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
