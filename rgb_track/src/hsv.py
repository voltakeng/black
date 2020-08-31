#!/usr/bin/env python 

import cv2
import numpy as np 

yellow = np.uint8([[[240,240,240 ]]])
hsv_yellow = cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
print(hsv_yellow)
