#!/usr/bin/env python
# coding: utf-8

# ## Setup

# In[1]:

import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("ROOT_VID", help="Path to the video to be summarized")
parser.add_argument("--INT_BW_DIV", help="Split moving objects - root.this => larger video => low overlapping")
args = parser.parse_args()
