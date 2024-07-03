'''
=====================================================================*/
AI ASSIGNMENT 1 : HASHIWOKAKERO PUZZLE
by- Ayusha Priyadarshani (z5452643) , Aryaman Sakthivel (z5455785)
=====================================================================*/

The program combines logic, search methods and data structure functionality to navigate through the Hashiwokakero puzzle. 
Data structures like 2D Numpy Arrays and Stacks have been used to store and manage the island-bridge information. 
The algorithm begins with using logic assignment and elimination in a loop to read and study the input data in order to build all compulsory bridges. 
This drastically reduces the size and complexity of the map, reducing computation time and increasing efficiency. 
The program then proceeds to use forward propagation from the first appearing island to assign bridge values to this highly scaled-down version of the map, choosing the biggest between available neighbouring islands. 
If a choice does not lead to the solution, it will use back propagation to fix the mistake and reach the desired, solved state.

Logic Bridges- Some islands, when surrounded by a specific number of neighbours, must share a certain number of bridges with each neighbour in order to satisfy the puzzle conditions.
For example, islands numbered 12 must have 4 neighbours and should share 3 bridges with each to reach a correct solution. 
Similarly, island 11s must have 2 bridges and 4 neighbours whereas island 10s must have 1 bridge with 4 neighbours. 
We can make several more programing decisions depending on the number of neighbours the remaining islands have. 
For example, if island 9 has 3 neighbours it must share 3 bridges with all three and islands 8 and 7 follow the same with 2 bridges and 1 bridge respectively.
Island 6 will have 3 bridges with each neighbour if there are 3 neighbours and islands 5 and 4 follow the same with 2 bridges and 1 bridge respectively. 

Functions- We have numerous functions to implement the above explained logic-- 
    neighbour_search() finds whether there are any neighbours for a given island, 
    update_islands() uses count_bridges() to update the island number and displays the remaining required bridges to complete it, 
    lonely_island() counts islands with only 1 neighbour and builds all required bridges to that neighbour, etc.

'''

import numpy as np 
import bridgemaker

Hashi = bridgemaker.HashiBoard

#This function converts the 2D numpy HashiBoard  to a string representation of the board
def Display_HashiBoard():
    for i in range (bridgemaker.H_Row):
        for j in range (bridgemaker.H_Col):
            chr = Hashi[i][j]
            match chr:
                case 0:
                    print(" ",end="")
                    continue
                case -1:
                    print('-',end="")
                    continue
                case -2:
                    print('=',end="")
                    continue
                case -3:
                    print('E',end="")
                    continue
                case -4:
                    print('|',end="")
                    continue
                case -5:
                    print('"',end="")
                    continue
                case -6:
                    print('#',end="")
                    continue
                
            island = bridgemaker.Original_HashiBoard[i][j]

            match island:
                case 12:
                    print('c',end="")
                    continue

                case 11:
                    print('b',end="")
                    continue

                case 10:
                    print('a',end="")
                    continue
            
            print("{}".format(island), end="")
            continue


        print()

complete=False

#Loop untill all logic bridges are constructed
logical_count=1
while logical_count > 0:
    prev=np.copy(Hashi)
    logical_count=bridgemaker.logic_bridges()
    bridgemaker.lonely_island()
    error=bridgemaker.false_output(prev,Hashi)
    if error: break


#Loop untill all forward bridges are formed 
while complete==False:
    prev=np.copy(Hashi)
    bridgemaker.forward_pass()
    complete=bridgemaker.board_complete()
    error=bridgemaker.false_output(prev,Hashi)
    if error: break


#Display the final Solved HashiBridge
Display_HashiBoard()

print(Hashi)

            
