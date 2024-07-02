
import numpy as np
import bridgemaker 

#Original_HashiBoard, H_Row, H_Col = bridgeMap.bridge_print()

HashiBoard = bridgemaker.HashiBoard
Original_HashiBoard = bridgemaker.Original_HashiBoard
H_Row = bridgemaker.H_Row
H_Col = bridgemaker.H_Col



#HashiBoard[0][1]=-6
#HashiBoard[1][0]=-1
#HashiBoard[1][2]=-3
#HashiBoard[1][2]=-4

#print(HashiBoard, H_Row, H_Col)
#print(Original_HashiBoard)

   

#lonely_island()

#This funcition is used to place bridges on islands which must have one or more bridges every side
def logic_bridges():
    for i in range (H_Row):
        for j in range (H_Col):
            
            curr = HashiBoard[i][j]

            match curr:
                case 12:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)
                    

                    if neighbors == 4:
                        bridgemaker.right_bridge_constructor(-3,i,j)
                        bridgemaker.left_bridge_constructor(-3,i,j)
                        bridgemaker.up_bridge_constructor(-6,i,j)
                        bridgemaker.down_bridge_constructor(-6,i,j)
                        

                case 9:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 3:
                        if r == 1: bridgemaker.right_bridge_constructor(-3,i,j)
                        if l == 1: bridgemaker.left_bridge_constructor(-3,i,j)
                        if  u == 1: bridgemaker.up_bridge_constructor(-6,i,j)
                        if d == 1:bridgemaker.down_bridge_constructor(-6,i,j)

                case 6:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 2:
                        if r == 1: bridgemaker.right_bridge_constructor(-3,i,j)
                        if l == 1: bridgemaker.left_bridge_constructor(-3,i,j)
                        if  u == 1: bridgemaker.up_bridge_constructor(-6,i,j)
                        if d == 1:bridgemaker.down_bridge_constructor(-6,i,j)

                case 11:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 4:
                        bridgemaker.double_bridge_constructor(i,j,r,d,l,u)
                        
                case 10:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 4:
                        bridgemaker.single_bridge_constructor(i,j,r,d,l,u)
                        
                case 8:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 3:
                        bridgemaker.double_bridge_constructor(i,j,r,d,l,u)
                
                case 7:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 3:
                        bridgemaker.single_bridge_constructor(i,j,r,d,l,u)

                case 5:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 2:
                        bridgemaker.double_bridge_constructor(i,j,r,d,l,u)

                case 4:
                    r, d, l, u, neighbors = bridgemaker.neighbor_search(HashiBoard,i,j)

                    if neighbors == 2:
                        bridgemaker.single_bridge_constructor(i,j,r,d,l,u)
            

#This function add bridges to all remaining islands using conditional logic
def forward_pass():
    for i in range(H_Row):
        for j in range(H_Col):

            island=HashiBoard[i][j]

            if island > 0:
                bridgemaker.forward_pass_bridge()
            else:
                continue
            #lonely_island()
            
    


#This function checks if an island is complete or not i.e can it accomodate more bridges
def island_isfull(r,c):
    island=bridgemaker.Original_HashiBoard[r][c]

    total_bridges=bridgemaker.count_bridges(r,c)
    if island == total_bridges: return True
    else : return False


#priority_bridges()
#logic_bridges()

#print(HashiBoard)

#lonely_island()

#logic_bridges()


#print(HashiBoard)

#lonely_island()

#,d,l,u,tot = bridgemaker.neighbor_search(HashiBoard,1,4)
#print("right",r,"left",l,"down",d,"up",u)
#print("total neihg for",HashiBoard[1][4],"is",tot)



#logic_bridges()
#lonely_island()

#forward_pass()
#print(HashiBoard)

#forward_pass()

print(HashiBoard,'\n',H_Row,H_Col)



