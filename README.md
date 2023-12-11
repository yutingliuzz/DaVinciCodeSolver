**The Da Vinci Code Solver**

This is the implementation of The Da Vinci Code Solver by using heuristic search algorithm against human player or baseline player (a random algorithm).

**Experiment Setup:**

**Game interface:** CodeSkulptor (https://py2.codeskulptor.org/) Just copy and paste the codes in *finalproject.py* file to CodeSkulptor and click run button. 

Then the game interface will automatically show up and the game will start immediately without any other operations.

**Baseline solver VS. Heuristic solver:** The baseline solver's cards will be marked by card numbers. When the game finishes, if the interface displays "Heuristic Wins", it means the baseline solver loses on that round. The number of rounds that will be tested in total is defined in global variable *max_games*.

**Baseline solver VS. Heuristic solver:** If you want to play against the heuristic agent, please change the *human_test* bool in the global variance to **True**. 
When "Please deal" is displayed on the interface, choose "Deal randomly" "deal white" or "deal black" on the left to get a new card from the draw stack. 
When "Please guess" is displayed on the interface, select the card on the opposite side (the side without Card Number) and a red dot will appear on it; input the number you guess of under "My guess" on the left. If your guess is correct, the new card will be put without being revealed; else, it will be revealed to the opposite (the Heuristic solver).

**Results:**

The winning rate of Heuristic Solver when it plays against Baseline Solver: around 100%.
The winning rate of Heuristic Solver when it plays against Baseline Solver: still testing and will be updated in final report.

**Credits:**
This project makes use of the design of the interface for The Da Vinci Code game from https://github.com/hello-world-zsp/The-Da-Vinci-Code-Board-Game/tree/master
