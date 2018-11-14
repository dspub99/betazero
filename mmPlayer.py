#!/usr/bin/env python

import random
from xo import ai
from xo.board import Board
import game

class MMPlayer:
    def __init__(self):
        self.setSeed(None)

    def __str__(self):
        return self.__class__.__name__

    def _convertBoard(self, board):
        outBoard = []
        for r in range(3):
            for c in range(3):
                i = 3*r + c
                if board[i]==game.Empty:
                    t = '.'
                else:
                    t = board[i].lower()
                outBoard.append( t )
        return Board.fromstring(''.join(outBoard))

    def setSeed(self, seed):
        self._rand = random.Random(seed)

    def move(self, ttt):
        (r,c) = self._rand.choice(ai.evaluate(self._convertBoard(ttt.board()), ttt.whoseTurn().lower()).positions)
        iSpace = 3*(r-1) + c-1
        for m in ttt.validMoves():
            if m.iSpace==iSpace:
                return m
        assert(False), "iSpace = %d [%s]" % (iSpace, [str(m) for m in ttt.validMoves()])



if __name__ == "__main__":
    import numpy as np
    import play
    from ticTacToe import TicTacToe
    from randomPlayer import RandomPlayer

    print (play.play(TicTacToe, MMPlayer(), RandomPlayer(), bShow=True))



