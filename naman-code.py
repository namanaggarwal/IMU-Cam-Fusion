#! /usr/bin/python

import smbus
import math
import time
import csv

imu = open("imuData.txt","w+")
imu.write("Computer_Time, timestamp, ax,AccelX, ay,AccelY, az,AccelZ, gx, GyroX, gy, GyroY, gz, GyroZ, MagX, MagY, MagZ, Bearing\n")

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
	
write_byte(0,0b01110000)
write_byte(1,0b01110000)
write_byte(2,0b01110000)

scale = 0.92
###################

bus = smbus.SMBus(1)
address = 0x68
bus.write_byte_data(address, power_mgmt_1, 0)

t0 = time.time()
imu.write("Computer Time: " + str(t0) + "\n")

while(1):
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
	x_out = scale*read_word_2c(3)
	y_out = scale*read_word_2c(7)
	z_out = scale*read_word_2c(5)
	
	bearing = math.atan2(y_out,x_out)
	if (bearing<0):
		bearing += 2*math.pi
	print "Bearing: ",math.degrees(bearing)
	print

	imu.write(str(ti) + ", " +str(timestamp) + ", " + str(accel_xout) + ", " + str(accel_xout/16384.) + ", " + str(accel_yout) + ", " + str(accel_yout/16384.) + ", " + str(accel_zout)+ ", " + str(accel_zout/16384.) + ", " 
		+ str(gyro_xout)+ ", " + str(gyro_xout/131.)+ ", " + str(gyro_yout)+ ", " + str(gyro_yout/131.)+ ", " + str(gyro_zout)+ ", " + str(gyro_zout/131.)+ ", " 
		+ str(x_out)+ ", " + str(y_out)+ ", " + str(z_out) + ", " + str(math.degrees(bearing)) + "\n")
