import Priority 
import numpy as np 
import bridgemaker
Hashi = Priority.HashiBoard
#print(Priority.Original_HashiBoard)



def Display_HashiBoard():
    for i in range (Priority.H_Row):
        for j in range (Priority.H_Col):
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
                case -10:
                    island = Priority.Original_HashiBoard[i][j]

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
                    
                    print(island, end="")
                    continue

            print("{}".format(chr),  end='')

        print()

Display_HashiBoard()     
Priority.logic_bridges()
bridgemaker.lonely_island()

Priority.logic_bridges()
bridgemaker.lonely_island()

Priority.logic_bridges()
bridgemaker.lonely_island()

Display_HashiBoard()
print("\n------------------------------\n")
#Priority.forward_pass()
for i in range(5):
    bridgemaker.forward_pass_bridge()
    Display_HashiBoard()

    print("\n------------------------------\n")
'''
Priority.forward_pass()
#Display_HashiBoard()
print("\n------------------------------\n")
Priority.forward_pass()
#Display_HashiBoard()
print("\n------------------------------\n")
'''


Display_HashiBoard()

                    

