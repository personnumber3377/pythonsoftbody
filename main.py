
from spring import *
from point import *
import time
import math
from constants import *



MOUSE_X = 3.0
MOUSE_Y = 3.0

def motion(event):
	global MOUSE_X
	global MOUSE_Y
	x, y = event.x, event.y
	print('Mouse pos: {}, {}'.format(x, y))
	# Need to divide by the image scaling factor to actually get the shit...
	x, y = conv_mouse(x,y)
	MOUSE_X = -x / SCALEFACTOR
	MOUSE_Y = -y / SCALEFACTOR


def conv_mouse(x, y):
	# Converts the mouse position to actually useful coordinates.
	h = turtle.window_height()
	w = turtle.window_width()
	x -= ( w / 2 ) # This makes that x=0 is the center
	y -= ( h / 2 )

	x *= -1
	
	return x,y






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
def gen_springs(points, width, height, relaxed_distance, k) -> list:
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
				
				# No wonder changing the constant didn't change shit! We are just using a constant here!
				#new_spring = Spring(0.1, relaxed_distance=actual_length)
				new_spring = Spring(k, relaxed_distance=actual_length)
				# Now try to do the shit.

				cur_point.connect_spring(new_spring)
				other_point.connect_spring(new_spring)
				springs.append(new_spring)

	# return
	return springs


def draw_floor(floor_height) -> None:
	turtle.penup()
	turtle.goto(-10000, floor_height*SCALEFACTOR)
	turtle.pendown()
	turtle.goto(10000, floor_height*SCALEFACTOR)
	turtle.penup()



def mouse_force(follow_point, follow_force):

	# distance_vector(p1, p2)
	# distance_vector_norm
	
	force_vector = distance_vector_norm([follow_point.x0, follow_point.y0], [MOUSE_X, MOUSE_Y])
	# Now multiply by the force.
	force_vector = [force_vector[i]*follow_force for i in range(len(force_vector))]
	# Now add the force.

	follow_point.force = [follow_point.force[0]+force_vector[0], follow_point.force[1]+force_vector[1]]
	return

def get_mouse_click_coor(x, y):
	print("Mouse pressed down!!!")
	global MOUSE_PRESSED
	MOUSE_PRESSED = True


def enable_follow():
	print("called enable_follow!!!!")
	global MOUSE_PRESSED
	MOUSE_PRESSED = True

def disable_follow():
	global MOUSE_PRESSED
	MOUSE_PRESSED = True



MOUSE_PRESSED = False

def main() -> int:
	# def __init__(self, x0, y0, mass)
	global MOUSE_PRESSED
	# def __init__(self, p1, p2, k, relaxed_distance=None)

	#k = 0.1
	#k = 2.0
	#k = 0.6
	k = 5.0
	#mass = 1.0
	mass = 1.0
	relaxed_distance = 1
	spring = Spring(k, relaxed_distance=relaxed_distance) # Create the spring object.
	# def __init__(self, k, relaxed_distance=None) -> None:
	


	# Distance between points in box
	#distance = 1.0
	#distance = 1.0
	distance = 0.5
	# Create a 5 points by 5 points box for now.
	relaxed_dist = distance

	# width = 2
	# height = 2


	#width = 10
	#height = 10

	width = 5
	height = 5

	#points = generate_points(width, height, relaxed_dist, mass, distance) # Generate point box.
	#springs = gen_springs(points, width, height, relaxed_distance) # Generate the springs.


	ex_point_1 = Point(0,2,mass)
	ex_point_2 = Point(0,1,mass)

	spring_thing = Spring(k, relaxed_distance=1.0)

	ex_point_1.connect_spring(spring_thing)
	ex_point_2.connect_spring(spring_thing)

	points = [ex_point_1, ex_point_2]
	springs = [spring_thing]

	window = turtle.Screen()

	# gen_springs(points, width, height, relaxed_distance)
	window.onkeypress(enable_follow, "Up")
	window.onkeyrelease(enable_follow, "Up")
	window.listen()

	time_step = 0.1


	points = generate_points(width, height, relaxed_dist, mass, distance) # Generate point box.
	springs = gen_springs(points, width, height, relaxed_distance, k) # Generate the springs.

	turtle.tracer(0,0)
	turtle.speed(0)


	floor = -1.0 # y coordinate of the floor


	#stat_index = 10

	#orig_x = points[stat_index].x0
	#orig_y = points[stat_index].y0


	# Every spring should be fully connected.

	spring_connected = [spring.isfullyconnected() for spring in springs]
	assert all(spring_connected)
	#print("Passed!!")
	#exit(1)

	# Now we also want to check that every point has atleast three connected springs.

	lengths_shit = [len(point.connected_springs) for point in points]
	assert all([x >= 3 for x in lengths_shit])

	print("length of springs: "+str(len(springs)))

	#print("Passed!")
	#exit(1)

	canvas = turtle.getcanvas()
	canvas.bind('<Motion>', motion)

	# Which point we are following?
	follow_point = points[0]
	#follow_force = 2.0 # Apply two newtons of force towards the mouse cursor.
	follow_force = 1.0


	

	turtle.onscreenclick(get_mouse_click_coor)

	while True:
		for point in points:
			point.render()
		for spring in springs:
			spring.render()
		draw_floor(floor)
		turtle.update()

		for point in points:
			point.calculate_force()

		# Make one point follow mouse.

		#follow_point.x0 = MOUSE_X
		#follow_point.y0 = MOUSE_Y
		if MOUSE_PRESSED:

			mouse_force(follow_point, follow_force)

		for point in points:
			point.timestep(time_step)


		# This is to make the box bounce from the floor.
		for point in points:
			if point.y0 < floor:
				point.y0 = floor
		turtle.clear()


		
		MOUSE_PRESSED = False
		# Force one of the points to stay in place.

		#points[stat_index].x0 = orig_x
		#points[stat_index].y0 = orig_y

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
