import scan_print_map as Test
import numpy as np

Original_HashiBoard, H_Row, H_Col = Test.bridge_print()

HashiBoard=np.copy(Original_HashiBoard)

#This function searches all 4 sides and returns if there are neighbors 
Horizontal_b = [-1,-2,-3]
Veritical_b = [-4,-5,-6]

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
                
            if (curr == -10) or (curr in Veritical_b):
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
                
            if (curr == -10) or (curr in Veritical_b):
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
                
            if (curr == -10) or (curr in Horizontal_b):
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
                
            if (curr == -10) or (curr in Horizontal_b):
                can_move = False
            
            elif curr >= 1:
                D_Neighbor+=1
                can_move = False
            else:
                ptr+=1

    Total_neighbors = R_Neighbor + L_Neighbor + U_Neighbor + D_Neighbor    
    return R_Neighbor, D_Neighbor, L_Neighbor, U_Neighbor, Total_neighbors  

#This function finds all islands with just one neighbour and connects them with bridges
def lonely_island():
    #while True:
    lonely_count=0
    for i in range (H_Row):
        for j in range (H_Col):
            if  HashiBoard[i][j]>=1:
                r, d, l, u, total_neighbors = neighbor_search(HashiBoard,i,j)
                island=HashiBoard[i][j]
                
                if  total_neighbors == 1:
                    #print("Lonely: Row",i,"column:",j,"Island:",island)
                    if r == 1:
                        if island==1:
                            brig_num = HashiBoard[i][j+1]-1
                        elif island==2:
                            brig_num = HashiBoard[i][j+1]-2
                        else:
                            brig_num = (0 - island)
                            right_bridge_constructor(brig_num,i,j)

                    elif l == 1:
                        if island==1:
                            brig_num = HashiBoard[i][j-1]-1
                        #elif island==2:
                        #    brig_num = HashiBoard[i][j-1]-2
                        else:
                            brig_num = (0 - island)
                            left_bridge_constructor(brig_num,i,j)

                    elif  u == 1:
                        if island==1:
                            if HashiBoard[i-1][j] == 0:
                                brig_num = -4
                            else:    
                                brig_num = HashiBoard[i-1][j]-1
                        #elif island==2:
                        #    brig_num = HashiBoard[i-1][j]-2
                        else:
                            brig_num = (0 - island) - 3
                            up_bridge_constructor(brig_num ,i,j)

                    elif d == 1:
                        if island==1:
                            if HashiBoard[i+1][j] == 0:
                                brig_num = -4
                            else:
                                brig_num = HashiBoard[i+1][j]-1
                        #elif island==2:
                        #    brig_num = HashiBoard[i+1][j]-2
                        else:
                            brig_num = (0 - island) - 3
                            down_bridge_constructor(brig_num,i,j)

                    lonely_count += 1
                    
        #if  lonely_count==0: break
 
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
                else: 
                    HashiBoard[i][j]=new_island


def right_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    #print(right,down,left,up)
    #print(bridge_num)

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
    update_islands()
    #print(HashiBoard, H_Row, H_Col)

def left_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    #print(right,down,left,up)
    #print(bridge_num)

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
    update_islands()
    #print(HashiBoard, H_Row, H_Col)
    
def down_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    #print(right,down,left,up)
    #print(bridge_num)

    row = i
    col = j

    if down==1:
        while (row<H_Row-1):
            if (HashiBoard[row+1][col] == 0):
                HashiBoard[row+1][col] = bridge_num
                row+=1
                #print(row)
            
            elif (HashiBoard[row+1][col] >= -6 and HashiBoard[row+1][col] <= -4):
                #print(HashiBoard[row+1][col])
                if (HashiBoard[row+1][col] > bridge_num):
                    HashiBoard[row+1][col] = bridge_num
                    row+=1

                else: 
                    down=0
                    break
            
            else:
                down=0
                break
    update_islands()
    #print(HashiBoard, H_Row, H_Col)
    
def up_bridge_constructor(bridge_num , i, j):
    right, down, left, up, total_n = neighbor_search(HashiBoard,i,j)
    #print(right,down,left,up)
    #print(bridge_num)

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
    update_islands()
    #print(HashiBoard, H_Row, H_Col)

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
                if (HashiBoard[row][col]<=0):
                    col+=1
                
                else:
                    break
                    #col=H_Col-1
                    #count=1
                
            
            right_v=HashiBoard[row][col]
            if (right_v>highest_n):
                highest_n=right_v
                dir='right'
            #print("right")
            #print(right_v)
            
            #else:

        
        if d==1:
            #find down
            row=i+1
            col=j
            count=0

            while row<H_Row-1:
                if (HashiBoard[row][col]<1):
                    row+=1
                
                else:
                    #row=H_Row-1
                    break
                    #count=1
                
            #if count==0:
            down_v=HashiBoard[row][col]
            if (down_v>highest_n):
                highest_n=down_v
                dir='down'
            #print(down_v)
        

        if total_n>0:                
            Neighbour_max=highest_n

    
        return dir

def forward_pass_bridge():
    for i in range(H_Row):
        for j in range(H_Col):

            dir = highest_neighbour(i,j)
        
            if dir=='right':
                #check r to make single right bridge
                brig_num=HashiBoard[i][j+1]

                right_bridge_constructor((brig_num-1) , i, j)

            elif dir=='down':
                brig_num=HashiBoard[i+1][j]

                if brig_num == 0:
                    brig_num=-4
                else:
                    brig_num=brig_num-1
                down_bridge_constructor(brig_num , i, j)
            
            lonely_island()
            return
        


'''
right_bridge_constructor(-2,3,3, H_Row,H_Col)
left_bridge_constructor(-3,3,3, H_Row,H_Col)
right_bridge_constructor(-3,3,3, H_Row,H_Col)
up_bridge_constructor(-5,3,3, H_Row,H_Col)
up_bridge_constructor(-6,3,3, H_Row,H_Col)
'''