from faller_class import Faller
import unittest

class FallerTest(unittest.TestCase):
    def setUp(self):
        '''Sets up fields for the following tests'''
        self.faller1 = Faller('X Y Z', 1)
        self.faller2 = Faller('S T V', 3)
    def test_has_faller_list_given_when_created(self):
        '''
        Tests if a list of three elements (a faller) is created correctly from a string 
        indicating what the faller's colors are
        '''
        self.assertEqual(self.faller1.faller, ['[Z]', '[Y]', '[X]'])
        self.assertEqual(self.faller2.faller, ['[V]', '[T]', '[S]'])
    def test_faller_num_adds_one(self):
        '''Tests that the self.add_to_faller_num() method adds one to self.faller_num '''
        self.assertEqual(self.faller1.faller_num, 0)

        self.faller1.add_to_faller_num()
        self.assertEqual(self.faller1.faller_num, 1)

        self.faller1.add_to_faller_num()
        self.faller1.add_to_faller_num()
        self.assertEqual(self.faller1.faller_num, 3)
    def test_faller_spot_adds_one(self):
        '''Tests that the self.add_to_faller_spot() method adds one to self.faller_spot '''
        self.assertEqual(self.faller1.faller_spot, 0)

        self.faller1.add_to_faller_spot()
        self.assertEqual(self.faller1.faller_spot, 1)

        self.faller1.add_to_faller_spot()
        self.faller1.add_to_faller_spot()
        self.assertEqual(self.faller1.faller_spot, 3)
    def test_faller_col_updates(self):
        '''Tests that self.change_fall_col can change the value of self.faller_col'''
        self.assertEqual(self.faller1.faller_col, 1)
        self.assertEqual(self.faller2.faller_col, 3)

        self.faller1.change_faller_col(2)
        self.assertEqual(self.faller1.faller_col, 2)

        self.faller2.change_faller_col(1)
        self.assertEqual(self.faller2.faller_col, 1)
    def test_faller_rotates(self):
        '''Tests that the faller rotates so that the bottom square becomes the middle square'''
        self.faller1.rotate()
        self.assertEqual(self.faller1.faller, ['[Y]', '[X]', '[Z]'])
        self.faller1.rotate()
        self.assertEqual(self.faller1.faller, ['[X]', '[Z]', '[Y]'])
    def test_faller_state_changes_to_landing(self):
        '''Tests that the faller changes to the landing state after self.land() is called'''
        self.faller1.land()
        self.assertEqual(self.faller1.faller, ['|Z|', '|Y|', '|X|'])
    def test_faller_state_changes_to_falling(self):
        '''Tests that the faller changes to the falling state after self.fall() is called'''
        self.test_faller_state_changes_to_landing()
        self.faller1.fall()
        self.assertEqual(self.faller1.faller, ['[Z]', '[Y]', '[X]'])
    def test_faller_state_changes_to_landing(self):
        '''Tests that the faller changes to the frozen state after self.freeze() is called'''
        self.faller1.freeze()
        self.assertEqual(self.faller1.faller, [' Z ', ' Y ', ' X '])

if __name__ == '__main__':
    unittest.main()