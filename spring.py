
import turtle
from constants import *



class Spring:
	#def __init__(self, p1, p2, k, relaxed_distance=None) -> None: # Constructor.
	def __init__(self, k, relaxed_distance=None) -> None: # Constructor.
		# k is the spring constant.
		self.k = k
		self.points = [None, None]
		if relaxed_distance: # If we specify the relaxed distance, then add it.
			self.relaxed_distance = relaxed_distance
	def connect_point(self, p) -> None: # This method attaches the point p to this spring.
		if self.points[0] == None: # The spring isn't connected to anything yet.
			self.points[0] = p
		elif self.points[1] == None: # This spring is already attached to the first point.
			self.points[1] = p
			# Now that the other point is attached, we need to calculate the relaxed_distance.
			# Maybe...
		else:
			# Can not attach an already attached spring.
			print("Tried to attach an already attached spring!")
			exit(1)
	# Rendering function.
	def render(self) -> None:
		if None in self.points: # Do not render springs which aren't fully connected
			return
		p1 = self.points[0]
		p2 = self.points[1]
		turtle.penup()
		turtle.goto(p1.x0*SCALEFACTOR, p1.y0*SCALEFACTOR)
		turtle.pendown()
		turtle.goto(p2.x0*SCALEFACTOR, p2.y0*SCALEFACTOR)
		turtle.penup()
		return
	
	def isfullyconnected(self) -> bool: # This checks if the spring is fully connected.
		return not None in self.points

