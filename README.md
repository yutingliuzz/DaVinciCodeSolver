The Da Vinci Code Solver

This is the implementation of The Da Vinci Code Solver for using heuristic search algorithm.

Experiment Setup:
Game interface: CodeSkulptor (https://py2.codeskulptor.org/) Just copy and paste the codes in finalproject.py file to CodeSkulptor and click run button. Then the game interface will automatically show up and the game will start immediately without any other operations.
Heuristic solver vs. baseline solver: the baseline solver's cards will be marked by card numbers. When the game finishes, if the interface displays "you lose", it means the baseline solver loses.
Run the game for 50 times and get the winning rate.

If you want to play against the heuristic agent, please change the human_test bool in the global variance to True. If you want to test the agent's performance, please change the bool to False.

Results:
For 50 games, the winning rate of baseline solver should be around 0.02
The decision-making speed should be around 2 seconds for both baseline and heuristic solver.

Credits:
This project makes use of the design of the interface for The Da Vinci Code game from https://github.com/hello-world-zsp/The-Da-Vinci-Code-Board-Game/tree/master
