#!/usr/bin/env python3

#=========================================================================================================================================================>
#                                                                   COMP3411 Assignment 3                                                                   
#                                                               Nine-Board Tic-Tac-Toe Agent
#                                                                    Program:  states.py     
#
#                                                             by: Ayusha Priyadarshani (z5452784) 
#                                                                 Aryaman Sakthivel    (z5455785)
#  
# ==========================================================================================================================================================>


EMPTY = 0

#Class States used to save a copy the current board and evaluate it 
class State:

    def __init__(self,board,curr,move,player):
        self.board = board  # game: is the deepcopy of the entire 9board
        self.curr = curr    # curr: is the numeric value pointing to the current subboard
        self.move = move    # move: is the last move made by the player
        self.player = player


    #Returns the score from the heuristic function
    def get_score(self):
        return self._heuristic()
    
    #Copy the game board
    def _copy(self, board):
        new_board = [[0] * 10]
        for n in range(1, 10):
            new_board.append(board[n].copy())
        return new_board
    
    #Creates a new state if the move is valid
    def new_state(self,new_move,player):
        if self.board[self.move][new_move] == EMPTY:
            new_board = self._copy(self.board)
            new_board[self.move][new_move] = player
            
            #Return the new board 
            return State(new_board,self.move,new_move,player)
        
        return None
    #Get state of the board
    # State = 0 : No winner
    # State = 1 : AGENT wins
    # State = 2 : OPPONENT wins
    def current_state(self):
        
        #Get the current playing board
        curr_game = self.board[self.curr]

        #Check for 3-in-a-row (Horizontal Rows)
        for row in range(1,4,7):
            if curr_game[row] > EMPTY and curr_game[row] == curr_game[row + 1] == curr_game[row + 2]:
                return curr_game[row]

        #Check for 3-in-a-row (Vertical Columns)
        for col in range(1,2,3):
            if curr_game[col] > EMPTY and curr_game[col] == curr_game[col + 3] == curr_game[col + 6]:
                return curr_game[col]
        
        #Check for 3-in-a-row Diagonally
        if curr_game[1] > EMPTY and curr_game[1] == curr_game[5] == curr_game[9]:
            return curr_game[1]
        if curr_game[3] > EMPTY and curr_game[3] == curr_game[5] == curr_game[7]:
            return curr_game[3]

        # No wins were found
        return 0
    
    
    
    #Heuristic function used to calculate the score of the current board
    def _heuristic(self):
        score = 0

        #List of winning combinations
        winning_combos = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]]
        #Weightage of positions
        weightage = [[0, -10, -100, -1000],
            [10, 0, 0, 0],
            [100, 0, 0, 0],
            [1000, 0, 0, 0]]

        #Evaluate board for each move
        for moves in range(1,10):
            curr_board = self.board[moves]

            for i in range(0,8):
                #Initialize counters
                temp = agent = opponent = 0

                for j in range(0,3):
                    cur = curr_board[winning_combos[i][j]]
                    if cur == 1: # 1 - we played here
                        agent += 1

                    elif cur == 2: # 2 - opponent played here
                        opponent += 1

                temp = weightage[agent][opponent] #score based on the current cells relation to the board and choice

                #If current tile is the main board the 'temp' score is doubled
                if moves == self.curr:
                    temp *= 2
                #If current tile is the chosen board the 'temp' score is tripled
                elif moves == self.move:
                    temp *= 3
                score += temp

        #Return the score 
        return score
                   





#class State:
    # game is a copy of the entire board
    # current_board tracks which board we are in
    # choice is the move we choose
    #def __init__(self, game, current_board, choice, player):
        #self.board = game
        #self.curr = current_board
        #self.move = choice
        #self.player = player


    def get_score(self):
        return self._heuristic()

    def _copy(self, game):
        new_game = [[0] * 10]
        for num in range(1, 10):
            new_game.append(game[num].copy())
        return new_game

    def new_state(self, new_choice, player):
        if self.board[self.move][new_choice] > 0:
            # illegal
            return None
        # copy current board and place new choice
        new_game = self._copy(self.board)
        new_game[self.move][new_choice] = player
        return State(new_game, self.move, new_choice, player)

    # get current state
    # 0 -> no wins
    # 1 -> AI wins
    # 2 -> opponent wins
    def current_state(self):
        win = 0
        curr_game = self.board[self.curr]

        # check rows
        for i in range(1, 4):
            start = i * 3 - 2
            if curr_game[start] > 0 and curr_game[start] == curr_game[start + 1] == curr_game[start + 2]:
                return curr_game[start]

        # check columns
        for i in range(1, 4):
            if curr_game[i] > 0 and curr_game[i] == curr_game[i + 3] == curr_game[i + 6]:
                return curr_game[i]
        
        # check diagonals
        if curr_game[1] > 0 and curr_game[1] == curr_game[5] == curr_game[9]:
            return curr_game[1]
        if curr_game[3] > 0 and curr_game[3] == curr_game[5] == curr_game[7]:
            return curr_game[3]

        # no wins
        return win

    def _heuristic(self):
        score = 0
        all_wins = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5, 8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]]
        weight = [[0, -10, -100, -1000],
            [10, 0, 0, 0],
            [100, 0, 0, 0],
            [1000, 0, 0, 0]]

        for num in range(1, 10):
            curr_board = self.board[num]
            for i in range(0, 8):
                temp = player = opponent = 0
                for j in range(0, 3):
                    curr = curr_board[all_wins[i][j]]
                    if curr == 1:
                        player += 1
                    elif curr == 2:
                        opponent += 1
                temp = weight[player][opponent]
                if num == self.curr:
                    temp *= 2
                elif num == self.move:
                    temp *= 3
                score += temp
    
        return score
