import math
import numpy as np
import random as random
import copy

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.opposite = (2 if (player_number == 1) else (1))
        print("opposite number is ",self.opposite)

    #Helper functions to update and check if game is complete
    def update_board(self, board, move, player_num):
        mockboard = copy.deepcopy(board)
        if 0 in mockboard[:,move]:
            update_row = -1
            for row in range(1, mockboard.shape[0]):
                update_row = -1
                if mockboard[row, move] > 0 and mockboard[row-1, move] == 0:
                    update_row = row-1
                elif row==mockboard.shape[0]-1 and mockboard[row, move] == 0:
                    update_row = row
                if update_row >= 0:
                    mockboard[update_row, move] = player_num
                    break
        else:
            err = 'in AI game Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)
        return mockboard

    def game_completed(self, board, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))

 
    def terminal_test(self, board, player_number): 
        return self.game_completed(board, player_number)

    #sum of all possible wins available at a particular board position
    def evaluation_function(self, board):
        wellness = 0
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        '''
        Factors identfied for defense play:
        1)Component My winning (+)(x1) (magnitude)(weight=negligible)
        2)Component Opponent winning score (-)(x2)(magnitude)(weight=almost infinity)
        3)Component Blocking/Attempting draw (Constant)(weight=very high)
        '''
        def scorecalculator(zeros, player_count, opponent_count):
            score = 50
            if(zeros == 4):
                return score
            if ((player_count == 0) or (opponent_count == 0)):
                score = ( ((player_count/3) * 50) + ((opponent_count/3) * -10000) )
            else:
                if ((player_count + opponent_count) == 4):
                    score = 20000
                else:
                    score = 10000
            return score

        for i in range(6):
            for j in range(7):
                #horizontal right
                if ((j+3) < 7):
                    #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        #print("(i,j,k) :",i,j,k)
                        statsdict[board[i][j+k]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
                #horizontal left
                if ((j-3) >= 0):
                    #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        statsdict[board[i][j-k]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
                #vertical up
                if ((i+3) < 6):
                     #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        statsdict[board[i+k][j]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
                #vertical bottom
                if ((i-3) >=0):
                     #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        statsdict[board[i-k][j]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
                #diagonal right up
                if (((j+3) < 7) and ((i+3) < 6)):
                    #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        statsdict[board[i+k][j+k]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
                #diagonal left down
                if (((j-3) >= 0) and ((i-3) >= 0)):
                    #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        statsdict[board[i-k][j-k]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
                #diagonal left up
                if (((j-3) >= 0) and ((i+3) < 6)):
                    #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        statsdict[board[i+k][j-k]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
                #diagonal right down
                if (((j+3) < 7) and ((i-3) >= 0)):
                    #collect stats
                    statsdict = {0:0, 1:0, 2:0}
                    for k in range(4):
                        statsdict[board[i-k][j+k]] += 1
                        k = k + 1
                    wellness += scorecalculator(statsdict[0], statsdict[1], statsdict[2])
        return wellness



    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
 
        def max_value(self, depth, board, alpha, beta, incol):
            if (self.terminal_test(board, self.player_number) or (depth <= 0)):
                return (self.evaluation_function(board), incol)
            value = float("-inf")
            retcol = incol
            #valid columns or actions
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            for col in valid_cols:
                # Choose the max of 7 or less(valid) actions
                mockboard = self.update_board(board, col, self.player_number)
                retvalue, colz =  min_value(self, depth-1, mockboard, alpha, beta, col)
                print("max-min_value returned ",retvalue, colz)
                if (retvalue > value):
                    value = retvalue
                    retcol = colz
                if (value >= beta):
                    return value, col
                alpha = max(alpha, value)
            return value, retcol

        # get best beta(min) given all leafs choose max
        def min_value(self, depth, board, alpha, beta, incol):
            if (self.terminal_test(board, self.opposite) or (depth <= 0)):
                return (self.evaluation_function(board), incol)
            value = float("+inf")
            retcol = incol
            #valid columns are the actions
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            for col in valid_cols:
                # Choose the max of 7 or less(valid) actions
                mockboard = self.update_board(board, col, self.opposite)
                retvalue, colz = max_value(self, depth-1, mockboard, alpha, beta, col)
                print("min max_val returned ",retvalue, colz)
                if (retvalue < value):
                    value = retvalue
                    retcol = colz
                if (value <= alpha):
                    return value, col
                beta = min(beta, value)
            return value, retcol

        #alpha beta algo that uses min-max
        depth = 4
        value, move = max_value(self, depth, board, float("-inf"), float("+inf"), -1)
        print("returned value and move ",value," ",move)
        return move

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        def max_value(self,depth, board, col):
            val = float("-inf")
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            for col in valid_cols:
                retval, colz = value(self, depth-1,"exp", board,col)
                if (retval > val):
                    val = retval
                    col = colz
            return val,col

        def exp_value(self,depth, board, col):
            val = 0
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            for col in valid_cols:
                p = 1/len(valid_cols)
                retval, colz = value(self, depth-1,"max", board, col)
                val += p * retval
            return val,col

        def value(self, depth, turn, board, col):
            print("Max at Depth=",depth)  #debug
            mockboard = copy.deepcopy(board)
            if (self.terminal_test(mockboard, self.player_number) or (depth <= 0)):
                return (self.evaluation_function(mockboard), col)

            if (turn == "max"):
                return max_value(self,depth, board, col)
            else:
                return exp_value(self,depth, board, col)

        depth = 3
        val, move = value(self, depth, "max", board, -1)
        return move


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move