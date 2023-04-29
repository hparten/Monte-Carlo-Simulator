from montecarlo import Die
from montecarlo import Game
from montecarlo import Analyzer
import unittest

class DieTestSuite(unittest.TestCase): 

    def test_1_init_die(self): 
        '''checks that all the weights of the initialized die are 1.0''' 
        test_die = Die(['a','b','c','d'])
        Expected = [1.0, 1.0, 1.0, 1.0]
        Actual = list(test_die._die_.weights)
        self.assertEqual(Expected, Actual)    
    
    def test_2_change_weight(self): 
        '''checks that the exception is raised when an incorrect face is passed as an argument''' 
        test_die = Die(['a','b','c','d'])
        correct_weight = 2.5
        incorrect_face = 1
        self.assertRaises(ValueError, test_die.change_weight, incorrect_face, correct_weight)
        
    def test_3_change_weight(self): 
        '''checks that the exception is raised when an incorrect type of weight is passed'''
        test_die = Die(['a','b','c','d'])
        correct_face = 'a'
        incorrect_weight = 'b'
        self.assertRaises(ValueError, test_die.change_weight, correct_face, incorrect_weight)
        
    def test_4_change_weight(self): 
        '''checks that the numeric character is converted to a float and the weight is changed.''' 
        test_die = Die(['a','b','c','d'])
        test_die.change_weight('a', '2')
        Expected = 2
        Actual = test_die.show_latest_die().iloc[0]['weights']
        self.assertEqual(Expected, Actual)
        
    def test_5_change_weight(self):
        '''tests if weight for corresponding face is changed'''
        test_die = Die(['a','b','c','d'])
        test_die.change_weight('a', 2.5)
        Expected = 2.5
        Actual = test_die.show_latest_die().iloc[0]['weights']
        self.assertEqual(Expected, Actual)
    
    def test_6_roll_die(self): 
        '''tests if the correct number of rolls is outputted'''
        test_die = Die(['a','b','c','d'])
        test_die.roll_die(5)
        Expected = 5
        Actual = len(test_die.roll_die(5))
        self.assertEqual(Expected, Actual)
        
    def test_7_show_latest_die(self):
        '''tests if the size of the die dataframe is expected'''
        test_die = Die(['a','b','c','d'])
        Expected = (4,2)
        Actual = test_die.show_latest_die().shape
        self.assertEqual(Expected, Actual)
        
class GameTestSuite(unittest.TestCase):
    

    def test_1_play_game(self):
        '''tests that the size of the wide results dataframe is expected for n_rolls'''
        test_die1 = Die(['a','b','c','d'])
        test_die2 = Die(['a','b','c','d'])
        test_die2.change_weight('b', 2.0)
        test_game = Game([test_die1, test_die2])
        test_game.play_game(20)
        Expected = (20, 2)
        Actual = test_game._game_result_df_.shape 
        self.assertEqual(Expected, Actual)
        
    def test_2_show_results_w(self): 
        '''tests that the size of the wide results data frame matches the expected size for n_rolls'''
        test_die1 = Die(['a','b','c','d'])
        test_die2 = Die(['a','b','c','d'])
        test_die2.change_weight('b', 2.0)
        test_game = Game([test_die1, test_die2])
        test_game.play_game(20)
        Expected = (20, 2)
        Actual = test_game.show_results().shape
        self.assertEqual(Expected, Actual)
        
        
    def test_3_show_results_n(self): 
        '''tests that the size fo the narrow results dataframe is expected for n_rolls'''
        test_die1 = Die(['a','b','c','d'])
        test_die2 = Die(['a','b','c','d'])
        test_die2.change_weight('b', 2.0)
        test_game = Game([test_die1, test_die2])
        test_game.play_game(20)
        Expected = (40, 1)
        Actual = test_game.show_results('N').shape
        self.assertEqual(Expected, Actual)
        
class GameAnalyzerSuite(unittest.TestCase):
        
    def test_1_jackpot(self):
        '''tests that size of the jackpot dataframe matches the jackpot count''' 
        test_die1 = Die(['a','b','c','d'])
        test_die2 = Die(['a','b','c','d'])
        test_die2.change_weight('b', 2.0)
        test_game = Game([test_die1, test_die2])
        test_game.play_game(20)
        test_analyzer = Analyzer(test_game)
        test_analyzer.jackpot()
        Expected = (test_analyzer.jackpot_count, 3)
        Actual = test_analyzer.jackpot_results.shape
        self.assertEqual(Expected, Actual)
        
    def test_2_combo(self):
        '''tests that the size of the combo dataframe matches the combo count'''
        test_die1 = Die(['a','b','c','d'])
        test_die2 = Die(['a','b','c','d'])
        test_die2.change_weight('b', 2.0)
        test_game = Game([test_die1, test_die2])
        test_game.play_game(20)
        test_analyzer = Analyzer(test_game)
        test_analyzer.combo()
        Expected = (test_analyzer.combo_count, 1)
        Actual = test_analyzer.combo_results.shape
        self.assertEqual(Expected, Actual)
        
    def test_3_face_counts_per_roll(self):
        '''tests that size of the face counts data frame is expected for n_rolls'''
        test_die1 = Die(['a','b','c','d'])
        test_die2 = Die(['a','b','c','d'])
        test_die2.change_weight('b', 2.0)
        test_game = Game([test_die1, test_die2])
        test_game.play_game(20)
        test_analyzer = Analyzer(test_game)
        test_analyzer.face_counts_per_roll()
        Expected = (20, 4)
        Actual = test_analyzer.face_counts_results.shape
        self.assertEqual(Expected, Actual)

        
if __name__ == '__main__':    
    unittest.main()        
        
        