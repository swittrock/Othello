WHITE = 'W'
BLACK = 'B'
NONE = '.'

class Game_state:
    def __init__(self,board,turn,win,rows,columns):
        self.row_num = rows
        self.column_num = columns
        self.board_state = board
        self.turn = turn
        self.win = win

    def _valid_block(self,player_move:list, result_list:list, turn) -> bool:
        '''function used to simploify the validity checking function'''
        direction_name = True

        if result_list == [] or self.board_state[player_move[0]][player_move[1]] != NONE:
            direction_name = False
        elif result_list[0] == NONE or result_list[0] == turn:
            direction_name = False
        elif turn not in result_list:
            direction_name = False
        else:
            direction_name = True
        return direction_name

    def opposite_turn(self):
        if self.turn == WHITE:
            return BLACK
        else:
            return BLACK

    def chip_count(self)-> dict:
        '''Counts all chips on the board and stores them in a dictionary'''
        count_dict = {'Black':0,'White':0}
        for row in self.board_state:
            for piece in row:
                if piece == 'W':
                    count_dict['White']+=1
                elif piece == 'B':
                    count_dict['Black']+=1
        return count_dict

    def board_full(self):
        '''Checks to see if every space on the board is occupied'''
        for row in self.board_state:
            for item in row:
                if item == NONE:
                    return False
        return True

    def player_turn(self):
        '''Alternates the value for turn'''
        if self.turn == WHITE:
            return BLACK
        else:
            return WHITE

    def determine_winner(self):
        '''Counts the chips of both players and compares them based off the determined win condition
        to decide who wins'''
        if self.win == '>':
            if self.chip_count()== None:
                print('WINNER: NONE')
                return None
            if self.chip_count()['White'] > self.chip_count()['Black']:
                print('B: {}  W: {}'.format(self.chip_count()['Black'],self.chip_count()['White']))
                self.display_board()
                print('WINNER: W')
            if self.chip_count()['White'] < self.chip_count()['Black']:
                print('B: {}  W: {}'.format(self.chip_count()['Black'], self.chip_count()['White']))
                self.display_board()
                print('WINNER: B')
            elif self.chip_count()['White'] == self.chip_count()['Black']:
                print('B: {}  W: {}'.format(self.chip_count()['Black'], self.chip_count()['White']))
                self.display_board()
                print('WINNER: NONE')
        if self.win == '<':
            if self.chip_count()== None:
                print('B: {}  W: {}'.format(self.chip_count()['Black'], self.chip_count()['White']))
                self.display_board()
                print('WINNER: NONE')
            if self.chip_count()['White'] < self.chip_count()['Black']:
                print('B: {}  W: {}'.format(self.chip_count()['Black'], self.chip_count()['White']))
                self.display_board()
                print('WINNER: W')
            if self.chip_count()['White'] > self.chip_count()['Black']:
                print('B: {}  W: {}'.format(self.chip_count()['Black'], self.chip_count()['White']))
                self.display_board()
                print('WINNER: B')
            elif self.chip_count()['White'] == self.chip_count()['Black']:
                print('B: {}  W: {}'.format(self.chip_count()['Black'], self.chip_count()['White']))
                self.display_board()
                print('WINNER: NONE')

    def determine_winner_name(self):
        if self.win == '>':
            if self.chip_count()== None:
                return 'WINNER: NONE'
            if self.chip_count()['White'] > self.chip_count()['Black']:
                return 'WINNER: W'
            if self.chip_count()['White'] < self.chip_count()['Black']:
                return 'WINNER: B'
            elif self.chip_count()['White'] == self.chip_count()['Black']:
                return 'WINNER: NONE'
        if self.win == '<':
            if self.chip_count()== None:
                return 'WINNER: NONE'
            if self.chip_count()['White'] < self.chip_count()['Black']:
                return 'WINNER: W'
            if self.chip_count()['White'] > self.chip_count()['Black']:
                return 'WINNER: B'
            elif self.chip_count()['White'] == self.chip_count()['Black']:
                return 'WINNER: NONE'


    def check_all_directions(self,player_move:list, turn) -> (bool, list):
        '''Checks the given move in all directions and returns a bool, if True then there
            is a valid move in at least one direction, if False there are no valid moves'''

        valid_list = []

        try:
            if self.board_state [player_move[0] + 1] [player_move[1]] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[0] + 1 <= self.row_num:
                valid_list.append((True, 'Vertical Down'))
            else:
                valid_list.append((False,'Vertical Down'))
        except:
            valid_list.append((False, 'Vertical Down'))
        try:
            if self.board_state [player_move[0] - 1] [player_move[1]] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[0] - 1 >= 0:
                valid_list.append((True, 'Vertical Up'))
            else:
                valid_list.append((False, 'Vertical Up'))
        except:
            valid_list.append((False, 'Vertical Up'))
        try:
            if self.board_state [player_move[0]] [player_move[1] + 1] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[1] + 1 <= self.column_num:
                valid_list.append((True, 'Horizontal Right'))
            else:
                valid_list.append((False, 'Horizontal Right'))
        except:
            valid_list.append((False, 'Horizontal Right'))
        try:
            if self.board_state [player_move[0]] [player_move[1] - 1] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[1] - 1 >= 0 :
                valid_list.append((True, 'Horizontal Left'))
            else:
                valid_list.append((False, 'Horizontal Left'))
        except:
            valid_list.append((False, 'Horizontal Left'))
        try:
            if self.board_state [player_move[0] + 1] [player_move[1] + 1] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[0] + 1 <= self.row_num \
                    and player_move[1] + 1 <= self.column_num :
                valid_list.append((True, 'Diagonal Down Right'))
            else:
                valid_list.append((False, 'Diagonal Down Right'))
        except:
            valid_list.append((False, 'Diagonal Down Right'))

        try:
            if self.board_state [player_move[0] + 1] [player_move[1] - 1] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[0] + 1 <= self.row_num \
                    and player_move[1] - 1 >= 0 :
                valid_list.append((True, 'Diagonal Down left'))
            else:
                valid_list.append((False, 'Diagonal Down left'))
        except:
            valid_list.append((False, 'Diagonal Down left'))

        try:
            if self.board_state [player_move[0] - 1] [player_move[1] + 1] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[0] - 1 >= 0 \
                    and player_move[1] + 1 <= self.column_num :
                valid_list.append((True, 'Diagonal Up Right'))
            else:
                valid_list.append((False, 'Diagonal Up Right'))
        except:
            valid_list.append((False, 'Diagonal Up Right'))

        try:
            if self.board_state [player_move[0] - 1] [player_move[1] - 1] == self.opposite_turn() and\
                self.board_state[player_move[0]][player_move[1]] == NONE and player_move[0] - 1 >= 0 \
                    and player_move[1] - 1 >= 0 :
                valid_list.append((True, 'Diagonal Up Left'))
            else:
                valid_list.append((False, 'Diagonal Up Left'))
        except:
            valid_list.append((False, 'Diagonal Up Left'))

        for x in valid_list:
            if x[0] == True:
                return (True,valid_list)

        return (False,valid_list)

    def flip_all_valids(self, player_move:list) -> list:
        '''Checks each direction to see if it is a valid move and then flips all chips in each valid direction'''
        down = False
        up = False
        right = False
        left = False
        d_down_right = False
        d_down_left = False
        d_up_right = False
        d_up_left = False

        directions = [up,down,right,left,d_down_right,d_down_left,d_up_right,d_up_left]

        '''0 = vertical down | 1 = vertical up | 2 = horizontal right |
           3 = horizontal left | 4 = diagonal down right | 5 = diagonal down left|
           6 = diagonal up right | 7 = diagonal up left |'''

        #flip down

        if self.check_all_directions(player_move, self.turn)[1][0][0] == True:
            directions[0] = True
            self.board_state[player_move[0] + 1][player_move[1]] = self.turn

        #flip up

        if self.check_all_directions(player_move, self.turn)[1][1][0] == True:
            directions[1] = True
            self.board_state[player_move[0] - 1][player_move[1]] = self.turn

        #flip right

        if self.check_all_directions(player_move, self.turn)[1][2][0] == True:
            directions[2] = True
            self.board_state[player_move[0]][player_move[1] + 1] = self.turn

        #flip left

        if self.check_all_directions(player_move, self.turn)[1][3][0] == True:
            directions[3] = True
            self.board_state[player_move[0]][player_move[1] - 1] = self.turn

        # flip diagonal down right

        if self.check_all_directions(player_move, self.turn)[1][4][0] == True:
            directions[4] = True
            self.board_state[player_move[0] + 1][player_move[1] + 1] = self.turn

        # flip diagonal down left

        if self.check_all_directions(player_move, self.turn)[1][5][0] == True:
            directions[5] = True
            self.board_state[player_move[0] + 1][player_move[1] - 1] = self.turn

        # flip diagonal up right

        if self.check_all_directions(player_move, self.turn)[1][6][0] == True:
            directions[6] = True
            self.board_state[player_move[0] - 1][player_move[1] + 1] = self.turn

        # flip diagonal up left
        if self.check_all_directions(player_move, self.turn)[1][7][0] == True:
            directions[7] = True
            self.board_state[player_move[0] - 1][player_move[1] - 1] = self.turn

        for x in directions:
            if x == True:
                self.board_state[player_move[0]][player_move[1]] = self.turn

        return self.board_state


    def check_both_possible_move(self):
        for x in range(self.row_num):
            for y in range(self.column_num):
                if self.check_all_directions([x,y] , self.turn)[0] == True:
                    return True
                if self.check_all_directions([x,y] , self.player_turn())[0] == True:
                    return True
        return False

    def check_single_valid_move(self):
        for x in range(self.row_num):
            for y in range(self.column_num):
                if self.check_all_directions([x,y] , self.turn)[0] == True:
                    return True
        return False

    def display_board(self):
        for x in self.board_state:
            print(' '.join(x))

    #def check_simplified

# board = \
#     [['.', '.', 'B'],
#      ['.', '.', 'B'],
#      ['.', '.', 'B'],
# ]
#
# x = Game_state(board,'W','>',3,3)
#
# for y in x.check_all_directions([0,0],x.turn)[1]:
#     print(y)
#
# for x in x.flip_all_valids([1,1]):
#     print(x)
