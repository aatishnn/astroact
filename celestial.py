'''
celestial.py
April 7, 2015
HELLO WORLD IT SOLUTION


REFERENCES:

Celestial class based on: 
http://www.stjarnhimlen.se/comp/tutorial.html

Earth, Moon and Pluto based on astronomy.js by Don Cross
http://cosinekitty.com/astronomy.js

Kelperian Elements for Approximate positions of major planets:
http://ssd.jpl.nasa.gov/txt/aprx_pos_planets.pdf

http://en.wikipedia.org/wiki/Kepler_orbit

http://en.wikipedia.org/wiki/Orbital_elements
'''

import datetime
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import json

factor = 1




def drawSphere( center=(0,0,0), radius=.5, sides=15 ):
	glPushMatrix()
	glTranslatef(*center)
	try:
		mat = [0, 0, 0, 0]

		# ambr = 0.0215
		# ambg = 0.1745
		# ambb = 0.0215
		ambr = 0.001
		ambg = 0.001
		ambb = 0.001

		# difr = 0.07568
		# difg =  0.61424
		# difb = 0.07568
		difr = 0.77568
		difg =  0.861424
		difb = 0.97568

		# specr = 0.633
		# specg = 0.727811
		# specb =  0.633
		specr = 0.9633
		specg = 0.97811
		specb =  0.5633
		shine =  .2

		mat[0] = ambr; mat[1] = ambg; mat[2] = ambb; mat[3] = 1.0
		glMaterialfv(GL_FRONT, GL_AMBIENT, mat)
		mat[0] = difr; mat[1] = difg; mat[2] = difb
		glMaterialfv(GL_FRONT, GL_DIFFUSE, mat)
		mat[0] = specr; mat[1] = specg; mat[2] = specb
		glMaterialfv(GL_FRONT, GL_SPECULAR, mat)
		glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0)


		glutSolidSphere(radius, sides, sides)
	finally:
		glPopMatrix()

class Celestial(object):
	def __init__(self, N1 = 0, N2 = 0, I1 = 0, I2 = 0, W1 = 0, W2 = 0, A1 = 0, A2 = 0, E01 = 0, E02 = 0, M1 = 0, M2 = 0, radius = .04):
		self.N1 = N1
		self.N2 = N2
		self.I1 = I1
		self.I2 = I2
		self.W1 = W1
		self.W2 = W2
		self.A1 = A1
		self.A2 = A2
		self.E01 = E01
		self.E02 = E02
		self.M1 = M1
		self.M2 = M2

		self.radius = radius
	
	def rev(self, degree):
		# Corrects degree 360.
		return degree % 360
		# return degree

	def N(self, d):
		# Longitude of ascending node
		return self.rev(self.N1 + self.N2 * d)
	
	def i(self, d):
		# Inclination
		return self.rev(self.I1 + self.I2 * d)
	
	def w(self, d):
		# Argument of perihelion
		return self.rev(self.W1 + self.W2 * d)
	
	def a(self, d):
		# Mean distance, or semi-major axis
		return self.A1 + self.A2 * d

	def e(self, d):
		# Eccentricity
		return self.rev(self.E01 + self.E02 * d)

	def M(self, d):
		# Mean anomaly
		return self.rev(self.M1 + self.M2 * d)

	def P(self):
		# TODO: add mass of each planet.
		# Orbital Period in days
		# m = mass of planet in solar masses
		m = 0
		return 365.256898326 * self.a() ** 1.5/sqrt (1 + m)

	def n(self):
		# Daily motion @degrees/day
		return 360 / self.P()

	def E(self, M, e):
		# Eccentric anomaly
		# M = self.M(d)
		# e = self.e(d)

		E0 = M + (180.0 / math.pi) * e * math.sin(M * math.pi / 180) * (1 + e * math.cos(M * math.pi / 180))
		d = 1
		while d > .005:
			E1 = E0 - (E0 - (180.0 / math.pi) * e * math.sin(E0 * math.pi / 180) - M) / (1 - e * math.cos(E0 * math.pi / 180))
			d = abs(E0 - E1)
			E0 = E1
		return E0


	def coordinates(self, d):
		
		M = self.M(d)
		e = self.e(d)
		E = self.E(M, e)
		a = self.a(d)
		i = self.i(d)
		N = self.N(d)
		w = self.w(d)

		# Rectangular coordinates (x, y) in the plane of the object's orbit.
		x = a * (math.cos(math.radians(E)) - e)
		y = a * pow(1 - e * e, .5) * math.sin(math.radians(E))


		# Conversion to distance and true anomaly.
		r = pow(x * x + y * y, .5)
		v = self.rev(math.degrees(math.atan2(y, x)))
		v_r = math.radians(v) #radians

		# position in ecliptic coordinates.
		v_plus_w_rad = v_r + math.radians(w) # radians
		N_rad = math.radians(N)
		i_rad = math.radians(i)

		xeclip = r * (math.cos(N_rad) * math.cos(v_plus_w_rad) - math.sin(N_rad) * math.sin(v_plus_w_rad) * math.cos(i_rad) )
		yeclip = r * (math.sin(N_rad) * math.cos(v_plus_w_rad) + math.cos(N_rad) * math.sin(v_plus_w_rad) * math.cos(i_rad))
		zeclip = r * math.sin(v_plus_w_rad) * math.sin(i_rad)
		return xeclip * factor, yeclip * factor, zeclip * factor


	def draw( self, day ):
		center = self.coordinates(day)
		radius = self.radius
		sides = 15
		glPushMatrix()
		glTranslatef(*center)
		try:
			mat = [0, 0, 0, 0]

			ambr = 0.001
			ambg = 0.001
			ambb = 0.001

			difr = 0.77568
			difg =  0.861424
			difb = 0.97568

			specr = 0.9633
			specg = 0.97811
			specb =  0.5633
			shine =  .2

			mat[0] = ambr; mat[1] = ambg; mat[2] = ambb; mat[3] = 1.0
			glMaterialfv(GL_FRONT, GL_AMBIENT, mat)
			mat[0] = difr; mat[1] = difg; mat[2] = difb
			glMaterialfv(GL_FRONT, GL_DIFFUSE, mat)
			mat[0] = specr; mat[1] = specg; mat[2] = specb
			glMaterialfv(GL_FRONT, GL_SPECULAR, mat)
			glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0)


			glutSolidSphere(radius, sides, sides)
		finally:
			glPopMatrix()


class Sun(Celestial):
	def draw(self, day):
		center = (0, 0)
		radius = .1
		sides = 15
		glDisable(GL_LIGHTING)
		glColor3fv(GLfloat_3(1,1,.5))
		glEnable(GL_BLEND); #Enable blending.
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); #Set blending function.
		# drawSphere(center=(0, 0, 0), radius=.1)

		glColor4fv(GLfloat_4(1,1,.5, .8))

		glutSolidSphere(radius, 25, 25)


		glColor3fv(GLfloat_3(.91,.91,.45))

		glColor4fv(GLfloat_4(0,0,0, .15))
		# glutSolidSphere(.15, 25, 25)
		glutWireSphere(radius + .01, 25, 25)
		glColor4fv(GLfloat_4(.9,.9,.45, .55))

		glutWireSphere(radius + .02, 25, 25)

		glEnable(GL_LIGHTING)


class Earth(Celestial):
	# based on http://cosinekitty.com/astronomy.js   ->  EarthClass

	def coordinates(self, d):
		# These formulas use 'd' based on days since 1/Jan/2000 12:00 UTC ("J2000.0"), instead of 0/Jan/2000 0:00 UTC ("day value").
		# Correct by subtracting 1.5 days...
		d = d - 1.5
		T = d / 36525.0

		# Sun's mean longitude, in degrees
		L0 = 280.46645 + (36000.76983 * T) + (0.0003032 * T * T)

		# Sun's mean anomaly, in degrees
		M0 = 357.52910 + (35999.05030 * T) - (0.0001559 * T * T) - (0.00000048 * T * T * T);  

		# Sun's equation of center in degrees
		C = (1.914600 - 0.004817 * T - 0.000014 * T * T) * math.sin(math.radians(M0)) + (0.01993 - 0.000101 * T) * math.sin(math.radians(2 * M0)) + 0.000290 * math.sin(math.radians(3 * M0))

		# true ecliptical longitude of Sun
		LS = L0 + C 

		# The eccentricity of the Earth's orbit.
		e = 0.016708617 - T * (0.000042037 + (0.0000001236 * T));

		# distance from Sun to Earth in astronomical units (AU)
		distanceInAU = (1.000001018 * (1 - e * e)) / (1 + e * math.cos(math.radians(M0 + C)))
		x = -distanceInAU * math.cos(math.radians(LS));
		y = -distanceInAU * math.sin(math.radians(LS));
		# the Earth's center is always on the plane of the ecliptic (z=0), by definition!
		return x * factor, y * factor, 0



class Pluto(Celestial):
	def coordinates(self, day):
		S  =   50.03  +  (0.033459652 * day);
		P  =  238.95  +  (0.003968789 * day);

		def SinDeg(x):
			return math.sin(math.radians(x))

		def CosDeg(x):
			return math.cos(math.radians(x))

		lonecl = (238.9508  +  (0.00400703 * day) - 
			19.799 * SinDeg(  P)  + 19.848 * CosDeg(  P) +
			0.897 * SinDeg(2*P)  -  4.956 * CosDeg(2*P) +
			0.610 * SinDeg(3*P)  +  1.211 * CosDeg(3*P) -
			0.341 * SinDeg(4*P)  -  0.190 * CosDeg(4*P) +
			0.128 * SinDeg(5*P)  -  0.034 * CosDeg(5*P) -
			0.038 * SinDeg(6*P)  +  0.031 * CosDeg(6*P) +
			0.020 * SinDeg(S-P)  -  0.010 * CosDeg(S-P))

		latecl =  (-3.9082 -
			5.453 * SinDeg(  P)   - 14.975 * CosDeg(  P) +
			3.527 * SinDeg(2*P)   +  1.673 * CosDeg(2*P) -
			1.051 * SinDeg(3*P)   +  0.328 * CosDeg(3*P) +
			0.179 * SinDeg(4*P)   -  0.292 * CosDeg(4*P) +
			0.019 * SinDeg(5*P)   +  0.100 * CosDeg(5*P) -
			0.031 * SinDeg(6*P)   -  0.026 * CosDeg(6*P) +
			0.011 * CosDeg(S-P))
		
		r =  (40.72 +
			6.68 * SinDeg(  P)   + 6.90 * CosDeg(  P) -
			1.18 * SinDeg(2*P)   - 0.03 * CosDeg(2*P) +
			0.15 * SinDeg(3*P)   - 0.14 * CosDeg(3*P))

		coslon = CosDeg (lonecl)
		sinlon = SinDeg (lonecl)
		coslat = CosDeg (latecl)
		sinlat = SinDeg (latecl)

		xp = r * coslon * coslat
		yp = r * sinlon * coslat
		zp = r * sinlat

		return xp * factor, yp * factor, zp * factor
		# return new CartesianCoordinates (xp, yp, zp);      // the Earth's center is always on the plane of the ecliptic (z=0), by definition!


def day_number(date):
	# Day value since Jan 1, 2000 00:00:00 UTC 
	return (367 * date.year - (7 * (date.year + ((date.month + 9) / 12))) / 4 + (275 * date.month) / 9 + date.day - 730530) + (1.0 * date.hour / 24 + 1.0 * date.minute / (24 * 60) + 1.0 * date.second / (24 * 60 * 60))

def date_from_today(days):
	return datetime.datetime.now() + datetime.timedelta(days = days)

sun = Sun()

mercury = Celestial(48.3313, 3.24587E-5,
	7.0047, 5.00E-8,
	29.1241, 1.01444E-5,
	0.387098, 0,
	0.205635, 5.59E-10,
	168.6562, 4.0923344368)

venus = Celestial(
	76.6799, 2.46590E-5,
	3.3946, 2.75E-8,
	54.8910, 1.38374E-5,
	0.723330, 0,
	0.006773, - 1.302E-9,
	48.0052, 1.6021302244
	)

earth = Earth()

moon = Celestial(
	125.1228, -0.0529538083,
	5.1454, 0,
	318.0634, 0.1643573223,
	60.2666 / 23454.779920164812, 0,
	0.054900, 0,
	115.3654, 13.0649929509)

mars = Celestial(
	49.5574, 2.11081E-5,
	1.8497, -1.78E-8,
	286.5016, 2.92961E-5,
	1.523688, 0,
	0.093405, 2.516E-9,
	18.6021, 0.5240207766, .1)

jupiter = Celestial(
	100.4542, 2.76854E-5,
	1.3030, -1.557E-7,
	273.8777, 1.64505E-5,
	5.20256, 0,
	0.048498, 4.469E-9,
	19.8950, 0.0830853001, .2)

saturn = Celestial(
	113.6634, 2.38980E-5,
	2.4886, -1.081E-7,
	339.3939, 2.97661E-5,
	9.55475, 0,
	0.055546, -9.499E-9,
	316.9670, 0.0334442282, .2)

uranus = Celestial(
	74.0005, 1.3978E-5,
	0.7733, 1.9E-8,
	96.6612, 3.0565E-5,
	19.18171, -1.55E-8,
	0.047318, 7.45E-9,
	142.5905, 0.011725806
)

neptune = Celestial(
	131.7806, 3.0173E-5,
	1.7700, -2.55E-7,
	272.8461, 6.027E-6,
	30.05826, 3.313E-8,
	0.008606, 2.15E-9,
	260.2471, 0.005995147
	)

pluto = Pluto()


NearAsteroids = []

class Asteroid(Celestial):
	"""docstring for Asteroid"""
	# def __init__(self, epochJD, Nx, i, w, a, e, Mx, T, amag):
	def __init__(self, epochJD, Nx, i, w, a, e, Mx, T, radius, full_name):
		# convert Julian Date to "0.0 January 2000" standard epoch day value.
		day = epochJD - 2451543.5 

		# "mean motion": how many degrees per day the body orbits around the Sun, on average.
		Mc = 360.0 / T

		# work backwards to figure out mean anomoly at standard epoch.
		M0 = (Mx - Mc * day) % 360

		N0 = Nx
		Nc = 0.0

		self.full_name = full_name
		self.distance = 9999999
		super(Asteroid, self).__init__(N0, Nc, i, 0.0, w, 0, a, 0, e, 0, M0, Mc, radius)
		# self.radius = .01
		# self.arg = arg

	def draw( self, day ):
	# def draw( self, center=(0,0,0), radius=.5, sides=15 ):
		center = self.coordinates(day)
		radius = self.radius
		sides = 15
		glPushMatrix()
		glTranslatef(*center)
		glDisable(GL_LIGHTING)
		try:
			# glPointSize( 2.0 );
			glBegin( GL_POINTS );
			glColor3fv(GLfloat_3(1,1,1))
			glVertex3f( 0, 0, 0 );
			glEnd();

			# glEnable(GL_BLEND); #Enable blending.
			# glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); #Set blending function.
			# glColor3fv(GLfloat_3(1,1,1))
			# glutSolidSphere(radius, 10, 10)
			# glColor4fv(GLfloat_4(1,1,1, .1))
			# glutSolidSphere(.05, 5, 5)
		finally:
			glPopMatrix()
		glEnable(GL_LIGHTING)
		distance = self.check_collision(center, day, earth)
		if distance != -1:
			# print day
			# print self.full_name
			# print earth.coordinates(day)
			# print date_from_today(day - day_number(datetime.datetime.utcnow()))
			# print (day - 5579) / 365.25
			global NearAsteroids
			found = False
			for ast in NearAsteroids:
				if ast.full_name == self.full_name:
					found = True
					if distance < self.distance:
						self.distance = distance
						self.near_date = date_from_today(day - day_number(datetime.datetime.utcnow()))
					break
			if found == False:
				if len(NearAsteroids) == 5:
					NearAsteroids.pop()
				NearAsteroids.append(self)
				self.near_date = date_from_today(day - day_number(datetime.datetime.utcnow()))
			# print NearAsteroids

	def check_collision(self, center, day, collision_with):
		center2 = collision_with.coordinates(day)
		if abs(center[0] - center2[0]) < .02 and abs(center[1] - center2[1]) < .02 and abs(center[2] - center2[2]) < .02:
			return pow(pow(center[0] - center2[0], 2) + pow(center[1] - center2[1], 2) + pow(center[2] - center2[2], 2), .5)
		else:
			return -1



asteroids = []
def init_asteroids():
	with open('hazardasteroids_final.json') as data_file:    
		asteroids_json = json.load(data_file)
	c = 0
	t = 2000
	# print asteroids_json
	for asteroid in asteroids_json:
		# if c == 0:
			# continue
		asteroids.append(Asteroid(asteroid['epoch'], asteroid['om'], asteroid['i'], asteroid['w'], asteroid['a'], asteroid['e'], asteroid['ma'], asteroid['per'], .5, asteroid['full_name']))
		# print asteroid
		c+=1
		if c == t:
			break
		# print asteroid
		# break
		# print ast_obj.coordinates(5578.32868)

init_asteroids()

# print asteroids





def main():
	pass

	# d = day_number(datetime.datetime.utcnow())
	# print mercury.coordinates(d)
	# print venus.coordinates(d)
	# print earth.coordinates(d)
	# print moon.coordinates(d)
	# print mars.coordinates(d)
	# print jupiter.coordinates(d)
	# print saturn.coordinates(d)
	# print uranus.coordinates(d)
	# print neptune.coordinates(d)
	# print pluto.coordinates(d)

if __name__ == '__main__':
	main()

