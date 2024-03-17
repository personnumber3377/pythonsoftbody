
from spring import *
from point import *
import time

def generate_points(width, height, relaxed_distance, mass) -> list:
	# def __init__(self, x0, y0, mass
	out = []
	for h in range(height):
		for w in range(width):
			x0 = w
			y0 = h



def main() -> int:
	# def __init__(self, x0, y0, mass)

	# def __init__(self, p1, p2, k, relaxed_distance=None)

	#k = 0.1
	k = 2.0
	mass = 10.0
	relaxed_distance = 1
	spring = Spring(k, relaxed_distance=relaxed_distance) # Create the spring object.
	# def __init__(self, k, relaxed_distance=None) -> None:
	distance = 10
	
	# Create a 5 points by 5 points box for now.
	relaxed_dist = distance

	width = 5
	height = 5


	points = generate_points(width, height, relaxed_dist, mass) # Generate point box.


	point1 = Point(0,0,mass)
	point2 = Point(2,0,mass)
	time_step = 0.1
	# Now create the connections.

	point1.connect_spring(spring)
	point2.connect_spring(spring)

	turtle.tracer(0,0)
	turtle.speed(0)

	while True:
		point1.render()
		point2.render()
		spring.render()
		turtle.update()

		point1.calculate_force()
		point2.calculate_force()

		# timestep

		point1.timestep(time_step)
		point2.timestep(time_step)

		turtle.clear()

		time.sleep(0.1)


	return 0

if __name__=="__main__":
	exit(main())
