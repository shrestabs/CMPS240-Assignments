import math
import numpy as np
import random as random
import copy #TODO: eval if u need this

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.opposite = (2 if (player_number == 1) else (1))


#below 2 functions are used by alphabeta and expectimax
    def update_board(self, board, move, player_num):
        if 0 in board[:,move]:
            update_row = -1
            for row in range(1, board.shape[0]):
                update_row = -1
                if board[row, move] > 0 and board[row-1, move] == 0:
                    update_row = row-1
                elif row==board.shape[0]-1 and board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    board[update_row, move] = player_num
                    #self.c.itemconfig(self.gui_board[move][update_row], fill=self.colors[self.current_turn]) does not apply to 
                    break
        else:
            #can never come here
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)

    #TODO: move this function to a common helper class
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


        # is terminal state game_completed? 
    def terminal_test(self, board): 
        return self.game_completed(board, self.player_number)


    def utility(self, board):
        #https://stackoverflow.com/questions/10985000/how-should-i-design-a-good-evaluation-function-for-connect-4
        return np.random.randint(low=0, high=88, size=1)

    def get_alpha_beta_move(self, board):
        print(board) #check input
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
 
        # get best alpha(max) given all leafs choose min
        def max_value(self, depth, board, alpha, beta):
            print("Depth=",depth," alpha= ",alpha," beta= ",beta) #debug
            if (self.terminal_test(board) or (depth <= 0)):
                return self.utility(board)
            value = float("-inf")
            #valid columns are the actions
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            for col in range(len(valid_cols)):
                # Choose the max of 7 or less(valid) actions
                mockboard = copy.deepcopy(board)
                self.update_board(mockboard, col, self.player_number)
                value = max(value, min_value(self, depth-1, mockboard, alpha, beta))
                if (value >= beta):
                    alpha = max(alpha, value)
            return value

        # get best beta(min) given all leafs choose max
        def min_value(self, depth, board, alpha, beta):
            if (self.terminal_test(board) or (depth <= 0)):
                return self.utility(board)
            value = float("+inf")
            #valid columns are the actions
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:,col]:
                    valid_cols.append(col)

            for col in range(len(valid_cols)):
                # Choose the max of 7 or less(valid) actions
                mockboard = copy.deepcopy(board)
                self.update_board(mockboard, col, self.player_number)
                value = min(value, max_value(self, depth-1, mockboard, alpha, beta))
            return value

        #alpha beta algo that uses min-max
        depth = 7 
        value = max_value(self, depth, board, float("-inf"), float("+inf"))
        print("returned value ",value)
        if (value == 0):
            move = 1
        move = random.randint(0, 6) #had issues with numpy randomint. keep this
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
        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):
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
       
       
        return 0


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

