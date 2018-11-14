#!/usr/bin/env python

import sys
import players
from ticTacToe import TicTacToe
from evaluator import Evaluator

nWorkers = int(sys.argv[1])
(p, opp) = players.getPlayers(sys.argv[2], sys.argv[3])
ev = Evaluator(TicTacToe, [opp], rW=1, nWorkers=nWorkers)
ev.setNRounds(100)
print (ev.evaluate([p])[0])
ev.stop()

