#!/usr/bin/env python

import random, math
import numpy as np
import game
from randomPlayer import RandomPlayer
import play

class OmniscientAdversary:
    def __init__(self, nPlay):
        self._rp = RandomPlayer()
        self._rand = random.Random()
        self._epsSame = 1e-6
        self._nPlay = nPlay

    def __str__(self):
        return "%s nPlay = %d" % (self.__class__.__name__, self._nPlay)

    def reconfigure(self, nn):
        self._nn = nn

    def setSeed(self, seed):
        if seed is None:
            self._rp.setSeed(None)
            self._rand.seed(None)
        else:
            self._rp.setSeed(seed)
            self._rand.seed(seed+1)

    def move(self, ttt):
        bestQ = -1e99
        qs = []
        vm = ttt.validMoves()
        for m in vm:
            q = self._moveQuality(ttt, m)
            if q > bestQ:
                bestQ = q
            qs.append(q)

        bestMoves = []
        for iMove, q in enumerate(qs):
            if abs(q-bestQ) < self._epsSame:
                bestMoves.append(vm[iMove])

        return random.choice(bestMoves)

    def xx_move(self, ttt):
        bestQ = -1e99
        qs = []
        vm = ttt.validMoves()
        for m in vm:
            q = self._moveQuality(ttt, m)
            if q > bestQ:
                bestQ = q
            qs.append(q)

        qs = np.array(qs)
        pMove = qs - qs.min() + 1e-6
        pMove /= pMove.sum()
        return np.random.choice(vm, p=pMove)

    def _moveQuality(self, ttt, m):
        scores = []
        if ttt.whoseTurn() == game.X:
            pX = self._rp
            pO = self._nn
        else:
            pX = self._nn
            pO = self._rp

        nPlay = self._nPlay
        for _ in range(nPlay):
            scores.append(play.simGame(pX, pO, ttt, m))

        scores = np.array(scores)
        return scores.mean()


if __name__ == "__main__":
    from ticTacToe import TicTacToe
    from nnPlayer import NNPlayerFactory

    npf = NNPlayerFactory([18])
    w = np.random.normal(size=(npf.numParams(),))
    player = npf(w)
    adv = OmniscientAdversary(nPlay = 10)
    adv.reconfigure(player)
    print (play.play(TicTacToe, player, adv, True))








