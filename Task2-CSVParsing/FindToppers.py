import csv
import sys


MAX_VAL = 999
DUMMY_STR = "-"
  
class MinHeap:
	"""
	A Min-Heap data-structure implementation
	# Each element is a list, where
	# - Index 0: Max Score
	# - Indices 1-<end> : Names
	The elements are heapified using 'score' as the key
	to resolve partial ordering
	"""
  
	def __init__(self, capacity):          
		self.capacity = capacity
		self.size = 0
		self.heap = [ [MAX_VAL, DUMMY_STR] for x in range(self.capacity) ]
		self.front = 0
		self.key_idx = 0

	def key_at(self, posn):
		return self.heap[posn][self.key_idx]

	def parent(self, posn):          
		return posn // 2  

	def left_child(self, posn):          
		return posn*2 + 1

	def right_child(self, posn):          
		return posn*2 + 2

	def is_leaf(self, posn):          
		return posn>=(self.size//2) and posn<=self.size

	def swap(self, src, destn):          
		self.heap[src], self.heap[destn] = self.heap[destn], self.heap[src]

	def append_values_to(self, posn, values):
		self.heap[posn] += values

	def insert(self, element):          
		if self.size >= self.capacity:
			return None
		self.heap[self.size] = element
		# Insert at bottom, percolate-up
		self.percolate_up(self.size)
		self.size += 1

	def percolate_up(self, posn):
		if posn==0:
			return None
		parent = self.parent(posn)
		if self.key_at(parent)>self.key_at(posn):
			self.swap(parent, posn)
			self.percolate_up(parent)

	def percolate_down(self, posn):	
		if self.is_leaf(posn):
			return None
		# Find smaller child
		left = self.left_child(posn)
		right = self.right_child(posn)
		smaller = posn 
		if self.key_at(left)<self.key_at(smaller):
			smaller = left 
		if self.key_at(right)<self.key_at(smaller):
			smaller = right
		# Percolate-down if necessary
		if(smaller!=posn):
			self.swap(smaller, posn)
			self.percolate_down(smaller)

	def remove_min_add_elem(self, new_elem):  
		popped = self.heap[self.front]
		self.heap[self.front] = new_elem
		self.percolate_down(self.front)      
		return popped 
		
	def append_values_to_min(self, new_name):
		self.append_values_to(self.front, new_name)

	def delete_min(self):  
		popped = self.heap[self.front]   
		self.size -= 1
		self.heap[self.front] = self.heap[self.size]
		self.percolate_down(self.front)      
		return popped

	def show_min(self):
		return self.key_at(self.front)


marklist_file = sys.argv[1:2]
if not marklist_file:
	print("No CSV file supplied")
	exit(0)

# Number of ranks to determine
num_ranks = 3

with open(marklist_file[0]) as f_in:
	reader = csv.reader(f_in, delimiter=',')
	header = next(reader)

	# Initialize Subject-Max list
	subject_names = header[1:]
	num_subjects = len(subject_names)
	# List of subject wise toppers
	# Each element is a list, where
	# - Index 0: Max Score
	# - Indices 1-<end> : Names
	# Allows for multiple toppers with same score
	# Guranteed that atleast one name will enter, assuming Min Marks is 0
	subject_max = [ [-1,] for x in range(num_subjects) ]
	score_idx = 0
	name_idx = 1

	# Initialize Overall-Max Min-Heap - stores `num_ranks` maximums
	# Min-Heap always stores 3 elements
	# Each element is a list, where
	# - Index 0: Max Score
	# - Indices 1-<end> : Names
	# Allows for multiple toppers with same score
	# Always selects 3 best students (even if the 3 have same scores)
	# But if there are more students with same marks as any of the 
	# selected 3, these are listed additionaly
	overall_max = MinHeap(capacity=num_ranks)

	for datarow in reader:
		name, scores = datarow[0], datarow[1:]

		total_score = 0
		for i in range(num_subjects):

			# Find subject toppers
			scores[i] = int(scores[i])
			if scores[i] > subject_max[i][score_idx]:
				subject_max[i] = [ scores[i], name ]
			elif scores[i] == subject_max[i][score_idx]:
				subject_max[i] += [ name ]

			# Accumulate student's total score
			total_score += scores[i]

		if reader.line_num-1 > num_ranks:
			if overall_max.show_min() < total_score:
				overall_max.remove_min_add_elem( [ total_score, name ] )
			elif overall_max.show_min() == total_score:
				overall_max.append_values_to_min( [ name ] )
		else:
			overall_max.insert( [ total_score, name ] )

# Displaying subject toppers
for i in range(num_subjects):
	disp_string = "Topper(s) in {subject} : {name}".format(
		subject = subject_names[i].ljust(10),
		name = ', '.join(subject_max[i][1:])
	)
	print(disp_string)

print()

# Displaying overall `num_ranks`
best_studs_rev = list()
scores = list()
for i in range(num_ranks):
	elem = overall_max.delete_min()
	best_studs_rev.extend(elem[overall_max.key_idx+1:])
	scores.extend([ elem[overall_max.key_idx] for x in range(len(elem)-1) ])
found = len(scores)

print("Best students in the class are", end=" ")
for i in range(1, num_ranks+1):
	print(best_studs_rev[-i], end=", ")

print("\n")

print("-------------------------------------------------------------")
print("List including  scores")
print("( If more student(s) have scores tied with the Mentioned Best, this list includes them ) ")
rank = 1
prev_score = scores[0]
for i in range(found-1, -1, -1):
	disp_string = " Rank {rank}: {name} => {marks}".format(
		name=best_studs_rev[i].ljust(10),
		marks=scores[i],
		rank=rank
	)
	print(disp_string)
	if(scores[-i]>prev_score):
		rank +=1
		prev_score = scores[-i]
	

	