#	Gabriel Summers ghs9@uw.edu
#	3/7/17
#	TCSS435
#	Assignment 1
#	15puzzle.py

import sys
from heapq import heappush, heappop

#################################################################
################## 		GLOBAL VARIABLES 	#####################
#################################################################
SOLVED_STATE_15		= '123456789ABCDEF '
SOLVED_STATE_15B	= '123456789ABCDFE '
SOLVED_STATE_8		= '12345678 '
SOLVED_STATE_3		= '123 '
STATE_15 			= '1645AC9F8 273BED'
STATE_8 			= '4732 6158'
STATE_3 			= '21 3'
ARGUMENTS			= sys.argv
STATE  				= ARGUMENTS[1]
VISITED				= []
DIMENSION			= int(len(STATE) ** 0.5)

if len(STATE) == 9:
	SOLVED_STATE 	= SOLVED_STATE_8
	SOLVED_STATE_B  = SOLVED_STATE_8
elif len(STATE) == 16:
	SOLVED_STATE 	= SOLVED_STATE_15
	SOLVED_STATE_B  = SOLVED_STATE_15B
elif len(STATE) == 4:
	SOLVED_STATE 	= SOLVED_STATE_3
	SOLVED_STATE_B 	= SOLVED_STATE_3
else:
	print '\nERROR ENCOUNTERED\n'
	print 'The puzzle state you put in of invalid length.'
	exit()

METHOD				= ARGUMENTS[2]
HEURISTIC  			= None

if len(ARGUMENTS) == 4:
	HEURISTIC 		= ARGUMENTS[3]

################################################################

################################################################
################## 		PUZSTATE CLASS 		####################
################################################################
class PuzState:
	def __init__(self, theState):
		self.state = theState
		self.parent = None
		self.depth = 0
		self.hval = 0

###############################################################

###############################################################
################# 		QUEUE CLASS 	#######################
###############################################################
class Queue:
	def __init__(self):
		self.items = []
		self.max = 0
		self.current = 0

	def isEmpty(self):
		return self.items == []

	def enqueue(self, item):
		self.current += 1
		if self.current > self.max:
			self.max = self.current
		self.items.append(item)

	def dequeue(self):
		self.current -= 1
		return self.items.pop(0)

	def size(self):
		return len(self.items)

#############################################################

#############################################################
##################		STACK CLASS 	#####################
#############################################################
class Stack:
	def __init__(self):
		self.items = []
		self.max = 0
		self.current = 0

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.current += 1
		if self.current > self.max:
			self.max = self.current
		self.items.append(item)

	def pop(self):
		self.current -= 1
		return self.items.pop()

	def size(self):
		return len(self.items)

############################################################

############################################################
############## 		METHODS FOR PUZZLE STATE	############
############################################################

# Prints the puzzle string in a 2d square format
def printPuzzle(stateOfPuz):
	for x in range(0,DIMENSION):
		print(stateOfPuz.state[DIMENSION*x:DIMENSION*(x+1)])
	print('\n')

# Will swap the space in the puzzle string
# with an adjacent char
def swap(stateOfPuz, i, j):
	li = list(stateOfPuz.state)
	li[i], li[j] = li[j], li[i]
	state = PuzState(''.join(li))
	state.depth = stateOfPuz.depth + 1
	state.parent = stateOfPuz
	return state
	
# This checks if space can be swaped with char above
def moveUp(stateOfPuz):
	space = stateOfPuz.state.index(' ')
	if (space - DIMENSION >= 0):
		return swap(stateOfPuz, space, space - DIMENSION)

# This checks if space can be swaped with char below
def moveDown(stateOfPuz):
	space = stateOfPuz.state.index(' ')
	if (space + DIMENSION <= ((DIMENSION*DIMENSION) -1)):
		return swap(stateOfPuz, space, space + DIMENSION)

# This checks if space can be swaped with char to the left
def moveLeft(stateOfPuz):
	space = stateOfPuz.state.index(' ')
	if((space // DIMENSION) == ((space - 1) // DIMENSION)):
		return swap(stateOfPuz, space, space - 1)

# This checks if space can be swaped with char to the right
def moveRight(stateOfPuz):
	space = stateOfPuz.state.index(' ')
	if((space // DIMENSION) == ((space + 1) // DIMENSION)):
		return swap(stateOfPuz, space, space + 1)


# This calculates the heuristic for greedy and aStar method
def calcHeuristic(stateOfPuz):
	if HEURISTIC == 'h1':
		count = 9
		listOfPassed = list(stateOfPuz.state)
		listOfActual = list(SOLVED_STATE)
		for i in range(0, len(listOfPassed)):
			if listOfPassed[i] == listOfActual[i]:
				count -= 1;
		return count
	elif HEURISTIC == 'h2':
		count = 0
		listOfPassed = list(stateOfPuz.state)
		listOfActual = list(SOLVED_STATE)
		for i in range(0, len(listOfPassed)):
			ch = listOfPassed[i]
			index = SOLVED_STATE.index(ch)
			count += abs((i // DIMENSION)-(index // DIMENSION))
			count += abs((i % DIMENSION)-(index % DIMENSION))
		return count
	else:
		print '\nERROR ENCOUNTERED\n'
		print 'The heuristic provided is not valid'
		print 'Please try one of the following:'
		print "\t\t\th1\t'Counts the number of tiles",\
			  "in incorrect places.'"
		print "\t\t\th2\t'Counts the manhattan distance of each tile"
		print "\t\t\t\t to it's correct placement and returns the sum.'"
		exit()

# This will look at all possible moves of a current
# state and return a list of PuzState objects that
# can spawn from it
def findMoves(stateOfPuz):
	li = []
	if METHOD == 'DLS':
		if stateOfPuz.depth < int(HEURISTIC):
			upState = moveUp(stateOfPuz)
			downState = moveDown(stateOfPuz)
			rightState = moveRight(stateOfPuz)
			leftState = moveLeft(stateOfPuz)
			if rightState is not None and \
			rightState.state not in VISITED:
				li.append(rightState)
				VISITED.append(rightState.state)
			if downState is not None and \
			downState.state not in VISITED:
				li.append(downState)
				VISITED.append(downState.state)
			if leftState is not None and \
			leftState.state not in VISITED:
				li.append(leftState)
				VISITED.append(leftState.state)
			if upState is not None and \
			upState.state not in VISITED:
				li.append(upState)
				VISITED.append(upState.state)
	else:
		upState = moveUp(stateOfPuz)
		downState = moveDown(stateOfPuz)
		rightState = moveRight(stateOfPuz)
		leftState = moveLeft(stateOfPuz)
		if HEURISTIC is not None:
			if upState is not None:
				upState.hval = calcHeuristic(upState)
			if downState is not None:
				downState.hval = calcHeuristic(downState)
			if rightState is not None:
				rightState.hval = calcHeuristic(rightState)
			if leftState is not None:
				leftState.hval = calcHeuristic(leftState)
		if rightState is not None and \
		rightState.state not in VISITED:
			li.append(rightState)
			VISITED.append(rightState.state)
		if downState is not None and \
		downState.state not in VISITED:
			li.append(downState)
			VISITED.append(downState.state)
		if leftState is not None and \
		leftState.state not in VISITED:
			li.append(leftState)
			VISITED.append(leftState.state)
		if upState is not None and \
		upState.state not in VISITED:
			li.append(upState)
			VISITED.append(upState.state)
	return li

#################################################################

#################################################################
################ 		SEARCH ALGORITHMS 		#################
#################################################################		
# ____________ _____ 
# | ___ \  ___/  ___|
# | |_/ / |_  \ `--. 
# | ___ \  _|  `--. \
# | |_/ / |   /\__/ /
# \____/\_|   \____/ 
#
#	This search utilizes
#	a queue. Queue class
#	defined above.

def bfs():
	succeeded = 0
	expanded = 0
	created = 0
	pState = PuzState(STATE)
	q = Queue()
	q.enqueue(pState)
	while q.size() > 0:
		pState = q.dequeue()
		expanded += 1
		VISITED.append(pState.state)
		if (pState.state == SOLVED_STATE or\
			pState.state == SOLVED_STATE_B):
			succeeded += 1
			break
		possibleStates = findMoves(pState)
		created += len(possibleStates)
		for eachState in possibleStates:
			q.enqueue(eachState)
	if (succeeded == 0):
		print -1,-1,-1,-1
		exit()
	print pState.depth,created,expanded,q.max


	# lis = []
	# while not pState is None:
	# 	lis.append(pState)
	# 	pState = pState.parent
	# for path in reversed(lis):
	# 	printPuzzle(path)

################################################################
# ____________ _____ 
# |  _  \  ___/  ___|
# | | | | |_  \ `--. 
# | | | |  _|  `--. \
# | |/ /| |   /\__/ /
# |___/ \_|   \____/ 
#
#	This search utilizes
#	a stack. Stack class
#	defined above.
                   
def dfs():
	succeeded = 0
	expanded = 0
	created = 0
	pState = PuzState(STATE)
	s = Stack()
	s.push(pState)
	while s.size() > 0:
		pState = s.pop()
		expanded += 1
		VISITED.append(pState.state)
		if (pState.state == SOLVED_STATE or\
			pState.state == SOLVED_STATE_B):
			succeeded = 1
			break
		possible = findMoves(pState)
		created += len(possible)
		for states in possible:
			s.push(states)
	if (succeeded == 0):
		print -1,-1,-1,-1
		exit()
	print pState.depth,created,expanded,s.max

################################################################
#  _   _ _____  _____  
# | | | /  __ \/  ___| 
# | | | | /  \/\ `--.  
# | | | ||      `--. \ 
# | |_| | \__/\/\__/ / 
#  \___/\_____/\____/ 
#
#	Kind of pointless cause
#	Cost will always be 1..
#	But the method is there I
#	guess if I ever need it.

def ucs():
	succeeded = 0
	expanded = 0
	created = 0
	pState = PuzState(STATE)
	maxF = 0
	VISITED.append(pState.state)
	pq = [(0, pState)]
	while len(pq) > 0:
		pState2 = heappop(pq)[1]
		expanded += 1
		if len(pq) > maxF:
			maxF = len(pq)
		if (pState2.state == SOLVED_STATE or\
			pState2.state == SOLVED_STATE_B):
			succeeded = 1
			break
		possibleStates = findMoves(pState2)
		created += len(possibleStates)
		for eachState in possibleStates:
			heappush(pq, (eachState.depth, eachState));
	if (succeeded == 0):
		print -1,-1,-1,-1
		exit()
	print pState2.depth,created,expanded,maxF

################################################################
#   ___     _    
#  / _ \ /\| |/\ 
# / /_\ \\ \ / / 
# |  _  |_     _|
# | | | |/ / \ \ 
# \_| |_/\/|_|\/
#
#	This method is by far
#	the most efficient.	
#	I tried to make my own
#	priority queue class but
#	It was buggy so I imported
#	methods from python's
#	heapq library.
               
def aStar():
	succeeded = 0
	expanded = 0
	created = 0
	maxF = 0
	pState = PuzState(STATE)
	VISITED.append(pState.state)
	pq = [(0, pState)]
	while len(pq) > 0:
		pState2 = heappop(pq)[1]
		expanded += 1
		if len(pq) > maxF:
			maxF = len(pq)
		if (pState2.state == SOLVED_STATE or\
			pState2.state == SOLVED_STATE_B):
			succeeded = 1
			break
		possibleStates = findMoves(pState2)
		created += len(possibleStates)
		for eachState in possibleStates:
			heappush(pq, (eachState.hval + eachState.depth, eachState));
	if (succeeded == 0):
		print -1,-1,-1,-1
		exit()
	print pState2.depth,created,expanded,maxF

################################################################
#  _____ ______ _____ _____________   __
# |  __ \| ___ \  ___|  ___|  _  \ \ / /
# | |  \/| |_/ / |__ | |__ | | | |\ V / 
# | | __ |    /|  __||  __|| | | | \ /  
# | |_\ \| |\ \| |___| |___| |/ /  | |  
#  \____/\_| \_\____/\____/|___/   \_/
#
#	This is similar to the aStar
#	method above but not quite
#	efficient. Again i'm using
#	heapq methods on a list.
                                      
def greedy():
	succeeded = 0
	expanded = 0
	created = 0
	maxF = 0
	pState = PuzState(STATE)
	VISITED.append(pState.state)
	q = [(0, pState)]
	while len(q) > 0:
		pState2 = heappop(q)[1]
		expanded += 1
		if len(q) > maxF:
			maxF = len(q)
		if (pState2.state == SOLVED_STATE or\
			pState2.state == SOLVED_STATE_B):
			succeeded = 1
			break
		possibleStates = findMoves(pState2)
		created += len(possibleStates)
		for eachState in possibleStates:
			heappush(q, (eachState.hval, eachState));
	if (succeeded == 0):
		print -1,-1,-1,-1
		exit()
	print pState2.depth,created,expanded,maxF

################################################################
# ______ ___________ _____ _   _      _     ___  ______________ 
# |  _  \  ___| ___ \_   _| | | |    | |    |  \/  |_   _|  _  \
# | | | | |__ | |_/ / | | | |_| |    | |    | .  . | | | | | | |
# | | | |  __||  __/  | | |  _  |    | |    | |\/| | | | | | | |
# | |/ /| |___| |     | | | | | |    | |____| |  | | | | | |/ / 
# |___/ \____/\_|     \_/ \_| |_/    \_____/\_|  |_/ \_/ |___(_)
#
#	This is the same as my dfs
#	method but will only go to
#	a certain depth.
                                                         

def dls():
	dfs()


###############################################################

###############################################################
##################		MAIN		###########################
###############################################################

if METHOD == 'BFS':
	bfs()
elif METHOD == 'DFS':
	dfs()
elif METHOD == 'UCS':
	ucs()
elif METHOD == 'DLS':
	if not HEURISTIC.isdigit():
		print '\nERROR ENCOUNTERED\n'
		print 'You selected to do depth limited search\n',\
			  'but failed to provide a valid depth limit.',\
			  '\n\nPlease try again with a valid integer.'
		exit()
	dls()
elif METHOD == 'GBFS':
	greedy()
elif METHOD == 'AStar':
	aStar()
else:
	print '\nERROR ENCOUNTERED\n'
	print 'Search algorithm not recognized,\n'
	print 'acceptable inputs include:\n'
	print "\t\tBFS\t'Breadth First Search.'"
	print "\t\tDFS\t'Depth First Search.'"
	print "\t\tUCS\t'Uniform Cost Search.'"
	print "\t\tDLS\t'Depth Limited Search.'"
	print "\t\tGBFS\t'Greedy Best First Search.'"
	print "\t\tAStar\t'A* Search.'"


###################################################################

###################################################################
####################		ARTIFACTS		#######################
###################################################################

#	| | 	This can be placed into most of the search algorithms
#  _| |_ 	to print the steps that result in the solved solution
#  \| |/	pState2 may need to be changed to pState depending on
#	 V 		the search algorithm. 
#
# lis = []
# while not pState2 is None:
# 	lis.append(pState2)
# 	pState2 = pState2.parent
# for path in reversed(lis):
# 	printPuzzle(path)