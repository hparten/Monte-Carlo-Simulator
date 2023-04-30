import numpy as np
import pandas as pd
import numbers

class Die:
    '''A die has N sides, or faces, and W weights, and can be rolled to select a face.
    W defaults to 1.0 for each face but can be changed after the object is created.
    The die has one behavior, which is to be rolled one or more times.
    '''
    
    weight = 1.0
    
    def __init__(self, faces): 
        '''Takes an array of faces as an argument. The array's data type (dtype) may be strings or numbers.
        '''
        self.faces = faces
        self._die_ = pd.DataFrame({
            'faces': self.faces,
            'weights': pd.Series([self.weight for x in range(len(self.faces))])
        })
        
    def change_weight(self, face, new_weight):
        '''A method to change the weight of a single side.
        
        Parameters: 
            face (string, number): the face value to be changed
            new_weight (float): the new weight 
        '''
        if face in self._die_.faces.values: 
            if (isinstance(new_weight, numbers.Number)==True) or (new_weight.isdigit()==True): 
                self._die_.loc[self._die_['faces'] == face, 'weights'] = float(new_weight)
            else: 
                raise ValueError("Your new weight must be a number!")
        else: 
            raise ValueError("That face is not on your die!")
            
        
            
            
    def roll_die(self, n_rolls=1):
        '''A method to roll the die one or more times.
        
        Parameters: 
            n_rolls(int): how many times the die is to be rolled; defaults to 1
            
        Returns: 
            a list of roll outcomes
        '''
        results = []
        for i in range(n_rolls):
            result = self._die_.faces.sample(weights=self._die_.weights).values[0]
            results.append(result)
        return pd.Series(results).to_list()
    
    def show_latest_die(self):
        '''A method to show the user the die's current set of faces and weights in a dataframe
        '''
        return self._die_
       

class Game:
    '''A game consists of rolling of one or more dice of the same kind one or more times.
    Each game is initialized with one or more of similarly defined (same # of sides and associated faces) dice (Die objects).
    The class has a behavior to play a game, i.e. to rolls all of the dice a given number of times.
    The class keeps the results of its most recent play.
    '''
    
    def __init__(self, dice):
        '''Takes a list of already instantiated similar Die objects.
        '''
        self.dice = dice
        
    def play_game(self, n_rolls):
        '''A method to play the game
        
        Parameters:
            n_rolls(int): how many ties the dice should be rolled
        '''
        game_result = []
        for i in self.dice:
            dice_result = pd.Series(i.roll_die(n_rolls))
            game_result.append(dice_result)
        self._game_result_df_ = pd.DataFrame(data=game_result).T
        self._game_result_df_.index.name = 'Roll Number'
        self._game_result_df_.columns.name = 'Die Number'
        
        
    def show_results(self, form='W'):
        '''A method to show the user the results of the most recent play.
        
        Parameters: 
            form('N' or 'W'): parameter to return the dataframe in narrow or wide form (defaults to 'W')
            
        Returns: 
            dataframe of results in either wide form (with index for roll number, column for each die number and face rolled)
            or narrow form (with a two column index with the roll number and die number, and a column for face rolled).
        '''
        if form=='W':
            return self._game_result_df_
        if form=='N':
            narrow_result = self._game_result_df_.stack().to_frame()
            narrow_result.rename(columns={0:'Face'}, inplace=True)
            return narrow_result
        else: 
            raise ValueError('You must specifiy you form as "W" for wide and "N" for narrow')
    
class Analyzer: 
    '''An analyzer takes the results of a single game and computes various descriptive statistical properties about it. 
    These properties results are available as attributes of an Analyzer object.
    
    Attributes (and associated methods) include:
        A face counts per roll, i.e. the number of times a given face appeared in each roll. 
            For example, if a roll of five dice has all sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.
        A jackpot count, i.e. how many times a roll resulted in all faces being the same, e.g. all one for a six-sided die.
        A combo count, i.e. how many combination types of faces were rolled and their counts.'''
    
    jackpot_count = 0
    combo_count = 0
    face_counts_results = []
    jackpot_results = []
    combo_results = []
    
    def __init__(self, game):
        '''Takes a game object as its input parameter. At initialization time, it also infers the data type of the die faces used as an attribute.
        '''
        self.game = game 
        self.dtype_dice = [] 
        for i in self.game.dice: 
            dtype = type(i.faces[0])
            self.dtype_dice.append(dtype)
            
    def jackpot(self):
        '''A jackpot method to compute how many times the game resulted in all faces being identical.
        
        Returns: 
            jackpot_count: returns an integer for the number times to the user (also stored as a public attribute)
            jackpot_results: stores the results as a dataframe of jackpot results in a public attribute.
        '''
        self.jackpot_results = self.game.show_results().copy()
        self.jackpot_results['jackpot'] = self.jackpot_results.eq(self.jackpot_results.iloc[:, 0], axis=0).all(1).astype(int)
        self.jackpot_results = self.jackpot_results.loc[self.jackpot_results['jackpot'] == 1]
        self.jackpot_count = sum(self.jackpot_results['jackpot'])
        return self.jackpot_count
    
    def combo(self):
        '''A combo method to compute the distinct combinations of faces rolled, along with their counts.
        
        Stores as a public attribute:
            combo_results: a dataframe with a multi-columned index of the combinations, sorted. 
            combo_count: an overall count of distinct combinations
        '''
        combo_copy = self.game.show_results().copy()
        self.combo_results = combo_copy.groupby(list(combo_copy.columns)).size().to_frame('counts').sort_values('counts', ascending=False)
        self.combo_count = len(self.combo_results)
    
    def face_counts_per_roll(self):
        '''A method to compute how many times a given face is rolled in each event. 
        
        Stores as a public attribute: 
            face_counts_per_roll: a dataframe with an index of the roll numer and face values as columns'''
        face_copy = self.game.show_results().copy()
        face_values = []
        for i in range(len(face_copy)):
            face_count = face_copy.iloc[i].value_counts()
            face_values.append(face_count)
        self.face_counts_results = pd.DataFrame(face_values).fillna(0).astype(int)
        self.face_counts_results.index.name = 'Roll Number'
        self.face_counts_results.columns.name = 'Faces'
        