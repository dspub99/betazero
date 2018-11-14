#!/usr/bin/env python

import random

class RandomPlayer:
    def __init__(self):
        self._rand = random.Random()

    def setSeed(self, seed):
        self._rand.seed(seed)

    def move(self, ttt):
        return self._rand.choice(ttt.validMoves())

if __name__=="__main__":
    from ticTacToe import TicTacToe
    import play

    print ("w = %s" % play.play(TicTacToe, RandomPlayer(), RandomPlayer(), bShow = True))

