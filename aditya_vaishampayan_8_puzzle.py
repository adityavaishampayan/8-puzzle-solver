#importing numpy
import numpy as np
import time

#creating a list of all the possible configurations
final_nodes_list = []

#creating a list for parent child configurations
nodes_info_list = [[0,0]]

rows = int(input("Enter number of rows in the matrix: "))
columns = int(input("Enter number of columns in the matrix: "))
matrix = []
print("Enter the %s x %s matrix: "% (rows, columns))
for i in range(rows):
    matrix.append(list(map(int, input().rstrip().split()))) 

start_config = np.array(matrix)

#locating blank tile i.e 0
def blank_tile_location(current_node):
    i,j = np.where(current_node == 0)
    return i,j

#ACTIONS [L,R,U,D]
#logic in action_move_left is similar for all actions

def action_move_left(current_node):
    #creating a copy of input var
    temp_node = np.copy(current_node)    
    #position of the blank tile
    row,coloumn = blank_tile_location(temp_node)
    if coloumn == 0:
        #return falseif moving left isnt possible
        status = False
    else:
        #return true if moving left is possible
        status = True
        #swapping the zero tile and left tile locations
        temp_node[[row,coloumn]],temp_node[[row,coloumn-1]] = temp_node[[row,coloumn-1]],temp_node[[row,coloumn]]
    #returning the new node
    return status,temp_node

def action_move_right(current_node):
    
    temp_node = np.copy(current_node)    
    row,coloumn = blank_tile_location(temp_node)
    if coloumn == 2:
        status = False
    else:
        status = True
        temp_node[[row,coloumn]],temp_node[[row,coloumn+1]] = temp_node[[row,coloumn+1]],temp_node[[row,coloumn]]
    return status,temp_node

def action_move_up(current_node):
    temp_node = np.copy(current_node)    
    row,coloumn = blank_tile_location(temp_node)
    if row == 0:
        status = False
    else:
        status = True
        temp_node[[row,coloumn]],temp_node[[row-1,coloumn]] = temp_node[[row-1,coloumn]],temp_node[[row,coloumn]]
    return status,temp_node

def action_move_down(current_node):
    temp_node = np.copy(current_node)    
    row,coloumn = blank_tile_location(temp_node)
    if row == 2:
        status = False
    else:
        status = True
        temp_node[[row,coloumn]],temp_node[[row+1,coloumn]] = temp_node[[row+1,coloumn]],temp_node[[row,coloumn]]
    return status,temp_node

#function for checking if a created node is already present or not
def ispresent(node_to_check,nodes_list):
    l = len(nodes_list)
    node_to_check_copy = (node_to_check).copy()
    #node_to_check_copy = np.array(node_to_check_copy)
    for i in range(l):
        state = False        
        if np.array_equal(nodes_list[i],node_to_check_copy):
            state = True
            break
    return state

child_counter = 0
element_counter = 0

#giving starting node configuration
#here i have taken center_config for testing
start_node = start_config

#appending the node to the list of all possible nodes
final_nodes_list.append(start_node)

#starting time
start = time.time()

while element_counter <= len(final_nodes_list):
    
    #defining goal configuration
    goal_config = np.array([[1,2,3],[4,5,6],[7,8,0]])
    
    node = final_nodes_list[element_counter] 
    

    #APPLYING LEFT RIGHT UP DOWN ALL 4 ACTIONS TO THE GIVEN NODE
    status, temporary1 = action_move_left(node)
    #status = true means the move was possible and hence we proceed further
    if status == True:
        #using the ispresent function to check if the node already exists
        if ispresent(temporary1,final_nodes_list) == False:
            #if it doesn't exist append that node to the list of configurations
            final_nodes_list.append(temporary1)
            #give that node a number
            child_counter += 1
            #append the parent child pair to the list which contains the list
            #of parents and childrens.
            nodes_info_list.append([element_counter,child_counter])                       
            

    status, temporary2 = action_move_right(node)
    if status == True:
        if ispresent(temporary2,final_nodes_list) == False:
            final_nodes_list.append(temporary2)
            child_counter += 1
            nodes_info_list.append([element_counter,child_counter])
            #temporary_right = temporary
           
    
    status, temporary3 = action_move_up(node)
    if status == True:
        if ispresent(temporary3,final_nodes_list) == False:
            final_nodes_list.append(temporary3)
            child_counter += 1
            nodes_info_list.append([element_counter,child_counter])
            #temporary_up = temporary   
            
            
    status, temporary4 = action_move_down(node)
    if status == True:
        if ispresent(temporary4, final_nodes_list) == False:
            final_nodes_list.append(temporary4)
            child_counter += 1
            nodes_info_list.append([element_counter,child_counter])
            #temporary_down = temporary        
            
    element_counter += 1
    
    #print(len(final_nodes_list))
    #print(child_counter)
       
    if np.array_equal(temporary1,goal_config):
        print(temporary1)                        
        break    
    if np.array_equal(temporary2,goal_config):
        print(temporary2)
        break
    if np.array_equal(temporary3,goal_config):
        print(temporary3)
        break
    if np.array_equal(temporary4,goal_config):
        print(temporary4)
        break

lists = []
goal_config = goal_config.T
lists.append(goal_config)

l = len(nodes_info_list)
nodes_info_list = np.array(nodes_info_list)

X = nodes_info_list[l-1] 
element1 = X[0]      
element2 = X[1]
print(element2,element1)
count = 0
while element1 != 0:
    for i in range(l):
        X = nodes_info_list[i]
        if X[1] == element1:
            element1 = X[0]
            element2 = X[1]
            Y = final_nodes_list[element2]
            Y = np.array(Y)
            Y = Y.T
            listY = Y.tolist()
            lists.append(listY)
            count +=1 
            print(element2,element1)

start_node = np.array(start_node)
start_node = start_node.T
lists.append(start_node)
    
file = open("path.txt","w")
for a in reversed(lists):
    for element in a:
        for index in element:
            file.write("%i\t" % index)
    file.write("\n")        
file.close()

file = open("parent_child.txt","w")
Z = nodes_info_list.tolist()
for item in Z:
    for index in reversed(range(2)):
        file.write("%i\t" % item[index])
    file.write("0")
    file.write("\n")
file.close()

file = open("all_nodes.txt","w")
X = final_nodes_list
for item in X:
    #node = X[item].tolist()
    for element in item.T:
        for index in element:
            file.write("%i\t" % index)
    file.write("\n")        
file.close()   
end = time.time()
print("elapsed time:" + str((end-start)) + "s")
print("no of nodes created: ", len(final_nodes_list))

