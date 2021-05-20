# Algorithm to find Highest-Scorers

Implemented in Python-3


An alogithm to fins the higest-scoring students subject-wise overall from a supplied CSV marks-list

A sample file (the test data given) can be found in [Student_marks_list.csv](Student_marks_list.csv)

## Executing the algorithm

`python FindToppers.py [csv-marklist-filename] [num_best]`

`csv-marklist-filename` : The filename of the CSV mark-list. (Default:  [Student_marks_list.csv](Student_marks_list.csv) )
`num-ranks` : The number of best students to be selected based on overall scores. ( Default: 3 - as specified in the task )

If the file ( default or supplied ) is not available/readable, the control-flow exits the script

## Outline of the Attempted Solution  

The script uses python's `csv` library to parse the CSV file. 

- The `csv reader object` is used to read one row of data at a time, into a list of string values.  

- When the header is read, the number of subjects are inferred, assuming the first column to be a list of names

- A for-loop is used to read the rest of the file and in each iteration, 

	- The subject scores of the current student are compared with the current maximum, and replaced if higher. 
	
	- If the scores are equal, both student names are recorded

	- The subject scores of the current student are also summed up while iterating the row-list. At the end of the list-iteration, the score is compared to minimum of the current `num_best scores`and is replaced with the smalled among them if the new one is greater. The name of the student is recorded in such as case.

	- If these scores are equal, both names are recorded

- After the entire file is parser, the results are displayed


## Data Structures used

### MinHeap - For overall best-students

Assume that `b` best students of the class have to be found ( here, b=3 )

A **MinHeap** with a `capacity = b` is initialized  

Each element of the heap looks like :   
`[ <max_score>, <stud_1>, <stud_2>, ... ]`     

At any instant, the MinHeap stores the `b` best students among the students seen so far.
When the total score of each student is found ( at the end of each row ), the score is compared to the `current minimum` of the heap. If higher, a customized MinHeap operation is used to replace the `current minimum` with the `new score`.

**NOTE** : Conventionally, removing the min and then adding the new element would involve two heapifications and contribute to `two O(log n)` operations.
However, here the `min is replaced with the new element` ( instead of the conventional method of replacing with the last lead-element ) and then `percolated down`. This not only cuts the run-time in half but has the added advantage of possibly not percolating till the bootom

A special case occurs when the new score is equal to the `current minimum` is equal to the `new score`. In such a case, the name is appended to the `current minimum`'s list.

Hence, in effect, the MinHeap stores `b` best students. 

#### The notion of 'best-student'

If there are multiple students with the same score, although they rank the same, they are counted as `individual best students`. Only when the number of such students with the same score exceeds `b`, they are listed additionally and separately

For instance,  
Consider `b=4` and the scores: `89, 85, 90, 89, 89, 50, 85`  
Here, the 4 best students are the ones with `90, 89, 89, 89`
Although the last three cannot be differentiated by rank, they ARE STILLthe 4 best students!

However, consider again `b=4` and the scores: `89, 85, 90, 89, 89, 50, 85, 89` 
( An additional 89 ) 
Here, an  `exact` 4 best students cannot be determined.
The best students would be ones with `90, 89, 89, 89, 89`, since there is no logical way to differentiate between the various 89-scorers. Hence, in this case, there are in fact `5` best students. 

They are listed separately in addition to the most-recently parsed among the 5 are displayed as `expected output`

### 2D List - For subject toppers

The subject toppers are stored in a **list** formatted as follows:

`[ [ <max_score>, <stud_1>, <stud_2>, ...(num_equal_scorers)] ...(num_subjects) ]`  

- The outer-list contains as many elements as there are subjects. The order of these lists corresponds to the order of subjects in the marks-list    
- The inner-list contains the highest-score for the subject, followed by names of all students who scored that much in the subject

When each subject score is encountered while parsing the rows, it compared against the corresponding list's `max_score` value and modified as necessary.   As mentioned, if the scores are equal, the new name is appended to the same list


### Time-Complexity Analysis

Assume marks for `n students` in `m subjects` and that `b best-students` to be found

- Parsing the lines of the marks-list file takes `n` iterations. In each iteration, the following is done

	- A row-list of size m is iterated. Hence, `m` iterations. ( The first value is the student name, which is separated out from the iteration. This is a `constant-time` operation ).

	- In each `list iteration`, the following operations are performed

		- Accumulate the subject-score by adding to total-score for student. This is q `constant-time` operation.

		- Compare the score to respective subject-list and alter it as mentioned in the previous sections. This is also a `constant-time` operation
	
	- If the number of students seen has crossed `b`, the total-score of the current student is compared to `minimum` of the min-heap. 

		- If the new score is higher, it is replaced and heapified using a customized operation, as described in the previous section. This involves `one percolation` and hence is a `logarithmic-time` operation with complexity `O(log b)`
		
		- If the new score is equal, the value is simply appended to the `current minimum` heap-element's list. This is a `constant-time` operation, since python uses linked-lists

	- Otherwise, if the number of students seen has NOT crossed `b`, the [ score, student ] element is simply inserted into the heap. This also involves `one percolation` and hence is a `logarithmic-time` operation with complexity `O(log b)`

Summing the complexities and applying the sum and product rules,
we have:

	  O(n*( m*(O(1) + O(1))+  O(log b)))
	= O(n*(O(m)+O(log b))
	= O(nm + n log b) (or) O(nm) + O(n log b)

- In the given case of `b=3`, this is `O(nm) + O(n.log 3)` = `O(nm) + O(n)` = `O(nm)`
- In the worst case, `b=n` and the complexity becomes `O(nm) + O(n.log n)`


