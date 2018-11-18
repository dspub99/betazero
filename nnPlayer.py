#!/usr/bin/env python

from collections import OrderedDict
import numpy as np
import random
import game
from nn import NNFactory, NN

NX = 18

class NNPlayerFactory:
    def __init__(self, nh):
        self._nnf = NNFactory(NX, 1, nh)

    def numParams(self):
        return self._nnf.numParams()

    def __call__(self, w):
        return NNPlayer(self._nnf(w))

class NNPlayer:
    def __init__(self, nn):
        if type(nn) == type(OrderedDict()):
            self._nn = NN(nn['player'])
        else:
            self._nn = nn
        self._x = np.zeros(shape=(NX,))
        self._epsSame = 1e-2
        self._rand = random.Random()
        
    def setName(self, n):
        self._name = n

    def setSeed(self, seed):
        self._rand.seed(seed)

    def name(self):
        return self._name

    def sDict(self):
        return {'player': self._nn.sDict()}
    
    def _encodeBoard(self, ttt):
        marker = ttt.whoseTurn()
        for i,b in enumerate(ttt.board()):
            if b==game.Empty:
                self._x[i] = 0
                self._x[i+9] = 0
            elif b == marker:
                self._x[i] = 1
                self._x[i+9] = 0
            else:
                self._x[i] = 0
                self._x[i+9] = 1

    def move(self, ttt):
        return self.moveAndValue(ttt)[0]

    def moveAndValue(self, ttt):
        self._encodeBoard(ttt)
        bestQ = -1e99
        qs = []
        vm = ttt.validMoves()
        for m in vm:
            ttt.add(m)
            self._encodeBoard(ttt)
            q = self._nn(self._x)[0]
            ttt.undo()
            self._encodeBoard(ttt)
            qs.append(q)
            if q > bestQ:
                bestQ = q

        bestMoves = []
        for iMove, q in enumerate(qs):
            if abs(q-bestQ) < self._epsSame:
                bestMoves.append(vm[iMove])
            
        return (self._rand.choice(bestMoves), bestQ, qs)


if __name__ == "__main__":
    from ticTacToe import TicTacToe
    import play

    npf = NNPlayerFactory([9])
    w = np.random.normal(size=(npf.numParams(),))
    player = npf(w)
    opponent = npf(w)
    play.play(TicTacToe, player, opponent, bShow=True)

