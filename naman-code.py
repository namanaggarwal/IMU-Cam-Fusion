#! /usr/bin/python

import smbus
import math
import time
import cv2.cv as cv
import os

#PATH FOR STORING IMAGES# 
#os.makedirs(~/Images)


data_ = open("Data.txt","w+")

bus = smbus.SMBus(1)

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
	return bus.read_byte_data(address, adr)

def read_word(adr):
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr+1)
	val = (high<<8) + low
	return val

def read_word_2c(adr):
	val = read_word(adr)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:	
		return val
# For Magnetometer
address_ = 0x1e
def write_byte(adr,value):
	bus.write_byte_data(address_, adr, value)
	
bus.write_byte_data(address_, 0x00, 0x60)
bus.write_byte_data(0x1E, 0x02, 0x00)

scale = 0.92
###################

bus = smbus.SMBus(1)
address = 0x68
bus.write_byte_data(address, power_mgmt_1, 0)

t0 = time.time()
imu.write("Computer Time: " + str(t0) + "\n")
imu.write("Computer_Time (time_elapse_epoch), timestamp (sec), Image Number, camera_capture_time (sec), ax,AccelX (m/s2), ay,AccelY (m/s2), az,AccelZ (m/s2), gx, GyroX (Rad/s), gy, GyroY (Rad/), gz, GyroZ Rad/s, MagX (Gauss), MagY(Gauss), MagZ (Gauss), Bearing\n")

#CAMERA CODE
cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)

i = 1
while(1):
# IMU CODE
	ti = time.time()
	timestamp = ti - t0
	print "Time Stamp",ti-t0
	print

	print "gyro data"
	print "------------"


	gyro_xout = read_word_2c(0x43)
	gyro_yout = read_word_2c(0x45)
	gyro_zout = read_word_2c(0x47)

	print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout/131.)
	print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout/131.)
	print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout/131.)

	print	
	print "accelerometer data"
	print "-------------"

	accel_xout = read_word_2c(0x3b)
	accel_yout = read_word_2c(0x3d)
	accel_zout = read_word_2c(0x3f)

	print "accel_xout: ", accel_xout, " scaled: ", 	(accel_xout/16384.)
	print "accel_yout: ", accel_yout, " scaled: ", (accel_yout/16384.)
	print "accel_zout: ", accel_zout, " scaled: ", (accel_zout/16384.)
	print

	# print mag values
	print"magnetometer data"
	print"----------"
	data = bus.read_i2c_block_data(address_, 0x03, 6)
	xMag = data[0] * 256. + data[1]
	if xMag > 32767 :
		xMag -= 65536

	zMag = data[2] * 256. + data[3]
	if zMag > 32767 :
		zMag -= 65536

	yMag = data[4] * 256. + data[5]
	if yMag > 32767 :
		yMag -= 65536

	
	bearing = math.atan2(yMag,xMag)
	if (bearing<0):
		bearing += 2*math.pi
	print "Bearing: ",math.degrees(bearing)
	print

	
# CAMERA CODE
	ti_camera = time.time()
	img = cv.QueryFrame(capture)
	cv.ShowImage("camera", img)
	cv.SaveImage('pic{:>05}.jpg'.format(i), img)
	camera.write("Image "+ str(i)+ ": " +  str(ti_camera - t0) + " s \n ")
	if cv.WaitKey(1) == 27:
		break

	data_.write(str(ti) + ", " +str(timestamp) + ", " + str("Image " + str(i)) + "," + str(ti_camera - t0) + ","+ str(accel_xout) + ", " + str(accel_xout/16384.) + ", " + str(accel_yout) + ", " + str(accel_yout/16384.) + ", " + str(accel_zout)+ ", " + str(accel_zout/16384.) + ", " 
		+ str(gyro_xout)+ ", " + str(gyro_xout/131.)+ ", " + str(gyro_yout)+ ", " + str(gyro_yout/131.)+ ", " + str(gyro_zout)+ ", " + str(gyro_zout/131.)+ ", " 
		+ str(xMag)+ ", " + str(yMag)+ ", " + str(zMag) + ", " + str(math.degrees(bearing)) + "\n")

	i=i+1
