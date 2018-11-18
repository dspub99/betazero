# betazero
Tabula Rasa Tic-Tac-Toe

./learnFrom.py 2 oa1 nn.json

# run optimized NN against minimax
./vs.py nn.json mm

# play against the NN
./players.py hu nn.json
# hu - human
# Your moves are specified by an numberin [0,9],
#  which indexes the spaces from upper-left to
#  lower-right.

# play against network from Run #2 into the blog post
./players.py hu run2.json
