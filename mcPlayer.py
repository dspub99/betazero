#!/usr/bin/env python

import sys, copy, random
import json
import numpy as np
from randomPlayer import RandomPlayer
import play

class MCPlayer:
    def __init__(self, nPlay):
        self._nPlay = nPlay
        self._rp = RandomPlayer()
        self._rand = random.Random()
        self._epsSame = 1e-6

    def __str__(self):
        return "%s(nPlay=%d)" % (self.__class__.__name__, self._nPlay)

    def setSeed(self, seed):
        self._rp.setSeed(seed)
        if seed is not None:
            self._rand.seed(seed+1)
        else:
            self._rand.seed(seed)

    def move(self, ttt):
        bestQ = -1e99
        qs = []
        vm = ttt.validMoves()
        for m in vm:
            q = self.moveQuality(ttt, m)
            # print ("MOVE:", q)
            qs.append(q)
            if q > bestQ:
                bestQ = q

        bestMoves = []
        for iMove, q in enumerate(qs):
            if abs(q-bestQ) < self._epsSame:
                bestMoves.append(vm[iMove])

        return self._rand.choice(bestMoves)

    def moveQuality(self, ttt, m):
        scores = []
        for _ in range(self._nPlay):
            scores.append(play.simGame(self._rp, self._rp, ttt, m))

        scores = np.array(scores)
        return scores.mean()

if __name__ == "__main__":
    from ticTacToe import TicTacToe
    from mmPlayer import MMPlayer
    play.play(TicTacToe, MCPlayer(1), MCPlayer(100), True)

