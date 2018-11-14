#!/usr/bin/env python

import sys
import numpy as np
from pool import Pool
from evalWorker import EvalWorker
from evaluation import Evaluation

class Evaluator:
    def __init__(self, gameClass, opponents, rW, nWorkers=1, nSeeds=None):
        self._pool = Pool([EvalWorker(gameClass, opponents, rW) for _ in range(nWorkers)])
        self._pool.start()
        if nSeeds is not None:
            self._seeds = np.random.randint(np.iinfo(np.int32).max, size=(nSeeds,))
        else:
            self._seeds = [None]
        self._nSeeds = len(self._seeds)

    def setNRounds(self, nRounds):
        self._nRounds = nRounds

    @property
    def nRounds(self):
        return self._nRounds

    def evaluate(self, players):
        evs = [Evaluation() for _ in range(len(players))]
        tasks = []
        for iPlayer, player in enumerate(players):
            for iRound in range(self._nRounds):
                    tasks.append( (iPlayer, self._seeds[iRound % len(self._seeds)], player) )

        for i, r in enumerate(self._pool.runTasks(tasks)):
            (iPlayer, w, W, D, L) = r
            evs[iPlayer].update(1, w, W, D, L)

        for ev in evs:
            ev.done()

        return evs

    def stop(self):
        self._pool.stop()



if __name__=="__main__":
    from randomPlayer import RandomPlayer
    from mmPlayer import MMPlayer

    ev = Evaluator(RandomPlayer(), 100, nWorkers=2)
    players = [MMPlayer() for _ in range(1)]
    print (ev.evaluate( players )[0])
    ev.stop()


