from faller_class import Faller
import random
from collections import namedtuple

class InvalidColumnError(Exception):
    '''Raised whenever the user tries to drop a faller into a column number that does not exist'''
class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass
class GameOverError(Exception):
    '''Raised whenever a move is made after the game is over'''
    pass

COLORS = ('R', 'O', 'Y', 'G', 'B', 'I', 'P')

Match = namedtuple('Match', ['delta', 'num'])

class Field:
    def __init__(self, field: list[list[str]]) -> None:
        '''Initializes variables'''
        self.cols = 6
        self.rows = 13
        self.field = field
        self.field_wo_faller = self._copy_field(field)
        self.faller = []
        self.need_new_faller = True
        self.matching = True
        self.game_over = False
    def _copy_field(self, field: list[list[str]]) -> list[list[str]]:
        '''Makes a copy of the current field'''
        field_copy = []

        for col in field:
            col_copy = []
            for row in col: 
                col_copy.append(row)
            field_copy.append(col_copy)

        return field_copy
    def _update_field(self, new_col: int):
        '''
        Updates the field when the faller changes (in position or in state) if the change is possible. 
        Raises an InvalidMoveError if the move is invalid.
        '''
        faller = self.faller
        field = self._copy_field(self.field_wo_faller)
        col = field[new_col]
        spot = faller.faller_spot - 1 # faller should remain in the same level

        for i in range(faller.faller_num):
            new_square = col[spot - i]
            if new_square[1] in COLORS and new_square[0] == ' ': # check if the there are any frozen blocks in this square
                raise InvalidMoveError
        
        self._change_faller_state(new_col)

        if faller.faller_spot < len(col) and col[faller.faller_spot] == '   ':
            faller.fall()

        for i in range(faller.faller_num):
            col[spot - i] = faller.faller[i] 

        faller.change_faller_col(new_col)
        self.field = field
    def _generate_rand_colors(self):
        '''Generates 3 random colors to create a faller'''
        rand_nums = []
        for num in range(3):
            rand_num = random.randint(0, len(COLORS) - 1)
            rand_nums.append(rand_num)
        
        colors_str = f'{COLORS[rand_nums[0]]} {COLORS[rand_nums[1]]} {COLORS[rand_nums[2]]}'
        return colors_str 
    def create_faller(self):
        '''Creates a faller object only if the previous faller object has already been frozen'''
        colors = self._generate_rand_colors()
        col_num = random.randint(0, self.cols - 1)

        # do not drop a faller in a column that is already filled
        while '   ' not in self.field[col_num]:
            col_num = random.randint(0, self.cols - 1)

        if self.game_over:
            raise GameOverError
        else:
            if self.faller == []: 
                # creates the very first faller
                if self._is_valid_column_number(col_num):
                    self.faller = Faller(colors, col_num)
                else:
                    raise InvalidColumnError

            if self.faller.frozen:
                if self._is_valid_column_number(col_num):
                    self.faller = Faller(colors, col_num)
                else:
                    raise InvalidColumnError

        self.faller.change_faller_col(col_num)
        self.need_new_faller = False
        self.matching = False
    def _change_faller_state(self, new_col: int):
        '''
        Depending on the previous state of the faller and the next square the faller is going to fall into,
        change the state of the faller accordingly
        '''
        faller = self.faller
        column = self.field[new_col]
        if faller.faller_spot < (len(column) - 1) and column[faller.faller_spot] == '   ' and column[faller.faller_spot + 1] == '   ':
            faller.fall()
        elif not faller.landed:
            faller.land()
        else:
            faller.freeze()
    def _change_faller_state_in_field(self):
        '''Change the state of the faller in the field to the actual state of the faller'''
        faller = self.faller
        column = self.field[faller.faller_col] 
        if faller.faller_num == 0:
            column[faller.faller_spot] = faller.faller[0]

        for i in range(faller.faller_num):
            if self._is_valid_row_number(faller.faller_spot - i):
                column[faller.faller_spot - i] = faller.faller[i]
    def _faller_drop(self, faller: Faller, column: list):
        '''Has the faller drop down a level if there is an empty space underneath it'''
        if faller.faller_num < 3:
            for num in range(faller.faller_num + 1):
                column[faller.faller_spot - num] = faller.faller[num]

            faller.add_to_faller_num()
        else:
            column.pop(faller.faller_spot)
            column.insert(0, '   ')

        faller.add_to_faller_spot()
    def _faller_freeze(self, faller: Faller):
        '''
        Has the faller go inot the freeze state if there are no matches.
        Goes through the matching process if there are matches.
        If the faller does not fit in the field, the game ends.
        '''
        faller.faller_spot -= 1
        self._change_faller_state_in_field()
        if faller.faller_num < 3:
            if self._check_game_over_matches():
                if self._check_if_faller_outside_field():
                    self._delete_extra_rows()
                    self.game_over = True
                else:
                    self._delete_extra_rows()
            else:
                self.game_over = True
        else:
            self.match_squares()
            if self.check_for_matches():
                self.matching = True
        faller.faller_num += 1 # get value to what it originally was
        self.field_wo_faller = self._copy_field(self.field) # update the field without the faller
        self.need_new_faller = True
    def _faller_land(self, faller: Faller, column: list):
        '''Has the faller go into its landing state'''
        if faller.faller_num < 3:
            faller.add_to_faller_num()
                
        if faller.faller_spot - 3 >= 0: # checks if the faller is at the very top of the column
            column[faller.faller_spot - 3] = '   '

        self._change_faller_state_in_field()
        faller.add_to_faller_spot()
    def _match(self):
        '''Checks it there are matches, and if there are, eliminates the squares in the matches'''
        if self.check_for_matches():
            self.delete_matches()
        else:
            self.matching = False
        self.match_squares()
    def pass_time(self):
        '''Shifts the faller down a square and updates the state (still dropping, landed, or frozen) of the faller'''
        if self.game_over:
            raise GameOverError
        else:
            if not self.need_new_faller:
                faller = self.faller
                column = self.field[faller.faller_col]
                self._change_faller_state(faller.faller_col)
                if not self.matching: # if the field is not matching squares, then do things with the faller
                    if not faller.landed and not faller.frozen:
                        self._faller_drop(faller, column)
                    elif faller.frozen:
                        self._faller_freeze(faller)
                    elif faller.landed:
                        self._faller_land(faller, column)
            else:
                self._match()
    def rotate_faller(self):
        '''Rotates the faller'''
        if self.game_over:
            raise GameOverError
        else:
            if not self.need_new_faller:
                faller = self.faller
                faller.rotate()
                spot = faller.faller_spot - 1 # faller should remain in the same level
                col = self.field[faller.faller_col]
                for i in range(faller.faller_num):
                    col[spot - i] = faller.faller[i] 
    def move_faller_left(self):
        '''
        Moves the faller one column to the left, if there is one 
        (and if it is not blocked by jewel already frozen on the field or by the edge of the field
        '''
        if self.game_over:
            raise GameOverError
        else:
            if not self.need_new_faller:
                faller = self.faller
                if faller.faller_col - 1 >= 0:
                    self._update_field(faller.faller_col - 1)
                else:
                    raise InvalidMoveError
    def move_faller_right(self):
        '''
        Moves the faller one column to the right, if there is one 
        (and if it is not blocked by jewel already frozen on the field or by the edge of the field
        '''
        if self.game_over:
            raise GameOverError
        else:
            if not self.need_new_faller:
                faller = self.faller
                if faller.faller_col + 1 < len(self.field):
                    self._update_field(faller.faller_col + 1)
                else:
                    raise InvalidMoveError
    def _is_valid_column_number(self, col_num: int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise'''
        return 0 <= col_num < self.cols
    def _is_valid_row_number(self, row_num: int) -> bool:
        '''Returns True if the given row number is valid; returns False otherwise'''
        return 0 <= row_num < self.rows
    def _three_in_a_row(self, col: int, row: int, coldelta: int, rowdelta: int):
        '''Returns the number of the same colors in a certain direction that are in a row'''
        start_square = self.field[col][row][1]
        num = 0
        if start_square == ' ':
            return num
        else:
            for i in range(max([self.cols, self.rows])):
                if self._is_valid_column_number(col + coldelta * i) and self._is_valid_row_number(row + rowdelta * i):
                    if start_square == self.field[col + coldelta * i][row + rowdelta * i][1]:
                        num += 1
                    else:
                        return num        
                else:
                    return num
            return num
    def _match_sequence_begins_at(self, col: int, row: int):
        '''
        Returns a list of objects containing details about a match that has 3 or more colors in a row
        (direction of the match and the number of colors in the match)
        '''
        matches = []
        if self._three_in_a_row(col, row, 0, 1) >= 3:
            matches.append(Match((0, 1), self._three_in_a_row(col, row, 0, 1)))
        if self._three_in_a_row(col, row, 1, 1) >= 3:
            matches.append(Match((1, 1), self._three_in_a_row(col, row, 1, 1)))
        if self._three_in_a_row(col, row, 1, 0) >= 3:
            matches.append(Match((1, 0), self._three_in_a_row(col, row, 1, 0)))
        if self._three_in_a_row(col, row, 1, -1) >= 3:
            matches.append(Match((1, -1), self._three_in_a_row(col, row, 1, -1)))
        if self._three_in_a_row(col, row, 0, -1) >= 3:
            matches.append(Match((0, -1), self._three_in_a_row(col, row, 0, -1)))
        if self._three_in_a_row(col, row, -1, -1) >= 3:
            matches.append(Match((-1, -1), self._three_in_a_row(col, row, -1, -1)))
        if self._three_in_a_row(col, row, -1, 0) >= 3:
            matches.append(Match((-1, 0), self._three_in_a_row(col, row, -1, 0)))
        if self._three_in_a_row(col, row, -1, 1) >= 3:
            matches.append(Match((-1, 1), self._three_in_a_row(col, row, -1, 1)))
        
        return matches
    def match_squares(self):
        '''If there is a match in the field, indicates that by putting stars around the colors that are in the match'''
        for col in range(len(self.field)):
            for row in range(len(self.field[col])):
                matches = self._match_sequence_begins_at(col, row)
                for match in matches:
                    coldelta = match.delta[0]
                    rowdelta = match.delta[1]
                    for i in range(match.num):
                        self.field[col + coldelta * i][row + rowdelta * i] = f'*{self.field[col][row][1]}*'
    def check_for_matches(self):
        '''If there is a match (a square with a * in it), returns True. Otherwise, returns False'''
        for col in range(len(self.field)):
            for row in range(len(self.field[col])):
                if self.field[col][row][0] == '*':
                    return True
        return False
    def delete_matches(self):
        '''Deletes all the matches in the field'''
        for col in range(len(self.field)):
            for row in range(len(self.field[col])):
                if self.field[col][row][0] == '*':
                    self.field[col].pop(row)
                    self.field[col].insert(0, '   ')
    def _check_game_over_matches(self):
        '''Check if the faller that has not completely entered the board can match '''
        field = self._copy_field(self.field)
        added_rows = 3 - self.faller.faller_num
        faller_num = self.faller.faller_num
        for col in range(len(self.field)):
            column = self.field[col]
            for row in range(added_rows):
                if col != self.faller.faller_col:
                    column.insert(0, '   ')
                else:
                    if self._is_valid_row_number(faller_num + row):
                        column.insert(0, self.faller.faller[faller_num + row])

        self.match_squares()

        if self.check_for_matches:
            return True
        else:
            self.field = field
            return False
    def _check_if_faller_outside_field(self):
        '''Checks if the faller would freeze outside of the field because it doesn't fit inside the field'''
        field = self._copy_field(self.field)
        added_rows = 3 - self.faller.faller_num
        
        self.delete_matches()
        self.drop_everything()

        for col in range(len(self.field)):
            column = self.field[col]
            for row in range(added_rows):
                if column[row] != '   ':
                    self.field = field
                    return True
        self.field = field
        self.drop_everything()
        return False
    def _delete_extra_rows(self):
        '''Deletes the extra rows that are added when trying to see if there would be a match with the faller'''
        added_rows = 3 - self.faller.faller_num

        for col in range(len(self.field)):
            column = self.field[col]
            for row in range(added_rows):
                column.pop(row)
    def _find_bottom_square_index(self, col: int):
        '''
        Returns the index of a non-empty square in a column.
        If all the squares are empty in the column, returns -1
        '''
        column = self.field[col]
        for square in range(len(column)):
            if column[square][0] == ' ' and column[square][1] in COLORS:
                return square
        return -1
    def drop_everything(self):
        '''Deletes all empty squares that are underneath squares with colors in them'''
        for col in range(len(self.field)):
            column = self.field[col]
            if self._find_bottom_square_index(col) != -1:
                for row in range(self._find_bottom_square_index(col), len(column)):
                    if column[row] == '   ':
                        column.pop(row)
                        column.insert(0, '   ')
                     

