# DS5100 Final Project
# Metadata 

*project name:* **Monte Carlo Simulator**

*project author:* **Hallie Parten** 

# Synopsis

To install the classes in the package: 
 
  ```bash
  pip install -e .
  ```

To import the package into a notebook or .py file: 

  ```python 
  from montecarlo import Die, Game, Analyzer 
  ```

To create a die: 

  ```python 
  Faces = [1, 2, 3, 4, 5, 6]
  die = Die(Faces)
  ```

To play a game: 

  ```python
  game = Game(dice = [die, die])
  game.play_game(n_rolls = 10)
  ```

To analyze a game: 

  ```python
  analyzer = Analyzer(game = game)
  analyzer.jackpot()
  ```
  
# API Description

[**Classes:**] 

1. **Die:** A die has N sides, or faces, and W weights, and can be rolled to select a face. W defaults to 1.0 for each face but can be changed after the object is created. The die has one behavior, which is to be rolled one or more times.
-  Methods: 
	1. **change_weight:** A method to change the weight of a single side
	-  Parameters:
		-  *face (string, number):* the face value to be changed
		-  *new_weight (float):* the new weight 

	2. **roll_die:** A method to roll the die one or more times.
	-  Parameters: 
		-  *n_rolls(int):* how many times the die is to be rolled; defaults to 1
	-  Returns: 
		-  a list of roll outcomoes 

	3. **show_latest_die:** A method to show the user the die's current set of faces and weights in a dataframe.

2. **Game:** A game consists of rolling of one or more dice of the same kind one or more times. Each game is initialized with one or more of similarly defined (same # of sides and associated faces) dice (Die objects). The class has a behavior to play a game, i.e. to rolls all of the dice a given number of timess. The class keeps the results of its most recent play.
-  Methods: 
	1. **play_game:** A method to play the game
	-  Parameters:
		-  n_rolls(int): how many ties the dice should be rolled
	
	2. **show_results** A method to show the user the results of the most recent play.
  	-  Parameters: 
  		-  form('N' or 'W'): parameter to return the dataframe in narrow or wide form (defaults to 'W')
  	-  Returns: 
  		-  dataframe of results in either wide form (with index for roll number, column for each die number and face rolled) or narrow form (with a two column index with the roll number and die number, and a column for face rolled).
 
 3. **Analyzer:** An analyzer takes the results of a single game and computes various descriptive statistical properties about it. These properties and results are available as attributes of an Analyzer object.
 - Attributes: 
 	-  dtype_dice: list of string or float
 	-  jackpot_count: int
 	-  jackpot_results: dataframe
 	-  combo_count: int
 	-  combo_results: dataframe
 	-  face_count_results: dataframe

- Methods:
	1. **jackpot:** A jackpot method to compute how many times the game resulted in all faces being identical. 
	-  Parameters: None
	-  Returns: 
		-  jackpot_count: returns an integer for the number times to the user (also stored as a public attribute)
	2. **combo:** A combo method to compute the distinct combinations of faces rolled, along with their counts. Takes no input; stores the following results as public attribute:
		-  combo_results: a dataframe with a multi-columned index of the combinations, sorted. 
		-  combo_count: an overall count of distinct combinations
	3. **face_counts_per_roll:** A method to compute how many times a given face is rolled in each event. Take no input; stores as a public attribute:
		-  face_counts_per_roll: a dataframe with an index of the roll numer and face values as columns'''


# Manifest 




