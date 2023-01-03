from field_class import Field, InvalidMoveError
import unittest

class FieldTest(unittest.TestCase):
    def setUp(self):
        '''Sets up fields for the following tests'''
        self.field1 = self._create_empty_mxn_field()
        self.field2 = self._create_empty_nxn_field()
        self.field3 = self._create_filled_mxn_field()
        self.field4 = self._create_filled_nxn_field()

    def _create_empty_mxn_field(self):
        '''Creates an empty mxn (non-square) field'''
        field = [['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   ']]
        return Field(field)
    def _create_empty_nxn_field(self):
        '''Creates an empty nxn field'''
        field = [['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   ']]
        return Field(field)  
    def _create_filled_mxn_field(self):
        '''Creates a non-empty mxn (non-square) field'''
        field = [['   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', ' X '], 
                 [' S ', '   ', ' V ', ' X '], 
                 [' T ', ' Y ', ' Y ', ' S '], 
                 [' X ', ' X ', ' X ', ' Y ']]
        return Field(field)
    def _create_filled_nxn_field(self):
        '''Creates a non-empty nxn field'''
        field = [['   ', ' Y ', '   ', ' X '], 
                 [' S ', '   ', ' V ', '   '], 
                 [' T ', ' X ', ' Y ', ' S '], 
                 [' X ', '   ', ' X ', ' Y ']]
        return Field(field)  
    def test_has_col_num_given_when_created(self):
        '''Tests if the correct number of columns are stored in self.cols'''
        self.assertEqual(self.field1.cols, 5)
        self.assertEqual(self.field2.cols, 4)
    def test_has_row_num_given_when_created(self):
        '''Tests if the correct number of rows are stored in self.rows'''
        self.assertEqual(self.field1.rows, 4)
        self.assertEqual(self.field2.rows, 4)
    def test_has_field_given_when_created(self):
        '''Tests if the field is stored in self.field'''
        self.assertEqual(self.field1.field, [['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
        self.assertEqual(self.field2.field, [['   ', '   ', '   ', '   '], 
                                          ['   ', '   ', '   ', '   '], 
                                          ['   ', '   ', '   ', '   '], 
                                          ['   ', '   ', '   ', '   ']])
        self.assertEqual(self.field3.field, [['   ', '   ', '   ', '   '], 
                                              ['   ', '   ', '   ', ' X '], 
                                              [' S ', '   ', ' V ', ' X '], 
                                              [' T ', ' Y ', ' Y ', ' S '], 
                                              [' X ', ' X ', ' X ', ' Y ']])
        self.assertEqual(self.field4.field, [['   ', ' Y ', '   ', ' X '], 
                                          [' S ', '   ', ' V ', '   '], 
                                          [' T ', ' X ', ' Y ', ' S '], 
                                          [' X ', '   ', ' X ', ' Y ']])
    def test_faller_created_from_string(self):
        '''
        Tests if a list of three elements (a faller) is created correctly from a string 
        indicating what the faller's colors are
        '''
        faller_string = 'V W Z'
        self.field1.create_faller(faller_string, 0)
        self.assertEqual(self.field1.faller.faller, ['[Z]', '[W]', '[V]'])
    def test_pass_times(self):
        '''Tests that the faller drops down one square at a time'''
        self.test_faller_created_from_string()
        self.field1.pass_time()
        self.assertEqual(self.field1.field, [['[Z]', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
        self.field1.pass_time()
        self.field1.pass_time()
        self.assertEqual(self.field1.field, [['[V]', '[W]', '[Z]', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
    def test_faller_lands(self):
        '''Tests that the faller changes to a landing state once it reaches the bottom of the field'''
        self.test_pass_times()
        self.field1.pass_time()
        self.assertEqual(self.field1.field, [['   ', '|V|', '|W|', '|Z|'], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
    def test_faller_freezes(self):
        '''
        Tests that the faller changes to the frozen state once time passes 
        after the faller is in its landed state
        '''
        self.test_faller_lands()
        self.field1.pass_time()
        self.assertEqual(self.field1.field, [['   ', ' V ', ' W ', ' Z '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
    def test_faller_rotates(self):
        '''Tests that the faller rotates correctly in the field'''
        self.test_pass_times()
        self.field1.rotate_faller()
        self.assertEqual(self.field1.field, [['[Z]', '[V]', '[W]', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
    def test_faller_moves_across_columns(self):
        '''Tests that the faller can move to the column to its left and to the column to its right'''
        self.test_pass_times()
        self.field1.move_faller_right()
        self.assertEqual(self.field1.field, [['   ', '   ', '   ', '   '], 
                                         ['[V]', '[W]', '[Z]', '   '],
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])

        self.field1.move_faller_right()
        self.field1.move_faller_right()
        self.assertEqual(self.field1.field, [['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['[V]', '[W]', '[Z]', '   '],
                                         ['   ', '   ', '   ', '   ']])

        self.field1.move_faller_left()
        self.assertEqual(self.field1.field, [['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['[V]', '[W]', '[Z]', '   '],
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
        self.field1.move_faller_left()
        self.field1.move_faller_left()
        self.assertEqual(self.field1.field, [['[V]', '[W]', '[Z]', '   '],
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
    def test_faller_doesnt_move_across_columns_if_not_possible(self):
        '''Tests that the faller doesn't switch columns if there are frozen squares in the way'''
        self.test_faller_freezes()
        faller_string = 'V W Z'
        self.field1.create_faller(faller_string, 1)
        self.field1.pass_time()
        self.field1.pass_time()
        self.field1.pass_time()
        self.assertRaises(InvalidMoveError, self.field1.move_faller_left)

        self.assertEqual(self.field1.field, [['   ', ' V ', ' W ', ' Z '], 
                                         ['[V]', '[W]', '[Z]', '   '],
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   '], 
                                         ['   ', '   ', '   ', '   ']])
    def test_matches(self):
        '''Tests that a three in a row match is registered as a match'''
        self.field3.match_squares()
        self.assertEqual(self.field3.field,[['   ', '   ', '   ', '   '], 
                                            ['   ', '   ', '   ', ' X '], 
                                            [' S ', '   ', ' V ', ' X '], 
                                            [' T ', ' Y ', ' Y ', ' S '], 
                                            ['*X*', '*X*', '*X*', ' Y ']])
    def test_deletes_matches(self):
        '''Tests that squares in the matched state are then deleted'''
        self.test_matches()
        self.field3.delete_matches()
        self.assertEqual(self.field3.field,[['   ', '   ', '   ', '   '], 
                                            ['   ', '   ', '   ', ' X '], 
                                            [' S ', '   ', ' V ', ' X '], 
                                            [' T ', ' Y ', ' Y ', ' S '], 
                                            ['   ', '   ', '   ', ' Y ']])
    def test_4_in_a_row_match(self):
        '''Tests that a four in a row match is registered'''
        field = [['   ', '   ', '   ', '   ', '   '], 
                 ['   ', '   ', '   ', '   ', ' X '], 
                 ['   ', ' S ', '   ', ' V ', ' X '], 
                 ['   ', ' T ', ' Y ', ' Y ', ' S '], 
                 [' X ', ' X ', ' X ', ' X ', ' Y ']]
        field = Field(field)
        field.match_squares()
        self.assertEqual(field.field, [['   ', '   ', '   ', '   ', '   '], 
                                       ['   ', '   ', '   ', '   ', ' X '], 
                                       ['   ', ' S ', '   ', ' V ', ' X '], 
                                       ['   ', ' T ', ' Y ', ' Y ', ' S '], 
                                       ['*X*', '*X*', '*X*', '*X*', ' Y ']])
    def test_5_in_a_row_match(self):
        '''Tests that a five in a row match is registered'''
        field = [[' Y ', ' X ', ' S ', ' T ', ' S '], 
                 ['   ', ' Y ', ' V ', ' X ', ' X '], 
                 [' U ', ' S ', ' Y ', ' V ', ' X '], 
                 [' S ', ' T ', ' Y ', ' Y ', ' S '], 
                 [' X ', ' Y ', ' X ', ' X ', ' Y ']]
        field = Field(field)
        field.match_squares()
        self.assertEqual(field.field, [['*Y*', ' X ', ' S ', ' T ', ' S '], 
                                       ['   ', '*Y*', ' V ', ' X ', ' X '], 
                                       [' U ', ' S ', '*Y*', ' V ', ' X '], 
                                       [' S ', ' T ', ' Y ', '*Y*', ' S '], 
                                       [' X ', ' Y ', ' X ', ' X ', '*Y*']])
        field.delete_matches()
        self.assertEqual(field.field, [['   ', ' X ', ' S ', ' T ', ' S '], 
                                       ['   ', '   ', ' V ', ' X ', ' X '], 
                                       ['   ', ' U ', ' S ', ' V ', ' X '], 
                                       ['   ', ' S ', ' T ', ' Y ', ' S '], 
                                       ['   ', ' X ', ' Y ', ' X ', ' X ']])
    def test_multiple_matches_in_one_drop(self):
        '''Tests that multiple matches can be made at a time (even if they are matches of different colors)'''
        field = [[' X ', ' X ', ' X ', ' X '],
                 ['   ', '   ', '   ', ' X '],
                 ['   ', '   ', '   ', ' X '],
                 ['   ', '   ', '   ', ' X ']]
        field = Field(field)

        field.match_squares()
        field.delete_matches()
        self.assertEqual(field.field, [['   ', '   ', '   ', '   '],
                                       ['   ', '   ', '   ', '   '],
                                       ['   ', '   ', '   ', '   '],
                                       ['   ', '   ', '   ', '   ']])

        field = [[' S ', ' Y ', ' Y ', ' Y '],
                 ['   ', ' X ', ' Y ', ' Y '],
                 ['   ', '   ', ' X ', ' X '],
                 ['   ', '   ', '   ', ' X ']]
        field = Field(field)

        field.match_squares()
        field.delete_matches()
        self.assertEqual(field.field, [['   ', '   ', '   ', ' S '],
                                       ['   ', '   ', ' Y ', ' Y '],
                                       ['   ', '   ', '   ', ' X '],
                                       ['   ', '   ', '   ', '   ']])
    def test_square_drop_down(self):
        '''
        Tests that if colored squares start above an empty space, they will drop down
        so that no empty space is below a colored square
        '''
        field = [[' X ', ' Y ', ' X ', ' X '],
                 [' Y ', '   ', '   ', ' Z '],
                 ['   ', ' X ', '   ', ' X '],
                 ['   ', '   ', ' Z ', ' X ']]
        field = Field(field)

        field.drop_everything()
        self.assertEqual(field.field, [[' X ', ' Y ', ' X ', ' X '],
                                       ['   ', '   ', ' Y ', ' Z '],
                                       ['   ', '   ', ' X ', ' X '],
                                       ['   ', '   ', ' Z ', ' X ']])
    

if __name__ == '__main__':
    unittest.main()