#!/usr/bin/python3

#=========================================================================================================================================================>
#                                                                   COMP3411 Assignment 3                                                                   
#                                                               Nine-Board Tic-Tac-Toe Agent
#                                                                    Program:  agent.py      
#
#                                                             by: Ayusha Priyadarshani (z5452784) 
#                                                                 Aryaman Sakthivel    (z5455785)
#  
# ==========================================================================================================================================================>
#   
#   QUESTION: Briefly describe how your program works, including any algorithms and data structures employed, =
#   and explain any design decisions you made along the way. 
#
# ==========================================================================================================================================================>
#   
# _________________________________________________________________________ANSWER:___________________________________________________________________________
#   Our program combines Alpha-Beta pruning with logic, object-oriented programming, and data structure functionality to create 
#   an artificially intelligent agent which can defeat other agents with above-average to good intelligence. 
#   Several classes along with data structures like 2D arrays and lists have been used to store the current board and game state information.
#
# _____________________________________________________________________IMPLEMENTATION:_______________________________________________________________________
#
#   The algorithm begins by evaluating the state of the current board. For every turn of the agent, 
#   a copy of the original board is made, and the best move is found by calculating efficiency of each legally allowed play on that board. 
#
#   We use Minimax, as explained above, and a custom-designed scoring logic to determine the most optimal move by finding all future moves 
#   post committing a move to the current board and assigning it a score based on how well its subtrees perform. 
#   We do this for all possible moves and choose the move with the highest score, as the agent will have a higher chance of winning by proceeding 
#   down the subtree.
#
#   This is repeated till the opponent wins or a move by the agent on the current board forms a winning combination, leading to the agent winning.
#
# ____________________________________________________________________SCORE CALCULATON:______________________________________________________________________
#
#   We calculate the score of each board by weighing the number of marks placed by the agent and the number of marks placed by the opponent against 
#   the 8 possible tic-tac-toe winning combinations. 
#   The frequency and placement of marks in each row and column total out to a temporary score which gets added to the final score of the board.
#
#   Agent and opponent scores are initialised to zero.
#
#   Assume the board is
#
#    X X O
#    . . .
#    X O . 
#
#   While checking for 3 in a row, for example in row 1, for every instance of the agent’s mark, the temporary score is increased by 10 times the
#   previous score. 
#   The first X increases the score to 10, while the second one increases it to 100. 
#   However, the third place is occupied by the opponent so the first and second marks are nullified since the combo can not be completed.
#
#   For column 1, the two Xs add on to weigh 100 and are added to the final score.
#
#   For row 3, the X and O get cancelled out so the final total score of the board is 100. 
#
# ==========================================================================================================================================================>

import socket
import sys
import numpy as np
import math
import copy
from states import State
# a board cell can hold:
#   0 - Empty
#   1 - We played here
#   2 - Opponent played here

# the boards are of size 10 because index 0 isn't used
#boards = np.zeros((10, 10), dtype="int8")
boards = [[0] * 10 for i in range(10)]
s = [".","X","O"]
curr = 0 # this is the current board to play in

#====================================================================================>
#Class Nodes used to save the state of the game 
class Nodes:
    def __init__(self,state,player):
        self.state = state
        self.player = player
        #list of additional moves
        self.children = []

    #Get a new Node which is one step/depth deeper
    def new_Node(self,move):
        new_state = self.state.new_state(move, 2 if self.player else 1)

        if new_state == None:
            return None
        return Nodes(new_state, not self.player)

#====================================================================================>
    

# print a row
def print_board_row(bd, a, b, c, i, j, k):
    print(" "+s[bd[a][i]]+" "+s[bd[a][j]]+" "+s[bd[a][k]]+" | " \
             +s[bd[b][i]]+" "+s[bd[b][j]]+" "+s[bd[b][k]]+" | " \
             +s[bd[c][i]]+" "+s[bd[c][j]]+" "+s[bd[c][k]])

# Print the entire board
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

#Setting Definations
EMPTY = 0
AGENT = 1 
OPPONENT = 2
MIN_EVAL = -math.inf
MAX_EVAL =  math.inf

#Global variables 
moves = 1
min_depth = 5
max_depth = 13

# choose a move to play
def play():
    # print_board(boards)
    # just play a random move for now
    #n = np.random.randint(1,9)
    #while boards[curr][n] != 0:
    #    n = np.random.randint(1,9)
    # print("playing", n)
    n = search_bestMove()
    place(curr, n, 1)
    return n

#====================================================================================>

#Calculate optimal depth based on moves made 
def dynamic_depth(moves):
    depth = min_depth
    depth += math.floor(moves / 81 * (max_depth - min_depth))
    return int(depth)

'''
#ATTEMPT 1
#Check if any player got a 3-in-a-row
def check_winner(board,player):
    #List of winning combinations
    winning_combos = [                    #3-in-a-row
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Horizontal
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Vertical
        (1, 5, 9), (3, 5, 7)              # Diagonal
    ]

    #Check for every combo in winning combos
    for combo in winning_combos:
        a,b,c = combo
        
        #Check if values at combo positions in the board are player tiles
        if board[a] == board[b] == board[c] == player:
            return True #player is the winner
        #No winner found or player is not the winner
        return False 

#Draw if current board is full 
def check_draw(board):
    for tile in board:
        if tile == EMPTY:
            return False
    
    #No empty tiles in the current board
    return True

#Evaluate the current board using a set of predefined scores
def eval_board(board,player,opponent):
    evaluation = 0
    #print(board)
    #Center tile
    if board[5] == player:
        evaluation += 2
    
    #Corner tile
    for i in (1,3,7,9):
        if board[i] == player:
            evaluation += 1
        elif board[i] == opponent:
            evaluation -= 1

    #2 in a row and opttential win or loss
    #Check board rows
    for row in (1,4,7):
        #If player has 2-in-a-row (horizontally) and last tile is empty 
        if board[row] == board[row +1] == player and board[row+2] == EMPTY: 
            evaluation += 100
        #If opponent has the same
        elif board[row] == board[row +1] == opponent and board[row+2] == EMPTY:
            evaluation -= 1000
        
        #If player has last two tiles and the first tile is empyt
        if board[row + 1] == board[row + 2] == player and board[row]== EMPTY:
            evaluation += 100
        #If opponent has the same
        elif board[row + 1] == board[row + 2] == opponent and board[row]== EMPTY:
            evaluation -= 1000

        #If player has first and last and middle is empty
        if board[row] == board[row + 2] == player and board[row+1]== EMPTY:
            evaluation += 100
        #If opponent has the same
        elif board[row] == board[row + 2] == opponent and board[row+1]== EMPTY:
            evaluation -= 1000

    #Check board columns
    for col in (1,2,3):
        #If player has 2-in-a-row (vertically) and last tile is empyt
        if board[col] == board[col + 3] == player and board[col + 6] == EMPTY:
            evaluation += 100
        #If opponent has the same
        if board[col] == board[col + 3] == opponent and board[col + 6] == EMPTY:
            evaluation -= 1000

        #If player has 2-in-a-row (vertically) and first tile is empyt
        if board[col + 3] == board[col + 6] == player and board[col] == EMPTY:
            evaluation += 100
        #If opponent has the same
        if board[col + 3] == board[col + 6] == opponent and board[col] == EMPTY:
            evaluation -= 1000

        #If player has first and last and the middle is empty 
        if board[col] == board[col + 6] == player and board[col +3] == EMPTY:
            evaluation += 100
        #If opponent has the same
        if board[col] == board[col + 6] == opponent and board[col + 3] == EMPTY:
            evaluation -= 1000
        
    
    #Check board diagonals
    #if player has first two diagonals and the last is empty
    if board[1] == board[5] == player and board[9] == EMPTY:
        evaluation += 100
    elif board[1] == board[5] == opponent and board[9] == EMPTY:
        evaluation -= 100 
    if board[3] == board[5] == player and board[7] == EMPTY:
        evaluation += 100
    elif board[3] == board[5] == opponent and board[7] == EMPTY:
        evaluation -= 100

    #If player has last two diagonals and the first is empty
    if board[5] == board[9] == player and board[1] == EMPTY:
        evaluation += 100
    elif board[5] == board[9] == opponent and board[1] == EMPTY:
        evaluation -= 100 
    if board[5] == board[7] == player and board[3] == EMPTY:
        evaluation += 100
    elif board[5] == board[7] == opponent and board[3] == EMPTY:
        evaluation -= 100

    #IF player has two end diagonals and middle is empty
    if board[1] == board[9] == player and board[5] == EMPTY:
        evaluation += 100
    elif board[1] == board[9] == opponent and board[5] == EMPTY:
        evaluation -= 100 
    if board[3] == board[7] == player and board[5] == EMPTY:
        evaluation += 100
    elif board[3] == board[7] == opponent and board[5] == EMPTY:
        evaluation -= 100
    
    return evaluation
'''

#Itterate through the valid moves and use minimax to select the best move
def search_bestMove():
    global curr

    bestScore = MIN_EVAL
    bestMove = 0 

    alpha = MIN_EVAL
    beta = MAX_EVAL

    depth = dynamic_depth(moves)

    all_moves = []
    for move in range(1,10):
        if boards[curr][move] == EMPTY:
            #Make a copy of the current board
            new_board = copy.deepcopy(boards)
            #Play a move in the new boards tile 
            new_board[curr][move] = AGENT
            node = Nodes(State(new_board,curr,move,AGENT),True)

            #Use minimax with depth to obtain score
            score = minimax(node,depth-1,alpha,beta,False) 
            #print('Score:',score)
            all_moves.append([move,score])

            #Update bestScore 
            if score > bestScore:
                bestScore = score
                bestMove = move
                #alpha = max(alpha, score)
            
    print("Best move:",bestMove)
    print("Best Score:",bestScore)
    return bestMove

'''
#ATTEMPT 1
def num_win_combinations(board,player):
    win_count = 0 

    #Check board rows
    for row in (1,4,7):
        #If player has 2-in-a-row (horizontally) and last tile is empty 
        if board[row] == board[row +1] == player and board[row+2] == EMPTY:
            win_count += 1

    #Check board columns
    for col in (1,2,3):
        #If player has 2-in-a-row (vertically) and last tile is empyt
        if board[col] == board[col + 3] == player and board[col + 6] == EMPTY:
            win_count += 1
    
    #Check board diagonals
    if board[1] == board[5] == player and board[9] == EMPTY:
        win_count += 1
    if board[3] == board[5] == player and board[7] == EMPTY:
        win_count += 1

    return win_count
'''  

#Minimax algorithm with alpha-beta pruning, evaluates and returns score for each move
def minimax(node, depth, alpha, beta, Maximizing):
    curr_state = node.state.current_state()
    #Return score if depth 0 reached or game ended
    if depth == 0 or curr_state > 0:
        return node.state.get_score()
    
    #Simulate Agents Turn
    if Maximizing:
        for move in range(1,10):
            new_node = node.new_Node(move)
            
            #Choose a different move if alreay taken
            if new_node == None:
                continue

            score = minimax(new_node,depth-1,alpha,beta,not Maximizing)
            alpha = max(alpha,score)
        
            #Alpha-Beta Pruning
            if alpha >= beta:
                break
        return alpha 
    
    #Simulate OPPONENTs Turn 
    else:
        for move in range(1,10):
            new_node = node.new_Node(move)

            #Choose a different move if already taken
            if new_node == None:
                continue

            score = minimax(new_node,depth-1,alpha,beta,not Maximizing)
            beta = min(beta,score)

            #Alpha-Beta Pruning
            if alpha >= beta:
                break
        return beta
    
'''
ATTEMPT #1
def minimax(board,curr,depth,alpha,beta,player):
    #The Agent has won the game
    if check_winner(board[curr],AGENT):
        print("_____WIN Detected_____")
        return 10000
    
    #The Opponent has won the game
    elif check_winner(board[curr],OPPONENT):
        print("_____LOSS Detected_____")
        return -10000
    
    #Game ends in a Draw
    elif check_draw(board[curr]):
        print("_____DRAW Detected_____")
        return 0
    
    elif depth == 0:
        score = eval_board(board[curr],AGENT,OPPONENT)
        print(score)
        print('board:',curr)
        return score
    

    #Simulate Agent's Turn 
    if player == OPPONENT:
        bestScore = MAX_EVAL

        for move in range(1,10):
            if board[curr][move] == EMPTY:
                boards[curr][move] = OPPONENT
                score = minimax(board,move,depth-1,alpha,beta,AGENT)
                boards[curr][move] = EMPTY

                if score < bestScore:
                    bestScore = score
                    beta = min(beta, score)
                
                #Prune Subtree
                if alpha >= beta:
                    break 
        return bestScore
    
    #Simulate Opponent's Turn
    else:
        bestScore = MIN_EVAL
        
        for move in range(1,10):
            if board[curr][move] == EMPTY:
                boards[curr][move] = AGENT
                score = minimax(board,move,depth-1,alpha,beta,OPPONENT)
                boards[curr][move] = EMPTY

                if score > bestScore:
                    bestScore = score
                    alpha = max(alpha,score)

                #Prune Subtree
                if alpha >= beta:
                    break
        return bestScore
'''


#====================================================================================>

# place a move in the global boards
def place( board, num, player ):
    global curr
    global moves
    curr = num
    boards[board][num] = player
    #Update move count
    moves += 1

# read what the server sent us and
# parse only the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    # init tells us that a new game is about to begin.
    # start(x) or start(o) tell us whether we will be playing first (x)
    # or second (o); we might be able to ignore start if we internally
    # use 'X' for *our* moves and 'O' for *opponent* moves.

    # second_move(K,L) means that the (randomly generated)
    # first move was into square L of sub-board K,
    # and we are expected to return the second move.
    if command == "second_move":
        # place the first move (randomly generated for opponent)
        place(int(args[0]), int(args[1]), 2)
        return play()  # choose and return the second move

    # third_move(K,L,M) means that the first and second move were
    # in square L of sub-board K, and square M of sub-board L,
    # and we are expected to return the third move.
    elif command == "third_move":
        # place the first move (randomly generated for us)
        place(int(args[0]), int(args[1]), 1)
        # place the second move (chosen by opponent)
        place(curr, int(args[2]), 2)
        return play() # choose and return the third move

    # nex_move(M) means that the previous move was into
    # square M of the designated sub-board,
    # and we are expected to return the next move.
    elif command == "next_move":
        # place the previous move (chosen by opponent)
        place(curr, int(args[0]), 2)
        return play() # choose and return our next move

    elif command == "win":
        print("Yay!! We win!! :)")
        return -1

    elif command == "loss":
        print("We lost :(")
        return -1

    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
