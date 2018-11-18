# betazero
Tabula Rasa Tic-Tac-Toe

See [the blog post](https://dspub99.github.io/betazero/betazero.html) for details.


Optimize a neural network tic-tac-toe-playing agent
 from random weights using self-play

 ./learnFrom.py 2 oa1 nn.json


Run optimized NN against minimax

 ./vs.py nn.json mm


Play against the NN

 ./players.py hu nn.json


hu - human
Your moves are specified by an numberin [0,9],
 which indexes the spaces from upper-left to
 lower-right.


Play against network from Run #2 into the blog post

 ./players.py hu run2.json
