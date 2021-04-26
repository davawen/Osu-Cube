from pynput import __doc__, mouse, keyboard

from math import cos, sin
import numpy as np

import time


def lerp(a: float, b: float, t: float):
	return (b - a)*t + a

def lerpToPos(x, y, ms):
	t = 0
	
	basePos = ms.position
	
	while(t < 1):
		ms.position = (lerp(basePos[0], x, t), lerp(basePos[1], y, t))
		
		t += 0.033
		time.sleep(0.016)

class Adjacent:
	def __init__(self, index):
		self.index = index
		self.hasGone = False

class Vertex:
	def __init__(self, x, y, z, adjacent, index):
		self.value = np.array((x, y, z))
		self.adjacent = adjacent
		self.index = index
		
	def moveToAdjacent(self, ms, vertices):
		
		lerpToPos(self.value[0], self.value[1], ms)
		
		# time.sleep(0.3)
		
		for adjacent in self.adjacent:
			if(adjacent.hasGone): # Too bad, already gone to that vertice
				continue
			
			vertex = vertices[adjacent.index]
			newPos = vertex.value

			adjacent.hasGone = True
			
			for otherAdjacent in vertex.adjacent:
				if(otherAdjacent.index == self.index):
					otherAdjacent.hasGone = True
			
			vertex.moveToAdjacent(ms, vertices)  # Search adjacents from this place !
			
			return # Stop this functions execution
		
		# If no adjacent vertices were found, we need to go deeper

		for adjacent in self.adjacent:
			if(vertices[adjacent.index].searchAdjacentAdjacent(ms, vertices)):
				return
		
	def searchAdjacentAdjacent(self, ms, vertices):
		for adjacent in self.adjacent:
			if(adjacent.hasGone):
				continue
			
			lerpToPos(self.value[0], self.value[1], ms)
			# time.sleep(0.3)

			vertex = vertices[adjacent.index]

			adjacent.hasGone = True
			for otherAdjacent in vertex.adjacent:
				if(otherAdjacent.index == self.index):
					otherAdjacent.hasGone = True
			
			vertex.moveToAdjacent(ms, vertices)
			
			return True
		# By this point, we should have finished the cube!
		return False

vertices = [
	Vertex(600. , 500., 100., # 0 +
		[ Adjacent(1), Adjacent(2), Adjacent(4) ],
		0
	),
	Vertex(1000., 500., 100.0, # 1 +x
		[ Adjacent(0), Adjacent(3), Adjacent(5) ],
		1
	),
	Vertex(600. , 500., 500., # 2 +z
		[ Adjacent(0), Adjacent(3), Adjacent(6) ],
		2
	),
	Vertex(1000., 500., 500., # 3 +xz
		[ Adjacent(1), Adjacent(2), Adjacent(7) ],
		3
	),
	Vertex(600. , 900., 100., # 4 +y
		[ Adjacent(0), Adjacent(5), Adjacent(6) ],
		4
	),
	Vertex(1000., 900., 100., # 5 +xy
		[ Adjacent(1), Adjacent(4), Adjacent(7) ],
		5
	),
	Vertex(600. , 900., 500., # 6 +yz
		[ Adjacent(2), Adjacent(4), Adjacent(7) ],
		6
	),
	Vertex(1000., 900., 500., # 7 +xyz
		[ Adjacent(3), Adjacent(5), Adjacent(6) ],
		7
	),
]

center = np.array((800., 700., 300.))

def rotateCube(angle: np.array, vertices, origin: np.array):
	rotationX = np.array(
	(
		(1., 0., 0.),
		(0., cos(angle[0]), -sin(angle[0])),
		(0., sin(angle[0]), cos(angle[0]))
	),
	dtype=object)

	rotationY = np.array(
	(
		(cos(angle[1]), 0., sin(angle[1])),
		(0., 1., 0.),
		(-sin(angle[1]), 0., cos(angle[1]))
	),
	dtype=object)
	
	rotationMatrix = np.dot(rotationY, rotationX)
	
	for vertex in vertices:
		
		vertex.value = vertex.value - origin # Rotate around center
		
		vertex.value = np.dot(rotationMatrix, vertex.value)
		
		vertex.value = vertex.value + origin
	
rotateCube([0.5, 0.2], vertices, center)

time.sleep(5)


lineIndexes = [
    [0, 1],
   	[0, 2],
   	[1, 3],
   	[2, 3],
   	[0, 4],
   	[2, 6],
   	[1, 5],
   	[3, 7],
   	[4, 5],
   	[4, 6],
   	[5, 7],
   	[6, 7]
]

ms = mouse.Controller()
kb = keyboard.Controller()

theta = 0

index = 0

# while(theta < 120):
if(True):	
	kb.press(keyboard.Key.ctrl)
	kb.press('a')
	kb.release('a')
	kb.release(keyboard.Key.ctrl)

	kb.press(keyboard.Key.delete)
	kb.release(keyboard.Key.delete)

	ms.position = (vertices[0].value[0], vertices[0].value[1])
	
	ms.press(mouse.Button.left)
	
	vertices[0].moveToAdjacent(ms, vertices)
	
	ms.release(mouse.Button.left)
	
	# while(index < 12):
	# 	flrIndex = index
		
	# 	positions = [
	# 		vertices[lineIndexes[flrIndex][0]],
	# 		vertices[lineIndexes[flrIndex][1]]
	# 	]
		
	# 	ms.position = (positions[0][0], positions[0][1])
		
	# 	ms.press(mouse.Button.left)
		
	# 	# newX = lerp(vertices[lineIndexes[flrIndex][0]][0], vertices[lineIndexes[flrIndex][1]][0], index-flrIndex)
	# 	# newY = lerp(vertices[lineIndexes[flrIndex][0]][1], vertices[lineIndexes[flrIndex][1]][1], index-flrIndex)
		
	# 	ms.position = (
	# 		positions[1][0],
	# 		positions[1][1]
	# 	)
		
		
	# 	ms.release(mouse.Button.left)
		
	# 	time.sleep(0.001)
		
	# 	index = flrIndex+1;
	
	index = 0
	
	rotateCube([.1, .05], vertices, center)
	
	theta += 1
