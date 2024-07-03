## Problem
This project is based on a popular puzzle, variously known as "Hashiwokakero", "Hashi" or "Bridges". You will need to write a program to solve this puzzle, and provide a brief description of the algorithm and data structures you have used. The input to your program will be a rectangular array of numbers and dots, for example:

![image](https://github.com/m1omomama/UNSW/assets/110977889/603fd91a-29f1-43cf-8db5-7feede7db413)



Each number represents an "island", while the dots represent the empty space (water) between the islands. Numbers larger than 9 are indicated by 'a' (10), 'b' (11) or 'c' (12). The aim is to connect all the islands with a network of bridges, satisfying these rules:
1. all bridges must run horizontally or vertically
2. bridges are not allowed to cross each other, or other islands
3. there can be no more than three bridges connecting any pair of islands
4. the total number of bridges connected to each island must be equal to the number on the island

![image](https://github.com/m1omomama/UNSW/assets/110977889/6f612c45-9381-4785-bd3e-23da0bcd06d8)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Solution

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

