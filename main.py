
from spring import *
from point import *
import time
import math

def generate_points(width, height, relaxed_distance, mass, actual_distance) -> list:
	# def __init__(self, x0, y0, mass
	out = []
	for h in range(height):
		for w in range(width):
			x0 = w*actual_distance
			y0 = h*actual_distance
			new_point = Point(x0, y0, mass)
			out.append(new_point)
	assert len(out) == width*height
	return out

# This gets the point at x,y.

def get_point(x,y, all_points, width, height):
	if x < 0 or x >= width or y < 0 or y >= height:
		print("Fuck!")
		return None
	index = y*width+x
	return all_points[index] # Returns the correct box index.

def get_neighbour_positions(x, y):
	return [[x+1, y],
			[x+1, y+1],
			[x+1, y-1],
			[x, y+1],
			[x, y-1],
			[x-1, y],
			[x-1, y+1],
			[x-1, y+1]]

# Get distance between points.
def get_distance(cur_point, other_point):
	diff_vec = [-1*cur_point.x0+other_point.x0, -1*cur_point.y0+other_point.y0]

	return math.sqrt(diff_vec[0]**2 + diff_vec[1]**2)


# This basically just connects all of the springs.
# This generates the connecting springs.
def gen_springs(points, width, height, relaxed_distance) -> list:
	spring_shit = set()
	springs = []

	# Loop through every point, find neighbours and then connect the springs.

	for y in range(height):
		for x in range(width):
			# Get the current point.
			# get_point(x,y, all_points, width, height)
			cur_point = get_point(x,y,points, width, height)

			neighs = get_neighbour_positions(x,y)
			for neig_pos in neighs:
				# Check if the spring is already connected between these two points.
				tup = (x,y,neig_pos[0], neig_pos[1])
				tup2 = (neig_pos[0], neig_pos[1], x,y)

				if tup in spring_shit or tup2 in spring_shit:
					continue
				
				# Now get the other point.
				x_other = neig_pos[0]
				y_other = neig_pos[1]

				other_point = get_point(x_other,y_other,points, width, height)
				# If the position is invalid, then continue.

				if other_point == None:
					continue

				spring_shit.add(tup)

				# Now add the spring.
				# Create spring.

				# def __init__(self, k, relaxed_distance=None)

				# Get the relaxed length.

				actual_length = get_distance(cur_point, other_point)
				new_spring = Spring(0.1, relaxed_distance=actual_length)

				# Now try to do the shit.

				cur_point.connect_spring(new_spring)
				other_point.connect_spring(new_spring)
				springs.append(new_spring)

	# return
	return springs








def main() -> int:
	# def __init__(self, x0, y0, mass)

	# def __init__(self, p1, p2, k, relaxed_distance=None)

	#k = 0.1
	k = 20.0
	mass = 1.0
	relaxed_distance = 1
	spring = Spring(k, relaxed_distance=relaxed_distance) # Create the spring object.
	# def __init__(self, k, relaxed_distance=None) -> None:
	


	# Distance between points in box
	distance = 0.5
	
	# Create a 5 points by 5 points box for now.
	relaxed_dist = distance

	width = 5
	height = 5


	points = generate_points(width, height, relaxed_dist, mass, distance) # Generate point box.
	springs = gen_springs(points, width, height, relaxed_distance) # Generate the springs.
	# gen_springs(points, width, height, relaxed_distance)

	time_step = 0.1




	turtle.tracer(0,0)
	turtle.speed(0)


	floor = 0 # y coordinate of the floor

	while True:
		for point in points:
			point.render()
		for spring in springs:
			spring.render()
		turtle.update()

		for point in points:
			point.calculate_force()


		for point in points:
			point.timestep(time_step)


		# This is to make the box bounce from the floor.
		for point in points:
			if point.y0 < floor:
				point.y0 = floor
		turtle.clear()

		#time.sleep(0.1)


	'''


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

		#point1.timestep(time_step)
		point2.timestep(time_step)

		turtle.clear()

		time.sleep(0.1)
	'''




	return 0

if __name__=="__main__":
	exit(main())
