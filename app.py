#!/usr/bin/env python
# -*- coding: utf8 -*-

import threading
from PIL.Image import open
import cv2
from Image import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import datetime, time, sys, gc 

# local modules for opencv
from video import create_capture
from common import clock, draw_str

# local modules for celestial
import celestial
# import celestial_smooth as celestial
from animator import Animator

try:
	from numpy import *
except ImportError, err:
	try: 
		from Numeric import *
	except ImportError, err:
		print "This demo requires the numpy or Numeric extension, sorry"
		import sys
		sys.exit()

# set this to true if face detection is needed.
video_enabled = True

# dictionary of textures used.
textures = {}

# screen width and height.
W = H = 0

# Coordinates of human face detected by opencv.
FACECENTER = {
	'x': 0,
	'y': 0
}

# Coordinates of camera.
EYE = {
	'x': 0,
	'y': 10,
	'z': 0
}

# smooth variable animator 
A_FACECENTER = Animator(FACECENTER)
A_EYE = Animator(EYE)

# mouse coordinates
mousex = mousey = 0

# variables for light
ambient = [0.0, 0.0, 1.0, 1.0]
diffuse = [1.0, 1.0, 1.0, 1.0]
specular = [1.0, 1.0, 1.0, 1.0]
position = [0.0, 0.0, 0.0, 1.0]
lmodel_ambient = [0.2, 0.2, 0.2, 0.0]
local_view = [0.0]


# animation start time and paused time.
starttime = time.time()
pausedtime = starttime

# day variables

# day of simulation
day_since_2000 = celestial.day_number(datetime.datetime.utcnow()) #changes with simulation 
# day_since_2000 = celestial.day_number(datetime.datetime(2022, 1,15)) #changes with simulation 
# day_since_2000 = celestial.day_number(datetime.datetime(2023, 1,29)) #changes with simulation 

# simulation start day
user_day_since_2000 = day_since_2000

# actual present day
# remains fixed throughout simulation
today_since_2000 = celestial.day_number(datetime.datetime.utcnow())

# flag for simulation play or paused.
PAUSED = False

# animation speed
speed = .4

# PHA that near earth calculated during simulation.
NearAsteroids = celestial.NearAsteroids

# List of celestial objects to draw.
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

# append list of potentially hazardous asteroids.
celestial_objects += celestial.asteroids

def LoadTextures(fname):
	'''Loads the image file fname and creates its texture'''
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
	'''returns rectangle coordinates of cascade in img'''
	rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
	if len(rects) == 0:
		return []
	rects[:,2:] += rects[:,:2]
	return rects

def drawHUD():
	'''Displays screen HUD'''
	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	glLoadIdentity();
	glOrtho(0.0, W, H, 0.0, -1.0, 10.0);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glDisable(GL_CULL_FACE);
	glClear(GL_DEPTH_BUFFER_BIT);
	glDisable(GL_LIGHTING)

	# Timeline
	glut_print( 32 , 56 , GLUT_BITMAP_8_BY_13 , "1950 A.D.", 0 , .8 , 0.0 , 1.0 , 256)
	glut_print( W - 104, 56 , GLUT_BITMAP_8_BY_13 , "2100 A.D.", 0 , .8 , 0.0 , 1.0 , 5000)
	glut_print( W / 2 - 72, 56 , GLUT_BITMAP_8_BY_13 , "2025 A.D.", 0 , .8 , 0.0 , 1.0 , 5000)

	# App Title
	glut_print( 32 , H - 16 , GLUT_BITMAP_9_BY_15 , "ASTROACT" , 1.0 , 1.0 , 0.0 , 1.0 , 1000)
	glut_print( 113 , H - 16 , GLUT_BITMAP_9_BY_15 , "| Hello World" , 1.0 , .0 , .0 , 1.0 , 500)
	glut_print( 32 , 128 , GLUT_BITMAP_8_BY_13 , "speed: " + str(speed) , 1.0 , 1.0 , 1.0 , 1.0 , 500)

	cnt = 0

	# print asteroids details.
	# asteroid name, time and distance when nearest with earth.
	for asteroid in NearAsteroids:
		if asteroid.distance < 1: # for error correction. TODO: need verify error here.
			glut_print( 1 , H - 48 - 64 * cnt , GLUT_BITMAP_8_BY_13 , asteroid.full_name , .5 , 1.0 , 0.0 , 1.0 , 500)
			glut_print( 1 , H - 48 - 64 * cnt - 16, GLUT_BITMAP_8_BY_13 , str(asteroid.near_date) , 0.0 , 0.5 , 1.0 , 1.0 , 500)
			glut_print( 1 , H - 48 - 64 * cnt - 32, GLUT_BITMAP_8_BY_13 , str(asteroid.distance) + " AU" , 1.0 , 255.0 , 1.0 , 1.0 , 500)
			cnt += 1

	full_sim_day = celestial.date_from_today(day_since_2000 - today_since_2000)
	leftx = 1.0 * (W - 64) / 150 * (full_sim_day.year - 1950)
	glPointSize( 7.0 );
	glBegin( GL_POINTS );
	glColor3fv(GLfloat_3(1,1,1))
	glVertex2f( leftx, H - 48 );
	glEnd();
	glPointSize( 1.0 );
	# print simulation date.
	glut_print( leftx - 56 , 32 , GLUT_BITMAP_8_BY_13 , str(full_sim_day.year) + " " + str(full_sim_day.month) + " " + str(full_sim_day.day) + " " + str(full_sim_day.hour) + "h", 1.0 , 1.0 , 0.0 , 1.0 , 5000)

	glColor4f(1.0, 1.0, 1.0, .1);
	glBegin(GL_LINES)
	glVertex2f(257, 0)
	glVertex2f(257, H - 97)
	glEnd()
	glBegin(GL_LINES)
	glVertex2f(257, H-96)
	glVertex2f(W, H-96)
	glEnd()

	glColor4f(1.0, 1.0, 1.0, 1);
	glBegin(GL_LINES)
	glVertex2f(32, H - 48)
	glVertex2f(W - 32, H - 48)
	glEnd()

	glColor4f(1.0, 1.0, 1.0, .05);
	glRectf(0, H - 96, W, H)
	glRectf(0, 0, 256, H)
	glEnable(GL_LIGHTING)

	# Making sure we can render 3d again
	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glMatrixMode(GL_MODELVIEW);

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

	if not PAUSED: day_since_2000 = user_day_since_2000 + (time.time() - starttime) * speed

	#TODO: change celestial object based on user's preference.
	celestial_coordinates = celestial_objects[0].coordinates(day_since_2000) 

	gluLookAt(
		0, 15.0-EYE['y']/3.0,0, # eyepoint
		celestial_coordinates[0], celestial_coordinates[1], celestial_coordinates[2], # center-of-view
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

	glLightfv(GL_LIGHT0, GL_POSITION, position)

	# glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
	glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, local_view)
	
	# draw all celestial objects.
	for body in celestial_objects:
		body.draw(day_since_2000)

	glEnable(GL_TEXTURE_2D)
	glRotate( 45, 0, 1, 0)
	# glRotate( 45, 1, 1, 1)

	glColor3f(1.0, 1.0, 1.0);

	# background milkyway galaxy sphere.
	# we are actually inside this sphere.
	glBindTexture( GL_TEXTURE_2D, LoadTextures('nightsky360.jpg') )
	Q=gluNewQuadric()
	gluQuadricNormals(Q, GL_SMOOTH)
	gluQuadricTexture(Q, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	gluSphere(Q, 80, 32, 16)

	glDisable(GL_TEXTURE_GEN_S)
	glDisable(GL_TEXTURE_GEN_T)
	gluDeleteQuadric( Q )
	glDisable(GL_TEXTURE_2D)

	drawHUD()
	if swap:
		glutSwapBuffers()

def glut_print( x,  y,  font,  text, r,  g , b , a, width = 1000):
	blending = False 
	if glIsEnabled(GL_BLEND) :
		blending = True
	x_new = x
	# glEnable(GL_BLEND)
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

	if not blending :
		glDisable(GL_BLEND)

def idle( ):
	glutPostRedisplay()

def rotation( period = 25):
	"""Do rotation of the scene based on face coordinates or mouse coordinates."""
	if video_enabled:
		glRotate( pow(pow(FACECENTER['x'], 2) + pow(FACECENTER['y'], 2), 0.5) * 10, FACECENTER['y'], 0, FACECENTER['x'])
	else:
		glRotate( pow(pow(mousex, 2) + pow(mousey, 2), 0.5) * 2, mousey, 0, -mousex)
	A_FACECENTER.update()
	A_EYE.update()

def key_pressed(*args):
	global day_since_2000, user_day_since_2000, starttime, PAUSED, pausedtime, speed
	# If escape is pressed, kill everything.
	if args[0] == '\033':
		sys.exit()

	# zoom feature
	elif args[0] == "=":
		if EYE['y'] < 37:
			EYE['y'] += .1
			# A_EYE.animate({'y':EYE['y'] + 5}, .1)
		else:
			EYE['y'] = 37
	elif args[0] == "-":
		EYE['y']-= .1
		# A_EYE.animate({'y':EYE['y'] - 5}, .1)

	elif args[0] == 'p':
		if PAUSED:
			starttime += (time.time() - pausedtime)
		else:
			pausedtime = time.time()
		PAUSED = not PAUSED

	# Time Travel
	elif args[0] == ".":
		day_since_2000 += 30 # go forward in time ## TIME TRAVEL!!!
		user_day_since_2000 = day_since_2000
		starttime = time.time()
	elif args[0] == ",":
		day_since_2000 -= 30 # go back in time 
		user_day_since_2000 = day_since_2000
		starttime = time.time()

	# speed manipulation 
	elif args[0] == "]":
		speed += .1
	elif args[0] == "[":
		speed -= .1


def mouse_handler( x, y ):
	global mousex, mousey
	mousex = .12 * (-W/2 + x)
	mousey = .12 * (-H/2 + y)

class GlutThread(threading.Thread):
	 def __init__(self):
		 super(GlutThread, self).__init__()

	 def run(self):
		glutInit(sys.argv);
		glutInitWindowSize(1280, 720);
		glutInitWindowPosition(50,50);
		glutCreateWindow(sys.argv[0]);
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
		glutDisplayFunc(display)
		glutPassiveMotionFunc(mouse_handler)
		# glutMotionFunc(mouse_handler)
		glutKeyboardFunc(key_pressed)
		glutIdleFunc(display)
		glutFullScreen()
		global W, H
		# W = glutGet(GLUT_WINDOW_WIDTH)
		W = glutGet(GLUT_SCREEN_WIDTH)
		H = glutGet(GLUT_SCREEN_HEIGHT)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		glutMainLoop()

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


# LEAP MOTION 
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
				else:
					speed = speed - 0.05
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
