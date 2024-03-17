
import math
import turtle
from constants import *

# This file defines the point class. One point is a place where the springs connect to.

def point_distance(p1, p2) -> float: # Gets the distance point p1 and p2.
	return math.sqrt((- p1.x0 + p2.x0)**2 + (- p1.y0 + p2.y0)**2)

def vec_dist(vec) -> float:
	x = vec[0]
	y = vec[1]
	return math.sqrt(x**2 + y**2)

def distance_vector(p1, p2) -> list: # Get the vector from p1 to p2
	if isinstance(p1, list): # Just a list.

		return [-1*p1[0]+p2[0], -1*p1[1]+p2[1]]

	return [-1*p1.x0+p2.x0, -1*p1.y0+p2.y0] # vector.

def distance_vector_norm(p1, p2) -> list: # Normalized.
	v = distance_vector(p1, p2)
	n = vec_dist(v) # Get the length of the distance vector.
	v = [v[0]/n, v[1]/n] # Divide elements.
	# Sanity checking.
	print("v == "+str(v))
	print("math.sqrt(v[0]**2 + v[1]**1) == "+str(math.sqrt(v[0]**2 + v[1]**2)))
	assert math.sqrt(v[0]**2 + v[1]**2) - 1 < 0.01 # The difference should be less than 0.01
	return v

class Point:
	def __init__(self, x0, y0, mass) -> None: # Constructor.
		self.x0 = x0
		self.y0 = y0
		self.pos = [x0, y0]
		self.mass = mass
		self.v = [0.0, 0.0] # Velocity vector.
		# Total force acting upon this point.
		self.force = 0.0
		# Connected springs. A list of spring references.
		self.connected_springs = []
		self.acceleration = 0.0
	def connect_spring(self,spring) -> None: # attaches the spring "spring" to this point.
		self.connected_springs.append(spring)
		# connect_point(self, p)
		spring.connect_point(self) # Connect the point to the spring.
	def calculate_force(self) -> None: # Calculates the force acting upon this point.
		
		#tot_f = 0.0
		tot_f_vec = [0.0, 0.0]
		for spring in self.connected_springs:
			# The spring has a relaxed length and the current length is the distance between the points.
			# Use hookes law.
			# F = -k*dx
			# First get the relaxed distance.
			relaxed_distance = spring.relaxed_distance
			# Now calculate actual distance.
			actual_distance = point_distance(spring.points[0], spring.points[1])
			dx = relaxed_distance - actual_distance
			F = spring.k * dx * -1 # Scalar value.

			# We need to convert the force to a vector.
			# we need a unit vector which points to the other point.

			# distance_vector_norm
			assert self in spring.points
			assert len(spring.points) == 2 # There should only be two points attached to each spring.

			if self == spring.points[0]:
				# We are the first point.
				p1 = spring.points[0]
				p2 = spring.points[1]
			elif self == spring.points[1]:
				# We are the second point.
				p1 = spring.points[1]
				p2 = spring.points[0]
			else:
				print("FUCK!")
				exit(1)
			print("p1 == "+str(p1))
			print("p2 == "+str(p2))
			assert p1 != p2
			print("p1 == p2: "+str(p1 == p2))
			# Now get the vector using distance_vector_norm.
			vec = distance_vector_norm(p1,p2)
			print("vec == "+str(vec))
			# Now multiply the thing with F
			vec = [vec[0]*F, vec[1]*F]
			tot_f_vec = [tot_f_vec[0]+vec[0], tot_f_vec[1]+vec[1]]
			#tot_f += F # Add to the force sum.

		#self.force = tot_f
		self.force = tot_f_vec
		print("Here is the force: "+str(self.force))
		return
	# Timestep a bit.
	def timestep(self, dt) -> None: # Update stuff.
		# F = m * a  =>  a = F / m
		self.acceleration = [self.force[0] / self.mass, self.force[1] / self.mass]
		print("self.acceleration == "+str(self.acceleration))
		# dv = acceleration * dt
		#dv = self.acceleration * dt

		self.v = [self.acceleration[0] * dt + self.v[0], self.acceleration[1] * dt + self.v[0]]

		# Now step over

		step_vector = [self.v[0]*dt, self.v[1]*dt] # dx = v * dt

		self.x0 = self.x0 + step_vector[0]
		self.y0 = self.y0 + step_vector[1]
		self.pos = [self.x0, self.y0]

	def render(self) -> None: # Shows this point.
		turtle.penup()
		turtle.goto(self.x0*SCALEFACTOR, self.y0*SCALEFACTOR)
		turtle.dot(10)






def main() -> int:
	# def distance_vector_norm(p1, p2) -> list:

	#vec0 = [0,0]
	#vec1 = [2,0]
	p1 = Point(-3,5,10)
	p2 = Point(2,2,10)
	v_norm = distance_vector_norm(p1, p2)
	print(v_norm)
	return 0

if __name__=="__main__":
	exit(main())
