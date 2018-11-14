
import sys, random
import numpy as np

import play
import game

class EvalWorker:
    def __init__(self, gameClass, opponents, rW):
        self._gameClass = gameClass
        self._rW = rW
        try:
            self._opponents = list(opponents)
        except:
            self._opponents = [opponents]

        self._reconfigures = []
        for opponent in self._opponents:
            self._reconfigures.append(getattr(opponent, 'reconfigure', None))

    def _reconfigure(self, player):
        return # TEST 
        for reconfigure in self._reconfigures:
            if reconfigure is not None:
                reconfigure(player)

    def __call__(self, task):
        (iPlayer, seed, player) = task
        self._reconfigure(player)

        totW = 0
        norm = 0
        (W,D,L) = (0,0,0)
        for opponent in self._opponents:
            for playerMarker in ['X', 'O']:
                opponent.setSeed(seed)
                if playerMarker == 'X':
                    w = play.play(self._gameClass, player, opponent)
                else:
                    w = play.play(self._gameClass, opponent, player)

                if w==playerMarker:
                    totW += self._rW
                    W += 1
                elif w==game.Draw:
                    totW += .5
                    D += 1
                else:
                    L += 1
                norm += 1
        self._reconfigure(None)

        return (iPlayer, totW/norm, W/norm, D/norm, L/norm)

                

