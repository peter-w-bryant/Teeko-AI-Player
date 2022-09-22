import random
import copy
import math
import numpy as np
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
         # TODO: implement a minimax algorithm to play better
        drop_phase = is_drop_phase(state)         # TODO: detect drop phase
        move = []
        if drop_phase:
            totalCount = 0;
            for i in range(5):
                for j in range(5):
                    if state[i][j] != ' ':
                        totalCount+=1
            if(totalCount == 0):
                newMove = (0,0)
            else:
                successors_states, legal_successors, source_idxs = succ(self, state)
                for i in range(len(successors_states)):
                    maxVal = -np.inf
                    compVal = minimax(self, successors_states[i], 2)
                    if(compVal > maxVal):
                        maxVal = compVal
                        newMove = legal_successors[i]

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            successors_states, legal_successors, source_idxs = succ(self, state)
            move = []
            for i in range(len(successors_states)):
                maxVal = -np.inf
                compVal = minimax(self, successors_states[i], 2)
                if(compVal > maxVal):
                    maxVal = compVal
                    newMove = legal_successors[i]
                    for key in source_idxs:
                        if(source_idxs[key] == newMove):
                            newSource = key # Insert the source coordinates to move tuple
            move.insert(1, newSource)
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            pass
        # select an unoccupied space randomly
        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, newMove)
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(len(state)):
            for j in range(len(state[i])):
                if(state[i][j] != ' '):
                    if((i, j) == (0,0) or (i, j) == (1,0) or (i, j) == (1,1) or (i, j) == (0,1)):
                        if(state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]):
                            return 1 if state[i][j]==self.my_piece else -1

        # TODO: check / diagonal wins
        for i in range(len(state)):
            for j in range(len(state[i])):
                if(state[i][j] != ' '):
                    if((i, j) == (0,4) or (i, j) == (0,3) or (i, j) == (1,4) or (i, j) == (1,3)):
                        if(state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]):
                            return 1 if state[i][j]==self.my_piece else -1

        # TODO: check box wins
        for i in range(len(state)):
            for j in range(len(state[i])):
                if(state[i][j] != ' '):
                    if((0<=j+1<=4) and (0<=i+1<=4)):
                        if(state[i][j] == state[i][j+1] == state[i+1][j] == state[i+1][j+1]):
                            return 1 if state[i][j]==self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# HELPER FUNCTIONS
#
############################################################################


def minimax(self, state, depth):
 
    if(self.game_value(state)):
        return self.game_value(state)
    elif(depth == 0):
        return heuristic_game_value(self, state)
    elif(depth % 2): # If it is MAX turn
        successors_states = succ(self, state)[0]     # List of legal successors for the current boards state
        min_list = np.zeros((len(successors_states)))
        for i in range(len(successors_states)):  
            min_list[i] = minimax(self, successors_states[i], (depth-1)) 
        return max(min_list)
    else: # If it is MIN turn
        successors_states = succ(self, state)[0]     # List of legal successors for the current boards state
        min_list = np.zeros((len(successors_states)))
        for i in range(len(successors_states)):
            min_list[i] = minimax(self, successors_states[i], (depth-1)) 
        return min(min_list)
    
# Evaluate non-terminal states. (you should call the game_value method from this function to determine whether the state is a 
# terminal state before you start evaluating it heuristically.)
def heuristic_game_value(self, state):    
    e_x = 0.0 # Heuristic game value function
    isTerminal = self.game_value(state)
    if(isTerminal): return 1
    # Criteria: Board position, how many are currently connected, distance between pieces
    # Non-Terminal Weights
    
    weights = [50,100,200]

    # ---
    ai_horizontal_2 = 0.0
    ai_horizontal_3 = 0.0
    ai_horizontal_4 = 0.0

    opp_horizontal_2 = 0.0
    opp_horizontal_3 = 0.0
    opp_horizontal_4 = 0.0

    # |
    ai_vertical_2 = 0.0
    ai_vertical_3 = 0.0
    ai_vertical_4 = 0.0

    opp_vertical_2 = 0.0
    opp_vertical_3 = 0.0
    opp_vertical_4 = 0.0

    #  /
    ai_updiag_2 = 0.0 
    ai_updiag_3 = 0.0 
    ai_updiag_4 = 0.0 

    opp_updiag_2 = 0.0 
    opp_updiag_3 = 0.0 
    opp_updiag_4 = 0.0 

    #  \
    ai_downdiag_2 = 0.0
    ai_downdiag_3 = 0.0
    ai_downdiag_4 = 0.0

    opp_downdiag_2 = 0.0
    opp_downdiag_3 = 0.0
    opp_downdiag_4 = 0.0

    # 2x2 Square
    ai_square_2 = 0.0
    ai_square_3 = 0.0
    ai_square_4 = 0.0

    opp_square_2 = 0.0
    opp_square_3 = 0.0
    opp_square_4 = 0.0

    # Calculate AI Piece weight(#Ai piece- #User Piece) + weight2(#Ai piece- #User Piece) + ...
    for row in range(5):
            for col in range(5):
                # AI Horizontal Counts
                if(state[row][col] == self.my_piece):
                    if((0 <=col+1 <= 4) and state[row][col+1] == self.my_piece):
                        ai_horizontal_2 = 1
                        if((0 <=col+2 <= 4) and state[row][col+2] == self.my_piece):
                            ai_horizontal_3 = 1
                            if((0 <=col+3 <= 4) and state[row][col+3] == self.my_piece):
                                ai_horizontal_4 = 1

                # Opp Horizontal Counts 
                if(state[row][col] == self.opp):
                    if((0 <=col+1 <= 4) and state[row][col+1] == self.opp):
                        opp_horizontal_2 = 1
                        if((0 <=col+2 <= 4) and state[row][col+2] == self.opp):
                            opp_horizontal_3 = 1
                            if((0 <=col+3 <= 4) and state[row][col+3] == self.opp):
                                opp_horizontal_4 = 1

                # AI Vertical Counts
                if(state[row][col] == self.my_piece):
                    if((0 <=row+1 <= 4) and state[row+1][col] == self.my_piece):
                        ai_vertical_2= 1
                        if((0 <=row+2 <= 4) and state[row+2][col] == self.my_piece):
                            ai_vertical_3 = 1
                            if((0 <=row+3 <= 4) and state[row+3][col] == self.my_piece):
                                ai_vertical_4 = 1

                # Opp Vertical Count
                if(state[row][col] == self.opp):
                    if((0 <=row+1 <= 4) and state[row+1][col] == self.opp):
                        opp_vertical_2= 1
                        if((0 <=row+2 <= 4) and state[row+2][col] == self.opp):
                            opp_vertical_3 = 1
                            if((0 <=row+3 <= 4) and state[row+3][col] == self.opp):
                                opp_vertical_4 = 1

                # AI Updiagonal Count (/)
                if(state[row][col] == self.my_piece):
                        if((0 <=row+1 <= 4) and (0 <=col-1 <= 4) and state[row+1][col-1] == self.my_piece):
                            ai_updiag_2= 1
                            if((0 <=row+2 <= 4) and (0 <=col-2 <= 4) and state[row+2][col-2] == self.my_piece):
                                ai_updiag_3 = 1
                                if((0 <=row+3 <= 4) and (0 <=col-3 <= 4) and state[row+3][col-3] == self.my_piece):
                                    ai_updiag_4 = 1

                # Opp Updiagonal Count (/)
                if(state[row][col] == self.opp):
                    if((0 <=row+1 <= 4) and (0 <=col-1 <= 4) and state[row+1][col-1] == self.opp):
                        opp_updiag_2= 1
                        if((0 <=row+2 <= 4) and (0 <=col-2 <= 4) and state[row+2][col-2] == self.opp):
                            opp_updiag_3 = 1
                            if((0 <=row+3 <= 4) and (0 <=col-3 <= 4) and state[row+3][col-3] == self.opp):
                                opp_updiag_4 = 1

                
                # AI Down-diagonal Count (\)
                if(state[row][col] == self.my_piece):
                        if((0 <=row+1 <= 4) and (0 <=col+1 <= 4) and state[row+1][col+1] == self.my_piece):
                            ai_downdiag_2 = 1
                            if((0 <=row+2 <= 4) and (0 <=col+2 <= 4) and state[row+2][col+2] == self.my_piece):
                                ai_downdiag_3 = 1
                                if((0 <=row+3 <= 4) and (0 <=col+3 <= 4) and state[row+3][col+3] == self.my_piece):
                                    ai_downdiag_4 = 1

                # Opp Down-diagonal Count (\)
                if(state[row][col] == self.opp):
                    if((0 <=row+1 <= 4) and (0 <=col+1 <= 4) and state[row+1][col+1] == self.opp):
                        opp_updiag_2= 1
                        if((0 <=row+2 <= 4) and (0 <=col+2 <= 4) and state[row+2][col+2] == self.opp):
                            opp_updiag_3 = 1
                            if((0 <=row+3 <= 4) and (0 <=col+3 <= 4) and state[row+3][col+3] == self.opp):
                                opp_updiag_4 = 1

                # AI 2x2 Square Count ([])
                    if(state[row][col] == self.my_piece):
                        if((0 <=row <= 4) and (col+1 <= 4) and state[row][col+1] == self.my_piece):
                            ai_square_2 = 1
                        if((0 <=row+1 <= 4) and (col <= 4) and state[row+1][col] == self.my_piece):
                            ai_square_3 = 1
                        if((0 <=row+1 <= 4) and (col+1 <= 4) and state[row+1][col+1] == self.my_piece):
                            ai_square_4 = 1

                # AI 2x2 Square Count ([])
                if(state[row][col] == self.opp):
                    if((0 <=row <= 4) and (col+1 <= 4) and state[row][col+1] == self.opp):
                            opp_square_2 = 1
                    if((0 <=row+1 <= 4) and (col <= 4) and state[row+1][col] == self.opp):
                            opp_square_3 = 1
                    if((0 <= row+1 <= 4) and (col+1 <= 4) and state[row+1][col+1] == self.opp):
                            opp_square_4 = 1
                        
                        
                
    # Add the HORIZONTAl sum of features to e_x
    e_x = weights[0] * (ai_horizontal_2-opp_horizontal_2) +  weights[1] * (ai_horizontal_3-opp_horizontal_3) + weights[2] * (ai_horizontal_4-opp_horizontal_4)
    # Add the VERTICAL sum of features to e_x
    e_x = e_x +  weights[0] * (ai_vertical_2-opp_vertical_2) +  weights[1] * (ai_vertical_3-opp_vertical_3) + weights[2] * (ai_vertical_4-ai_vertical_4)
     # Add the UPPER DIAGNONAL (/) sum of features to e_x
    e_x = e_x +  weights[0] * (ai_updiag_2-opp_updiag_2) +  weights[1] * (ai_updiag_3-opp_updiag_3) + weights[2] * (ai_updiag_4-opp_updiag_4)
    # Add the DOWN DIAGNONAL (\) sum of features to e_x
    e_x = e_x +  weights[0] * (ai_downdiag_2-opp_downdiag_2) +  weights[1] * (ai_downdiag_3-opp_downdiag_3) + weights[2] * (ai_downdiag_4-opp_downdiag_4)   
    # Add the 2X2 SQUARE (\) sum of features to e_x
    e_x = e_x +  10 * (ai_square_2-opp_square_2) +  10 *  (ai_square_3-opp_square_3) + 10 *  (ai_square_4-opp_square_4) 
    
    e_x = e_x / 300
    return e_x
    

def succ(self, state):
    """ takes in a board state and returns a list of all the legal successors states. During the drop phase, this simply means
        adding a new piece of the current player's type to the board; during continued
        gameplay, this means moving any one of the current player's pieces to an unoccupied
        location on the board, adjacent to that piece. 
    """
    source_idx = {}
    legal_successors = []
    successors_states = []
    # If it is the drop phase, find all coordinate tuples for all available spaces

    if(is_drop_phase(state)):
        for row in range(len(state)):
            for col in range(len(state[row])):
                if(state[row][col] == ' '):
                    newState = copy.deepcopy(state)
                    newState[row][col] = self.my_piece
                    successors_states.append(newState)
                    legal_successors.append((row, col))
                    source_idx[(row, col)] = (row, col)
                    
    else:
    # If it is not the drop phase, find all coordinate tuples for all adjacent spaces
        for row in range(len(state)):
            for col in range(len(state[row])):
                if(state[row][col] == self.my_piece):
                    for i in range(-1,2,1):
                        for j in range(-1,2,1):
                            if((0<=(row+i)<=4) and (0<=(col+j)<=4)):
                                if((state[row+i][col+j] == ' ')):
                                    newState = copy.deepcopy(state)
                                    newState[row][col] = ' '
                                    newState[row+i][col+j] = self.my_piece
                                    successors_states.append(newState)
                                    source_idx[(row, col)] = (row+i, col+j)
                                    legal_successors.append((row+i, col+j))
            
    return successors_states, legal_successors, source_idx


def is_drop_phase(state):
    """
    Returns true if the state of the game is currently in the drop phase, false otherwise
    """
    #  In the "drop phase", the state will contain less than 8 elements which are not ' ' (a single space character).
    markerCount = 0;
    for row in state:
        for i in range(len(row)):
            if row[i] != ' ':
                markerCount+=1
    if(markerCount < 8):
        return True
    return False

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
