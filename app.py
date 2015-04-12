#!/usr/bin/env python
# -*- coding: utf8 -*-

import threading

from PIL.Image import open
# import PIL
# import numpy as np
import cv2

# local modules
from video import create_capture
from common import clock, draw_str


import random
# import pygame
from Image import *


import celestial
from animator import Animator
# import OpenGL 
# OpenGL.ERROR_ON_COPY = True 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import datetime, time, sys, gc 


try:
	from numpy import *
except ImportError, err:
	try: 
		from Numeric import *
	except ImportError, err:
		print "This demo requires the numpy or Numeric extension, sorry"
		import sys
		sys.exit()



video_enabled = True
# video_enabled = False





textures = {}
def LoadTextures(fname):
	if textures.get( fname ) is not None:
		return textures.get( fname )
	texture = textures[fname] = glGenTextures(1)
	image = open(fname)

	ix = image.size[0]
	iy = image.size[1]
	image = image.tostring("raw", "RGBX", 0, -1)

	# Create Texture    
	glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)

	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	return texture







def detect(img, cascade):
	rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
	if len(rects) == 0:
		return []
	rects[:,2:] += rects[:,:2]
	return rects




W = H = 0

FACECENTER = {
	'x': 0,
	'y': 0
}

EYE = {
	'x': 0,
	'y': 10,
	'z': 0
}

A_FACECENTER = Animator(FACECENTER)
A_EYE = Animator(EYE)

VERTICAL_HEIGHT = 4

def drawCheckerBoard( N=20, white=GLfloat_3(.81,.81,.83), black=GLfloat_3(.1,.1,.3) ):
	"""Draw an 2N*2N checkerboard with given colours"""
	# return
	glDisable(GL_LIGHTING)
	glColor3fv(GLfloat_3(.1,.1,.2))

	# try:
	# 	glTranslatef(0, 0, -VERTICAL_HEIGHT);
	# 	glRectf(-N, -N, N, N)
	# 	glTranslatef(0, 0, VERTICAL_HEIGHT);
	# 	glTranslatef(0, 0, VERTICAL_HEIGHT);
	# 	glRectf(-N, -N, N, N)
	# 	glTranslatef(0, 0, -VERTICAL_HEIGHT);

	# finally:
	# 	# pass
	# 	glEnable(GL_LIGHTING)

	# return
	try:
		# h = 5

		#TOP BOTTOM
		# glTranslatef(0, 0, -VERTICAL_HEIGHT);
		# glRectf(-20, -20, 20, 20)
		# glTranslatef(0, 0, VERTICAL_HEIGHT);
		# glTranslatef(0, 0, VERTICAL_HEIGHT);
		# # glRectf(-20, -20, 20, 20)
		# white1=GLfloat_3(.1,.1,.25)
		# black1=GLfloat_3(.1,.1,.2)

		for x in range(-N, N, 4):
			# white=GLfloat_3(.5 + abs(.025 * x),.1,.1)
			# black=GLfloat_3(.5 + abs(.025 * x),.0,.0)
			for y in range(-N, N, 4):
				if (x + y) % 8 == 0:
					glColor3fv(white)
				else:
					glColor3fv(black)
				glTranslatef(0, 0, -VERTICAL_HEIGHT);
				glRectf(x, y, x + 3.95, y + 3.95)
				glTranslatef(0, 0, VERTICAL_HEIGHT);
				glTranslatef(0, 0, VERTICAL_HEIGHT);
				glRectf(x, y, x + 3.95, y + 3.95)
				glTranslatef(0, 0, -VERTICAL_HEIGHT);

		
		#FRONT BACK
		black = white=GLfloat_3(.19,.19,.39)
		# black=GLfloat_3(.35,.25,.55) 

		# glColor3fv(GLfloat_3(.2,.2,.3))
		
		glRotate( 90, 1,0,0)
		# glTranslatef(0, 0, 20);
		# glRectf(-20, -VERTICAL_HEIGHT, 20, VERTICAL_HEIGHT)
		# glTranslatef(0, 0, -20);
		# glTranslatef(0, 0, -20);
		# glRectf(-20, -VERTICAL_HEIGHT, 20, VERTICAL_HEIGHT)
		# glTranslatef(0, 0, 20);

		for x in range(-N, N, 2):
			for y in range(-4, 4, 2):
				if (x + y) % 4 == 0:
					glColor3fv(white)
				else:
					glColor3fv(black)	
				glTranslatef(0, 0, -N);
				glRectf(x, y, x + 1.95, y + 1.95)
				glTranslatef(0, 0, N);
				glTranslatef(0, 0, N);
				glRectf(x, y, x + 1.95, y + 1.95)
				glTranslatef(0, 0, -N);


		glRotate( -90, 1,0,0)


		#LEFT RIGHT

		# glColor3fv(GLfloat_3(.15,.15,.25))
		# glRotate( 90, 0,1,0)
		# glTranslatef(0, 0, 20);
		# glRectf(-VERTICAL_HEIGHT, -20, VERTICAL_HEIGHT, 20)
		# glTranslatef(0, 0, -20);
		# glTranslatef(0, 0, -20);
		# glRectf(-VERTICAL_HEIGHT, -20, VERTICAL_HEIGHT, 20)
		# glTranslatef(0, 0, 20);



		glRotate( 90, 0,1,0)
		# white=GLfloat_3(.5,.0,.5)
		# black=GLfloat_3(.5,.5,.6) 
		black = white=GLfloat_3(.13,.13,.33)

		for x in range(-4, 4, 2):
			for y in range(-N, N, 2):
				if (x + y) % 4 == 0:
					glColor3fv(white)
				else:
					glColor3fv(black)	
				glTranslatef(0, 0, -N);
				glRectf(x, y, x + 1.95, y + 1.95)
				glTranslatef(0, 0, N);
				glTranslatef(0, 0, N);
				glRectf(x, y, x + 1.95, y + 1.95)
				glTranslatef(0, 0, -N);
		glRotate( -90, 0,1,0)


		# glTranslatef(0, 0, 20);
		# glRectf(-20, -VERTICAL_HEIGHT, 20, VERTICAL_HEIGHT)
		# glTranslatef(0, 0, -20);
		# glTranslatef(0, 0, -20);
		# glRectf(-20, -VERTICAL_HEIGHT, 20, VERTICAL_HEIGHT)
		# glTranslatef(0, 0, 20);



		# glRotate( -90, 1,0,0)







		# for x in range(-N, N):
		#   for y in range(-N, N):
		#       if (x + y) % 2 == 0:
		#           glColor3fv(white)
		#       else:
		#           glColor3fv(black)   
		#       glRectf(x, y, x + 1, y + 1)
	finally:
		# pass
		glEnable(GL_LIGHTING)

mousex = 0
mousey = 0
rrx = 20
rry = 20
ambient = [0.0, 0.0, 1.0, 1.0]
diffuse = [1.0, 1.0, 1.0, 1.0]
specular = [1.0, 1.0, 1.0, 1.0]
position = [0.0, 0.0, 0.0, 1.0]
lmodel_ambient = [0.2, 0.2, 0.2, 0.0]
local_view = [0.0]
# day_since_2000 = celestial.day_number(datetime.datetime.utcnow()) #changes with simulation 
# day_since_2000 = celestial.day_number(datetime.datetime.utcnow() + datetime.timedelta(days = 365.25*10)) #changes with simulation 
day_since_2000 = celestial.day_number(datetime.datetime(2022, 1,1)) #changes with simulation 
# today_since_2000 = day_since_2000 #fixed throughout simulation
user_day_since_2000 = day_since_2000
today_since_2000 = celestial.day_number(datetime.datetime.utcnow()) #fixed throughout simulation
print day_since_2000 - today_since_2000
PAUSED = False
speed = 10
NearAsteroids = celestial.NearAsteroids

def drawHUD():
	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	glLoadIdentity();
	glOrtho(0.0, W, H, 0.0, -1.0, 10.0);
	glMatrixMode(GL_MODELVIEW);
	# //glPushMatrix();        ----Not sure if I need this
	glLoadIdentity();
	glDisable(GL_CULL_FACE);

	glClear(GL_DEPTH_BUFFER_BIT);

	glDisable(GL_LIGHTING)

	glut_print( 32 , 56 , GLUT_BITMAP_8_BY_13 , "1950 A.D.", 0 , .8 , 0.0 , 1.0 , 256)
	glut_print( W - 104, 56 , GLUT_BITMAP_8_BY_13 , "2100 A.D.", 0 , .8 , 0.0 , 1.0 , 5000)
	glut_print( W / 2 - 72, 56 , GLUT_BITMAP_8_BY_13 , "2025 A.D.", 0 , .8 , 0.0 , 1.0 , 5000)




	# glut_print( 1 , H - 12 , GLUT_BITMAP_8_BY_13 , "3D SOLAR SYSTEM VISUALIZATION WITH HEAD TRACKING" , 1.0 , .0 , 0.0 , 1.0 , 1000)
	glut_print( 1 , H - 12 , GLUT_BITMAP_9_BY_15 , "ASTROACT" , 1.0 , .0 , 0.0 , 1.0 , 1000)
	# glut_print( 1 , H - 12 , GLUT_BITMAP_9_BY_15 , "3D SOLAR SYSTEM VISUALIZATION WITH HEAD TRACKING" , 1.0 , .0 , 0.0 , 1.0 , 1000)
	# glut_print( 1 , 1 , GLUT_BITMAP_HELVETICA_12 , "Hello world. AATISH NEUPANE | HILSON SHRESTHA | MANISH GAUTAM | ROHIT SHRESTHA | RITESH JUNG THAPA" , 1.0 , 255.0 , 1.0 , 1.0 )
	glut_print( 81 , H - 12 , GLUT_BITMAP_8_BY_13 , "| HELLO WORLD" , 1.0 , 1.0 , 1.0 , 1.0 , 500)
	glut_print( 1 , H - 500 , GLUT_BITMAP_8_BY_13 , "speed: " + str(speed) , 1.0 , 1.0 , 1.0 , 1.0 , 500)

	cnt = 0
	# print celestial.NearAsteroids
	for asteroid in NearAsteroids:
		glut_print( 1 , H - 48 - 64 * cnt , GLUT_BITMAP_8_BY_13 , asteroid.full_name , .5 , 1.0 , 0.0 , 1.0 , 500)
		glut_print( 1 , H - 48 - 64 * cnt - 16, GLUT_BITMAP_8_BY_13 , str(asteroid.near_date) , 0.0 , 0.5 , 1.0 , 1.0 , 500)
		# glut_print( 1 , H - 48 - 64* cnt - 32, GLUT_BITMAP_8_BY_13 , str(asteroid.distance) + " AU" , 1.0 , 255.0 , 1.0 , 1.0 , 500)
		cnt += 1


	
	# glut_print( 1 , H - 60 , GLUT_BITMAP_8_BY_13 , "SUN: " , .2 , 0.2 , 1.0 , 1.0 , 256)
	# glut_print( 1 , H - 80 , GLUT_BITMAP_8_BY_13 , "MERCURY: " , .2 , 0.2 , 1.0 , 1.0 , 256)
	# glut_print( 1 , H - 100 , GLUT_BITMAP_8_BY_13 , "VENUS: " , .2 , 0.2 , 1.0 , 1.0 , 256)
	# glut_print( 1 , H - 120 , GLUT_BITMAP_8_BY_13 , "EARTH: " , .2 , 0.2 , 1.0 , 1.0 , 256)
	# glut_print( 1 , H - 140 , GLUT_BITMAP_8_BY_13 , "MARS: " , .2 , 0.2 , 1.0 , 1.0 , 256)

	# glut_print( 1 , H - 180 , GLUT_BITMAP_8_BY_13 , "TIME:", .2 , 1.0 , 0.0 , 1.0 , 256)
	full_sim_day = celestial.date_from_today(day_since_2000 - today_since_2000)
	# full_sim_day = celestial.date_from_today(day_since_2000)
	# print day_since_2000 - today_since_2000

	lll = 1.0 * (W - 64) / 150 * (full_sim_day.year - 1950)
	# lll = 500
	# print lll
	# glut_print( 1 , H - 200 , GLUT_BITMAP_8_BY_13 , str(full_sim_day.year) + " " + str(full_sim_day.month) + " " + str(full_sim_day.day) + " " + str(full_sim_day.hour) + "h", .2 , 0.2 , 1.0 , 1.0 , 256)
	glPointSize( 7.0 );
	glBegin( GL_POINTS );
	glColor3fv(GLfloat_3(1,1,1))
	glVertex2f( lll, H - 48 );
	glEnd();
	glPointSize( 1.0 );

	glut_print( lll - 56 , 32 , GLUT_BITMAP_8_BY_13 , str(full_sim_day.year) + " " + str(full_sim_day.month) + " " + str(full_sim_day.day) + " " + str(full_sim_day.hour) + "h", 1.0 , 1.0 , 0.0 , 1.0 , 5000)



	# earth = celestial_objects[3]
	# earth_coordinates = celestial_objects[3].coordinates(day_since_2000)
	# glut_print( 50 , H - 64 , GLUT_BITMAP_8_BY_13 , str(earth_coordinates[0]) , .2 , 0.2 , 1.0 , 1.0 , 300)
	# glut_print( 50 , H -  80, GLUT_BITMAP_8_BY_13 , str(earth_coordinates[1]) , .2 , 0.2 , 1.0 , 1.0 , 300)
	# glut_print( 50 , H - 96 , GLUT_BITMAP_8_BY_13 , str(earth_coordinates[2]) , .2 , 0.2 , 1.0 , 1.0 , 300)




	

	glColor4f(1.0, 1.0, 1.0, .1);

	glBegin(GL_LINES)
	# glVertex3f(start[0], start[1], start[2])
	glVertex2f(257, 0)
	glVertex2f(257, H - 97)
	# glVertex2f(257, H - 9)
	# glVertex2f(390, 20)
	# glVertex2f(W, H-90)
	# glVertex2f(257, H - 96)
	glEnd()
	glBegin(GL_LINES)
	glVertex2f(257, H-96)
	glVertex2f(W, H-96)
	glEnd()

	glColor4f(1.0, 1.0, 1.0, 1);
	glBegin(GL_LINES)
	# glVertex3f(start[0], start[1], start[2])
	glVertex2f(32, H - 48)
	glVertex2f(W - 32, H - 48)
	glEnd()


	glColor4f(1.0, 1.0, 1.0, .05);
	glRectf(0, H - 96, W, H)
	# glColor4f(1.0, 1.0, 1.0, .05);
	glRectf(0, 0, 256, H)
	


	glEnable(GL_LIGHTING)

	# // Making sure we can render 3d again
	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glMatrixMode(GL_MODELVIEW);
	# //glPopMatrix();        ----and this?




class DrawThread(threading.Thread):
	"""docstring for DrawThread"""
	def __init__(self, bodies, day, height, thread_idx, thread_total):
		super(DrawThread, self).__init__()
		self.bodies = bodies
		self.day = day
		self.height = height
		self.thread_idx = thread_idx
		self.thread_total = thread_total

	def run(self):
		b = self.bodies
		for i in range(len(b) * self.thread_idx / self.thread_total, len(b)):
			b[i].draw(self.day, self.height)


import Queue

# q = Queue.Queue()

# my_texture=Texture("EarthMap_2500x1250.jpg")




celestial_objects = [
	celestial.sun,
	celestial.mercury,
	celestial.venus,
	celestial.earth,
	# celestial.moon,
	celestial.mars,
	celestial.jupiter,
	celestial.saturn,
	celestial.uranus,
	celestial.neptune,
	celestial.pluto
]

celestial_objects += celestial.asteroids


# turn = 0
# total_celestial = len(celestial_objects)

def display( swap=1, clear=1):
	"""Callback function for displaying the scene

	This defines a unit-square environment in which to draw,
	i.e. width is one drawing unit, as is height
	"""
	if clear:
		glClearColor(.02, .02, .03, 0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# establish the projection matrix (perspective)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	x,y,width,height = glGetDoublev(GL_VIEWPORT)
	gluPerspective(
		45, # field of view in degrees
		width/float(height or 1), # aspect ratio
		.25, # near clipping plane
		100, # far clipping plane
	)



	# and then the model view matrix
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()


	global mousex, mousey, day_since_2000, starttime, today_since_2000, turn
	# glDisable(GL_LIGHTING)

	# day_since_2000 = today_since_2000 + (time.time() - starttime) * 1
	if not PAUSED: day_since_2000 = user_day_since_2000 + (time.time() - starttime) * speed
	# print day_since_2000
	# day_since_2000 = 40526 + (time.time() - starttime) * 1

	# day_since_2000 = celestial.day_number(datetime.datetime.utcnow())
	earth_coordinates = celestial_objects[0].coordinates(day_since_2000)

	gluLookAt(
		0, 15.0-EYE['y']/3.0,0, # eyepoint
		# 0, 15.0-EYE['y']/3.0,EYE['x'], # eyepoint
		# earth_coordinates[0] - 5, earth_coordinates[1] - 5, earth_coordinates[2], # eyepoint
		# 0, .1,20, # eyepoint
		# mousex,20-mousey,15, # eyepoint
		earth_coordinates[0], earth_coordinates[1], earth_coordinates[2], # center-of-view
		# 0, 0, 0, # center-of-view
		0, 0, 1, # up-vector
	)


	modelTwoside = [GL_TRUE]
	glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, modelTwoside)
	glFrontFace(GL_CW)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_AUTO_NORMAL)
	glEnable(GL_NORMALIZE)
	glEnable(GL_DEPTH_TEST) 
	
	rotation()
	# drawCheckerBoard()


	glLightfv(GL_LIGHT0, GL_POSITION, position)

	# glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
	glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, local_view)
	
	for body in celestial_objects:
		body.draw(day_since_2000, VERTICAL_HEIGHT)



	glEnable(GL_TEXTURE_2D)
	# glRotate( 45, 0, .1, 0)
	glRotate( 45, 1, 1, 1)

	# glClearColor(0.2, 0.5, 1.0, 1.0)    # This Will Clear The Background Color To Black
	# glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
	# glClearStencil(0)



	glColor3f(1.0, 1.0, 1.0);
	# glBindTexture( GL_TEXTURE_2D, LoadTextures('NeHe.bmp') )
	# glBindTexture( GL_TEXTURE_2D, LoadTextures('EarthMap_2500x1250.jpg') )
	# glBindTexture( GL_TEXTURE_2D, LoadTextures('eso_dark.jpg') )
	glBindTexture( GL_TEXTURE_2D, LoadTextures('nightsky360.jpg') )

	Q=gluNewQuadric()
	gluQuadricNormals(Q, GL_SMOOTH)
	gluQuadricTexture(Q, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

	gluSphere(Q, 30.35, 32, 16)

	# # glColor4f(1.0, 1.0, 1.0, 0.4)
	# glEnable(GL_BLEND)
	# glBlendFunc(GL_SRC_ALPHA, GL_ONE)
	# glEnable(GL_TEXTURE_GEN_S)
	# glEnable(GL_TEXTURE_GEN_T)
	# gluSphere(Q, 0.35, 32, 16)

	glDisable(GL_TEXTURE_GEN_S)
	glDisable(GL_TEXTURE_GEN_T)
	# glDisable(GL_BLEND)
	gluDeleteQuadric( Q )

	glDisable(GL_TEXTURE_2D)





	# q = Queue.Queue()


	# threads = []
	# thread1 = DrawThread(celestial_objects, day_since_2000, VERTICAL_HEIGHT, 0, 4)
	# thread2 = DrawThread(celestial_objects, day_since_2000, VERTICAL_HEIGHT, 1, 4)
	# # thread3 = DrawThread(celestial_objects, day_since_2000, VERTICAL_HEIGHT, 2, 4)
	# # thread4 = DrawThread(celestial_objects, day_since_2000, VERTICAL_HEIGHT, 3, 4)

	# thread1.start()
	# thread2.start()
	# # thread3.start()
	# # thread4.start()
	# thread1.join()
	# thread2.join()
	# thread3.join()
	# thread4.join()
	# for body in celestial_objects:
	# 	body.draw(day_since_2000, VERTICAL_HEIGHT)
	# 	thread = DrawThread(body, day_since_2000, VERTICAL_HEIGHT)
	# 	threads.append(thread)
	# 	thread.start()

	# for thread in threads:
	# 	thread.join()
	# thread1.run()
	# thread2 = FaceThread()    
	# thread1.start()
	# thread2.start()
	# thread1.join()  
	# thread2.join()  


	drawHUD()



	if swap:
		glutSwapBuffers()
	# time.sleep(.016)



def glut_print( x,  y,  font,  text, r,  g , b , a, width = 1000):
	# width = 1000
	# global first, width
	# print glutGet(GLUT_WINDOW_WIDTH)
	blending = False 
	if glIsEnabled(GL_BLEND) :
		blending = True
	x_new = x
	#glEnable(GL_BLEND)
	glColor3f(r,g,b)#color controlled by this
	# glTranslatef(0.0, 0.0, -5.0)
	glWindowPos2f(x,y)#this is to create position in screen.
	for ch in text :
		x_new = x_new + 10
		if x_new > width-60:
			y = y - 15
			glWindowPos2f(x,y)
			x_new = x
		glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )
		# if (first):
		#     glutSwapBuffers()                                  # important for double buffering
		#     time.sleep(0.1)
		

	if not blending :
		glDisable(GL_BLEND)
	# first = False 
	# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
	# glEnable(GL_BLEND)
	# pygame.init()
	# pygame.font.init()
	# myfont = pygame.font.SysFont("monospace", 15)

	# # render text
	# label = myfont.render("Some text!", 1, (255,255,0))
	# # screen.blit(label, (100, 100))


def idle( ):
	# pass
	glutPostRedisplay()

starttime = time.time()
pausedtime = starttime


def rotation( period = 25):
	"""Do rotation of the scene at given rate"""
	# angle = (((time.time()-starttime)%period)/period)* 360
	# glRotate( angle, 0,0,1)
	# glRotate( 0, 0, 0, 0)

	if video_enabled:
		glRotate( pow(pow(FACECENTER['x'], 2) + pow(FACECENTER['y'], 2), 0.5) * 10, FACECENTER['y'], 0, FACECENTER['x'])
	else:
		glRotate( pow(pow(mousex, 2) + pow(mousey, 2), 0.5) * 2, mousey, 0, -mousex)

	# glTranslatef(-mousex, 0, mousey)
	A_FACECENTER.update()
	A_EYE.update()
	# glTranslatef(-FACECENTER['x'], 0, FACECENTER['y'])
	return angle


def key_pressed(*args):
	# If escape is pressed, kill everything.
	if args[0] == '\033':
		sys.exit()
	elif args[0] == "=":
		if EYE['y'] < 37:
			A_EYE.animate({'y':EYE['y'] + 5}, .1)
		else:
			EYE['y'] = 37
		# EYE['y'] -= 1
		# print EYE['y']
	elif args[0] == "-":
		A_EYE.animate({'y':EYE['y'] - 5}, .1)
		# EYE['y'] += 1
	elif args[0] == 'p':

		global PAUSED, pausedtime, starttime
		if PAUSED:
			starttime += (time.time() - pausedtime)
			# print starttime
		else:
			pausedtime = time.time()

		PAUSED = not PAUSED

	elif args[0] == "l":
		global day_since_2000, user_day_since_2000, starttime
		# day_since_2000 = celestial.day_number(datetime.datetime(2012, 6,15)) #changes with simulation 
		day_since_2000 += 100 #changes with simulation 
		# today_since_2000 = day_since_2000 #fixed throughout simulation
		user_day_since_2000 = day_since_2000
		starttime = time.time()

	# print args
		# print EYE['y']


def mouse_handler( x, y ):
	global mousex, mousey
	# w = glutGet(GLUT_WINDOW_WIDTH)
	# w = 1386
	# h = glutGet(GLUT_WINDOW_HEIGHT)
	mousex = .12 * (-W/2 + x)
	mousey = .12 * (-H/2 + y)
	# print mousex, mousey
	return None

class GlutThread(threading.Thread):
	 def __init__(self):
		 super(GlutThread, self).__init__()

	 def run(self):
		glutInit(sys.argv);
		glutInitWindowSize(1000, 600);
		glutInitWindowPosition(50,50);
		glutCreateWindow(sys.argv[0]);
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

		glutDisplayFunc(display)
		glutPassiveMotionFunc(mouse_handler)
		# glutMotionFunc(mouse_handler)
		glutKeyboardFunc(key_pressed)
		glutIdleFunc(display)
		# note need to do this to properly render faceted geometry


		# glEnable( GL_DEPTH_TEST )
		# print glutGet(GLUT_SCREEN_WIDTH)
		# time.sleep(1)
		# glutMainLoop()
		# glutMainLoopUpdate()
		glutFullScreen()
		global W, H
		# W = glutGet(GLUT_WINDOW_WIDTH)
		W = glutGet(GLUT_SCREEN_WIDTH)
		H = glutGet(GLUT_SCREEN_HEIGHT)
		print W, H
		# glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)



		glutMainLoop()
		 # for i in range(self.low,self.high):
			 # self.total+=i




class FaceThread(threading.Thread):
	"""docstring for FaceThread"""
	def __init__(self):
		super(FaceThread, self).__init__()

	def run(self):
		import sys, getopt
		global mousex, mousey, A_FACECENTER
		args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
		try:
			video_src = video_src[0]
		except:
			video_src = 0
		args = dict(args)
		cascade_fn = args.get('--cascade', "../../data/haarcascades/haarcascade_frontalface_alt.xml")
		# cascade_fn = args.get('--cascade', "../../data/haarcascades/haarcascade_upperbody.xml")
		# nested_fn  = args.get('--nested-cascade', "../../data/haarcascades/haarcascade_eye.xml")

		cascade = cv2.CascadeClassifier(cascade_fn)
		# nested = cv2.CascadeClassifier(nested_fn)

		cam = create_capture(video_src, fallback='synth:bg=../data/lena.jpg:noise=0.05')

		while True:
			ret, img = cam.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			gray = cv2.equalizeHist(gray)

			t = clock()
			rects = detect(gray, cascade)
			for rect in rects:
				# mousex = .1 * ((rect[0] + rect[2]) * .5 -320)
				# mousey = .1 * ((rect[1] + rect[3]) * .5 - 240)
				A_FACECENTER.animate({
					'x': .02 * ((rect[0] + rect[2]) * .5 -320),
					'y': .02 * ((rect[1] + rect[3]) * .5 - 240)
				}, .5)

				A_EYE.animate({'y':-10 - (rect[0] - rect[2])/10}, .5)
				break

			# vis = img.copy()
			# draw_rects(vis, rects, (0, 255, 0))
			# draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
			# cv2.imshow('facedetect', vis)

			if 0xFF & cv2.waitKey(5) == 27:
				break
			time.sleep(.1)


		cv2.destroyAllWindows()

import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

class SampleListener(Leap.Listener):
	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
	def on_frame(self, controller):
		global speed
		frame = controller.frame();
		gestures = frame.gestures();
		for gesture in frame.gestures():
			if gesture.state is Leap.Gesture.STATE_UPDATE and gesture.type is Leap.Gesture.TYPE_CIRCLE:
				circle = Leap.CircleGesture(gesture)
				if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
					speed = speed + 0.05
					# print "increase"
				else:
					# if not speed <= 0:
					# print "decrease"
					speed = speed - 0.05
				# print speed
			if gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
				key_pressed('p',)


if __name__ == '__main__':
	controller = Leap.Controller()
	listener = SampleListener()
	controller.add_listener(listener)

	thread1 = GlutThread()
	thread2 = FaceThread()    
	if video_enabled:
		thread1.start()
		thread2.start()
		thread1.join()  
		thread2.join()  
	else:
		thread1.run()


	# Remove the sample listener when done
	controller.remove_listener(listener)

