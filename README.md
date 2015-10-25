# Astroact
Visualize the Asteroid Skies

## Overview
Astroact simulates the position of planets and 1,572 Potentially Hazardous Asteroids (PHAs) and predict their possible near pass with earth. Astroact provides interactive three dimensional visualization of the solar system with head tracking which helps to understand its actual geometry.

Video URL: https://youtu.be/bxICpe1wxSE

## Installation
  1. Install OpenGl python bindings
  2. Install OpenCV bindings
  
For Ubuntu based systems, following may work for handling requirements    
    `sudo apt-get install python-opengl python-opencv`    
To be sure, check `face detection samples` bundled with OpenCV.

## Running
  1. Connect Leap Motion Device(optional)
  2. Run app.py via `python2 app.py` or `python app.py`
  
### Running without face detection
To run the program without face detection, do `python2 app.py nofacedetect`.    
Following controls are available if face detection is disabled: 
  1. Mouse cursor can move the viewport
  2. `+` and `-` can change zoom levels

## More discussion
Astroact aims to simulate the position of heavenly bodies of our solar system, specifically 1,572 Potentially Hazardous Asteroids (PHAs) and predict their possible near pass with earth.

Astroact uses asteroids data from JPL Small-Body Database Search Engine (http://ssd.jpl.nasa.gov/sbdb_query.cgi). Based on the article "Computing planetary positions" (http://www.stjarnhimlen.se/comp/tutorial.html), this application calculates the Cartesian coordinates of the heavenly bodies at a given time from their respective orbital elements. The computed coordinates are then fed into the OpenGl api for 3d rendering of the solar system.

Written in python, Astroact makes use of OpenCV (http://opencv.org/) for face detection and to track the position of head. Based on the coordinates and size of the head, the solar system rotates to give the user a complete three dimensional visualization. Basically, this feature fabricates a window to our solar system. When you move your head to the left you see more of the objects to your right and when you move your head to the right, you see more of the objects to your left. Similarly, when you move closer to the screen, the center of the solar system (the Sun) seems to approach closer to you. Hence, this feature will be very helpful for educational purpose, especially to understand the geometry of our solar system and movement of celestial bodies around the sun. Moreover, Astroact uses Leap Motion Technology so that users can manipulate the time of simulation based on the hand gestures. Rotating your finger in clockwise direction speeds up the animation and vice-versa. Tapping in the mid air pauses and resumes the simulation.

Finally, the most important objective of Astroact is to predict the near pass of PHAs with earth. Based on the simulation, distance between the asteroids and the earth is calculated. When the calculated distance is very close to earth, a small information about the Asteroid (which includes its name, distance from earth and time of near pass) is displayed on the left side of the screen. This feature can be helpful for sky watchers.

The future extension of this project is to publish the computed information of near pass of asteroids to the web. The information will by supported by the means of graph plot of the distance of a given asteroids with earth against the time.
