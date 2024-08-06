# AI 2048 Game Solver

This is an adversarial search agent implemented using the expectiminimax algorithm and alpha-beta pruning.\
In order to make the search more optimal, game-specific heuristics -- monotonicity and smoothness -- are used to create a more favorable environment for the AI agent's success. \
\
Monotonicity refers to a state in which the numbers are increasing/decreasing along the diagonal path.\
Smoothness refers to a state in which the adjacent numbers are equivalent, increasing the change of combining the cells.\
Heuristic weights were optimized after a series of test runs.\
\
Currently, among 10 runs, at least 3 runs reach 2048 and at least 2 runs reach 1024.

BaseAI.py -- Abstract base class for both agents (inherited by ComputerAI.py and IntelligentAgent.py)\
BaseDisplayer.py -- Abstract base class for grid display (inherited by Displayer.py)\
ComputerAI.py -- Randomly determines next moves for the opponent\
Displayer.py -- Displays the current state of the game\
GameManager.py -- Executes the game\
IntelligentAgent.py -- Implements the expectiminimax algorithm to determine the best move for the AI agent\

## To run
In terminal, run `$ python GameManager.py`
