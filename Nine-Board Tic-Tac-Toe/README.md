In this assignment you will be writing an agent to play the game of Nine-Board Tic-Tac-Toe. This game is played on a 3 x 3 array of 3 x 3 Tic-Tac-Toe boards. The first move is made by placing an X in a randomly chosen cell of a randomly chosen board. After that, the two players take turns placing an O or X alternately into an empty cell of the board corresponding to the cell of the previous move. (For example, if the previous move was into the upper right corner of a board, the next move must be made into the upper right board.)

The game is won by getting three-in-a row either horizontally, vertically or diagonally in one of the nine boards. If a player is unable to make their move (because the relevant board is already full) the game ends in a draw.


 Our program combines Alpha-Beta pruning with logic, object-oriented programming, and data structure functionality to create 
an artificially intelligent agent which can defeat other agents with above-average to good intelligence. 
Several classes along with data structures like 2D arrays and lists have been used to store the current board and game state information.

 _____________________________________________________________________IMPLEMENTATION:_______________________________________________________________________

   The algorithm begins by evaluating the state of the current board. For every turn of the agent, 
   a copy of the original board is made, and the best move is found by calculating efficiency of each legally allowed play on that board. 

   We use Minimax, as explained above, and a custom-designed scoring logic to determine the most optimal move by finding all future moves 
   post committing a move to the current board and assigning it a score based on how well its subtrees perform. 
   We do this for all possible moves and choose the move with the highest score, as the agent will have a higher chance of winning by proceeding 
   down the subtree.

   This is repeated till the opponent wins or a move by the agent on the current board forms a winning combination, leading to the agent winning.

____________________________________________________________________SCORE CALCULATON:______________________________________________________________________

   We calculate the score of each board by weighing the number of marks placed by the agent and the number of marks placed by the opponent against 
   the 8 possible tic-tac-toe winning combinations. 
   The frequency and placement of marks in each row and column total out to a temporary score which gets added to the final score of the board.

   Agent and opponent scores are initialised to zero.

   Assume the board is

    X X O
    . . .
    X O . 

   While checking for 3 in a row, for example in row 1, for every instance of the agent’s mark, the temporary score is increased by 10 times the
   previous score. 
   The first X increases the score to 10, while the second one increases it to 100. 
   However, the third place is occupied by the opponent so the first and second marks are nullified since the combo can not be completed.

#   For column 1, the two Xs add on to weigh 100 and are added to the final score.
#
#   For row 3, the X and O get cancelled out so the final total score of the board is 100. 
