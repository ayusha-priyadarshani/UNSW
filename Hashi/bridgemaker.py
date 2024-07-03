import scan_print_map as scan
import numpy as np

Original_HashiBoard, H_Row, H_Col = scan.bridge_print()

#make a back up of the hashiboard
HashiBoard=np.copy(Original_HashiBoard)

#This function searches all 4 sides and returns if there are neighbors 
Horizontal_b = [-1,-2,-3]
Veritical_b = [-4,-5,-6]

#stack used for back propagation
Board_stack=[]

#This function checks the number of neighbors an island has
def neighbor_search(Board,r,c):
    R_Neighbor=0
    L_Neighbor=0
    U_Neighbor=0
    D_Neighbor=0

    #Check number of Right neighbors
    can_move = True
    ptr = c+1
    while can_move:
         if ptr > H_Col-1:
             can_move = False
         
         else:
            curr=Board[r][ptr] 
                
            if (curr == -10) or (curr in Veritical_b):#or curr == -3:
                can_move = False
            
            elif curr >= 1:
                R_Neighbor+=1
                can_move = False
            else:
                ptr+=1

    #Check number of Left neighbors
    can_move = True
    ptr = c-1
    while can_move:
         if ptr < 0:
             can_move = False
         
         else:
            curr=Board[r][ptr] 
                
            if (curr == -10) or (curr in Veritical_b):# or curr == -3:
                can_move = False
            
            elif curr >= 1:
                L_Neighbor+=1
                can_move = False
            else:
                ptr-=1

    #Check number of Up neighbors
    can_move = True
    ptr = r-1
    while can_move:
         if ptr < 0:
             can_move = False
         
         else:
            curr=Board[ptr][c] 
                
            if (curr == -10) or (curr in Horizontal_b): #or curr == -6:
                can_move = False
                
            elif curr >= 1:
                U_Neighbor+=1
                can_move = False
            else:
                ptr-=1

    #Check number of Down neighbors
    can_move = True
    ptr = r+1
    while can_move:
         if ptr > H_Row - 1:
             can_move = False
         
         else:
            curr=Board[ptr][c] 
                
            if (curr == -10) or (curr in Horizontal_b): #or curr == -6:
                can_move = False
            
            elif curr >= 1:
                D_Neighbor+=1
                can_move = False
            else:
                ptr+=1

    Total_neighbors = R_Neighbor + L_Neighbor + U_Neighbor + D_Neighbor    
    return R_Neighbor, D_Neighbor, L_Neighbor, U_Neighbor, Total_neighbors  

#This function checks if the island is full i.e if it can accomodate more bridges
def island_isfull(r,c):
    island=Original_HashiBoard[r][c]

    total_bridges=count_bridges(r,c)
    if island == total_bridges: return True
    else : return False

#This function finds all islands with just one neighbour and connects them with bridges
def lonely():
    lonely_count=0
    for i in range (H_Row):
        for j in range (H_Col):
            if  HashiBoard[i][j]>=1:
                r, d, l, u, total_neighbors = neighbor_search(HashiBoard,i,j)
                island=HashiBoard[i][j]
                
                if  total_neighbors == 1:
                    if r == 1 and HashiBoard[i][j+1]!=-3:
                        if island==1:
                            brig_num = HashiBoard[i][j+1]-1
                        else:
                            brig_num = (0 - island)
                        right_bridge_constructor(brig_num,i,j)
                        lonely_count +=1

                    elif l == 1 and HashiBoard[i][j-1]!=-3:
                        if island==1:
                            brig_num = HashiBoard[i][j-1]-1
                        else:
                            brig_num = (0 - island)
                        left_bridge_constructor(brig_num,i,j)
                        lonely_count+=1

                    elif  u == 1 and HashiBoard[i-1][j]!=-6:
                        if island==1:
                            if HashiBoard[i-1][j] == 0:
                                brig_num = -4
                            else:    
                                brig_num = HashiBoard[i-1][j]-1
                        else:
                            brig_num = (0 - island) - 3
                        up_bridge_constructor(brig_num ,i,j)
                        lonely_count+=1

                    elif d == 1 and HashiBoard[i+1][j]!=-6:
                        if island==1:
                            if HashiBoard[i+1][j] == 0:
                                brig_num = -4
                            else:
                                brig_num = HashiBoard[i+1][j]-1
                        else:
                            brig_num = (0 - island) - 3
                        down_bridge_constructor(brig_num,i,j)
                        lonely_count+=1
                        
                    update_islands()
    return lonely_count
        
#This function repeats the loneley function untill all islands are complete
def lonely_island():
    while True:
        prev=np.copy(HashiBoard)
        islands=lonely()
        error=false_output(prev,HashiBoard)
        if error:break
        if islands == 0: break 

#This funcition is used to place bridges on islands which must have one or more bridges every side
def logic_bridges():
    logical_count=0
    for i in range (H_Row):
        for j in range (H_Col):
            
            curr = HashiBoard[i][j]

            match curr:
                case 12:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)
                    

                    if neighbors == 4:
                        right_bridge_constructor(-3,i,j)
                        left_bridge_constructor(-3,i,j)
                        up_bridge_constructor(-6,i,j)
                        down_bridge_constructor(-6,i,j)
                    
                        logical_count+=1
                        

                case 9:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 3:
                        if r == 1: right_bridge_constructor(-3,i,j)
                        if l == 1: left_bridge_constructor(-3,i,j)
                        if  u == 1: up_bridge_constructor(-6,i,j)
                        if d == 1:down_bridge_constructor(-6,i,j)

                        logical_count+=1

                case 6:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 2:
                        if r == 1: right_bridge_constructor(-3,i,j)
                        if l == 1: left_bridge_constructor(-3,i,j)
                        if  u == 1: up_bridge_constructor(-6,i,j)
                        if d == 1:down_bridge_constructor(-6,i,j)

                        logical_count+=1

                case 11:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 4:
                        double_bridge_constructor(i,j,r,d,l,u)
                        logical_count+=1
                        
                case 10:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 4:
                        single_bridge_constructor(i,j,r,d,l,u)
                        logical_count+=1
                        
                case 8:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 3:
                        double_bridge_constructor(i,j,r,d,l,u)
                        logical_count+=1
                
                case 7:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 3:
                        single_bridge_constructor(i,j,r,d,l,u)
                        logical_count+=1

                case 5:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 2:
                        double_bridge_constructor(i,j,r,d,l,u)
                        logical_count+=1

                case 4:
                    r, d, l, u, neighbors = neighbor_search(HashiBoard,i,j)

                    if neighbors == 2:
                        single_bridge_constructor(i,j,r,d,l,u)
                        logical_count+=1

    update_islands()
    return logical_count
 
#This function counts the number of bridges attached to the island
def count_bridges(r,c):
    right_bridges,left_bridges,down_bridges,up_bridges=0,0,0,0
    if c < (H_Col-1): 
        if  HashiBoard[r][c+1] in Veritical_b:
            right_bridges = 0
        else: 
            right_bridges = abs(HashiBoard[r][c+1])

    if c > 0: 
        if HashiBoard[r] [c - 1] in Veritical_b:
            left_bridges=0
        else:
            left_bridges = abs(HashiBoard[r][c-1])

    if r < (H_Row-1):
        if  HashiBoard[r+1][c]==0 or HashiBoard[r+1][c] in Horizontal_b:
            down_bridges=0
        else:
            down_bridges = abs(HashiBoard[r+1][c])-3 

         
    if r > 0: 
        if HashiBoard[r-1][c]==0 or HashiBoard[r-1][c] in Horizontal_b:
            up_bridges=0
        else:
            up_bridges = abs(HashiBoard[r-1][c])-3
    
    #print ("Right",right_bridges,"Left",left_bridges,"Down",down_bridges,"Up",up_bridges)

    total_bridges=(right_bridges + left_bridges + up_bridges + down_bridges)
    return total_bridges

#This function subtracts the number of bridges from the island and updates the board
def update_islands():
    for i in range (H_Row):
        for j in range (H_Col):
            if  HashiBoard[i][j] > 0:
                bridges=count_bridges(i,j)
                new_island=(Original_HashiBoard[i][j]-bridges)

                if new_island == 0: 
                    HashiBoard[i][j]=-10
                elif new_island<0:
                    HashiBoard[i][j]=-11
                else: 
                    HashiBoard[i][j]=new_island
    return

#This function checks the Hashi Board is complete
def board_complete():
    for i in range (H_Row):
        for j in range (H_Col):
            element=HashiBoard[i][j]
            
            if element>0:
                return False
    #print('\n\nComplete')
    return True

#These functions construct respective Bridges in the Hashi Board 
def right_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    row = i
    col = j

    if right==1:
        while (col<H_Col-1):
            if (HashiBoard[row][col+1] == 0):
                HashiBoard[row][col+1] = bridge_num
                col+=1
            
            elif (HashiBoard[row][col+1] >= -3 and HashiBoard[row][col+1] <= -1):
                if (HashiBoard[row][col+1] > bridge_num):
                    HashiBoard[row][col+1] = bridge_num
                    col+=1

                else: 
                    right=0
                    break
            
            else:
                right=0
                break

def left_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    row = i
    col = j

    if left==1:
        while (col>0):
            if (HashiBoard[row][col-1] == 0):
                HashiBoard[row][col-1] = bridge_num
                col-=1
            
            elif (HashiBoard[row][col-1] >= -3 and HashiBoard[row][col-1] <= -1):
                if (HashiBoard[row][col-1] > bridge_num):
                    HashiBoard[row][col-1] = bridge_num
                    col-=1

                else: 
                    left=0
                    break
            
            else:
                left=0
                break
       
def down_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    row = i
    col = j

    if down==1:
        while (row<H_Row-1):
            if (HashiBoard[row+1][col] == 0):
                HashiBoard[row+1][col] = bridge_num
                row+=1
            
            elif (HashiBoard[row+1][col] >= -6 and HashiBoard[row+1][col] <= -4):
                if (HashiBoard[row+1][col] > bridge_num):
                    HashiBoard[row+1][col] = bridge_num
                    row+=1

                else: 
                    down=0
                    break
            
            else:
                down=0
                break
   
def up_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    row = i
    col = j

    if up==1:
        while (row>0):
            if (HashiBoard[row-1][col] == 0):
                HashiBoard[row-1][col] = bridge_num
                row-=1
            
            elif (HashiBoard[row-1][col] >= -6 and HashiBoard[row-1][col] <= -4):
                if (HashiBoard[row-1][col] > bridge_num):
                    HashiBoard[row-1][col] = bridge_num
                    row-=1

                else: 
                    up=0
                    break
            
            else:
                up=0
                break
    
def single_bridge_constructor(i,j,r,d,l,u):
    if r == 1: right_bridge_constructor(-1,i,j)
    if l == 1: left_bridge_constructor(-1,i,j)
    if  u == 1: up_bridge_constructor(-4,i,j)
    if d == 1: down_bridge_constructor(-4,i,j)

def double_bridge_constructor(i,j,r,d,l,u):
    if r == 1: right_bridge_constructor(-2,i,j)
    if l == 1: left_bridge_constructor(-2,i,j)
    if  u == 1: up_bridge_constructor(-5,i,j)
    if d == 1: down_bridge_constructor(-5,i,j)

#This function returns the neighbor island with te greater number
def highest_neighbour(i,j):
    island=HashiBoard[i][j]
    Neighbour_max=0
    if island>0:
        r , d ,l , u,total_n = neighbor_search(HashiBoard,i,j)
        right_v=0
        left_v=0
        up_v=0
        down_v=0
        highest_n=0
        dir=''

        if r==1:
            #find right neighbour value
            row=i
            col=j+1
            count=0

            while (col<H_Col-1):
                if (HashiBoard[row][col]<=0 and HashiBoard[row][col]!=-3 and HashiBoard[row][col] not in Veritical_b):
                    col+=1
                
                else:
                    break
                
            
            right_v=HashiBoard[row][col]
            if (right_v>highest_n):
                highest_n=right_v
                dir='right'
        
        if d==1:
            #find down
            row=i+1
            col=j
            count=0

            while row<H_Row-1:
                if (HashiBoard[row][col]<1 and HashiBoard[row][col]!=-6 and HashiBoard[row][col] not in Horizontal_b):
                    row+=1
                
                else:
                    break
                
            down_v=HashiBoard[row][col]
            if (down_v>highest_n):
                highest_n=down_v
                dir='down'
        

        if right_v==down_v:
            if right_v==0 or down_v==0:
                return 0
            dir='equal'

    
        return dir

#This function checks if the Hashi Board has any errors
def false_output(prev,curr):
    same=True
    for i in range(H_Row):
        for j in range(H_Col):
            if  prev[i][j]!=curr[i][j]:
                same=False
            if curr[i][j] < -10:
                return True
    if same==True:
        return True
    else:
        return False


#These functions add bridges to all remaining islands using conditional logic
def forward_pass():
    for i in range(H_Row):
        for j in range(H_Col):

            island=HashiBoard[i][j]

            if island > 0:
                forward_pass_bridge(i,j)
                lonely_island()
                return
            else:
                continue
            
def forward_pass_bridge(i,j):
        #print('forward_pass')
        dir = highest_neighbour(i,j)
        #print(dir)

        if dir=='right':
            #check r to make single right bridge
            brig_num=HashiBoard[i][j+1]

            right_bridge_constructor((brig_num-1) , i, j)
            update_islands()
            return

        elif dir=='down':
            brig_num=HashiBoard[i+1][j]

            if brig_num == 0:
                brig_num=-4
            else:
                brig_num=brig_num-1
            down_bridge_constructor(brig_num , i, j)
            update_islands()
            return
    
        elif dir =='equal':
            #Tries forward propagation with down bridge
            result=forward_propagation(i,j,'down',HashiBoard)

            if result=='Solved': return

            elif result == 'Stuck': 
                #Backtracking and trying other directions
                forward_propagation(i,j,'right', HashiBoard)
                return
        else:
            #print("Error in Forward Pass Bridge")
            return
        
            
#This function used forward and backword propagation in case of neighbors with same value
def forward_propagation(i,j,dirr,HashiBoard):
    backup_hashi=np.copy(HashiBoard)
    Board_stack.append([backup_hashi])
    
    #make a right bridge
    if dirr == 'right':
        brig_num=HashiBoard[i][j+1]
        right_bridge_constructor((brig_num-1) , i, j)
        update_islands()

    #create a down bridge
    elif dirr == 'down':
        brig_num=HashiBoard[i+1][j]
        if brig_num == 0:
            brig_num=-4
        else:
            brig_num=brig_num-1
        down_bridge_constructor(brig_num , i, j)
        update_islands()

    #solve normally 
    complete=False
    while  not complete :
        prev_hashi=np.copy(HashiBoard)
        forward_pass()

        complete=board_complete()
        wrong_output=false_output(prev_hashi,HashiBoard)

        if complete==True: return 'Solved'
        if wrong_output:
            break
    board=Board_stack.pop()
    HashiBoard=np.copy(board)
    return 'Stuck'
    
