
import sys
import json_tricks
from ticTacToe import TicTacToe
from evaluator import Evaluator
from mmPlayer import MMPlayer
from randomPlayer import RandomPlayer

class Benchmark:
    def __init__(self, name, nRounds, outFn, nWorkers):
        self._name = name
        self._nRounds = nRounds
        self._outFn = outFn
        self._nWorkers = nWorkers
        self._iBench = 0

    def benchMark(self, tag0, player):
        self._eval("RP %s" % tag0, RandomPlayer(), player)
        self._eval("MMP %s" % tag0, MMPlayer(), player)
        if self._outFn is not None:
            f = open(self._outFn,'w')
            d = {'player': player.sDict()}
            f.write(json_tricks.dumps(d))
            f.close()
        self._iBench += 1

    def _eval(self, tag, opponent, player):
        ev = Evaluator(TicTacToe, [opponent], rW=1, nWorkers=self._nWorkers, nSeeds=None)
        ev.setNRounds(self._nRounds)
        eeEst = ev.evaluate([player])[0]
        phiEst = eeEst.w
        ev.stop()
        print ("BENCHMARK: %s::%s iterBench = %d phiEst = %f eeEst = %s" % (self._name, tag, self._iBench, phiEst, eeEst))
        sys.stdout.flush()
        
