#! /usr/bin/env python
import cv2.cv as cv
import time

f= open("time_data.txt","w+")
cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)
i = 0

t0 = time.time()
while True:
	img = cv.QueryFrame(capture)
	cv.ShowImage("camera", img)
	cv.SaveImage('pic{:>05}.jpg'.format(i), img)
	#cv.SaveImage(str(interval) + ".jpg", img)
	ti = time.time()
	if i==0:
		f.write(str(0) + " s \n " )
	else:
		f.write(str(ti - t0) + " s \n ")
	if cv.WaitKey(10) == 27:
		break
	i += 1

f.close()
