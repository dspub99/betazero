#!/usr/bin/env python

import os, sys, time
import numpy as np
import cma
from ticTacToe import TicTacToe
from evaluator import Evaluator
from nnPlayer import NNPlayerFactory
from benchmark import Benchmark
import players


nWorkers = int(sys.argv[1])
opp = sys.argv[2]
outFn = sys.argv[3]

RewardWin = .5
MinLosses = 0
NRounds0 = 100 #max([10, MinLosses])
KRounds = 1.0
MaxNRounds = 100
ThreshOpp = 10
Sigma0 = .1
NRoundsBenchmark = 100
NSeeds = None #MaxNRounds
OneMinute = 60
OneHour = 60*OneMinute
MaxRunningTime = 411 * OneMinute # int(1000 * OneHour) # was 10 hhours
TimeBetweenBenchmarks = 10*OneMinute

Game = TicTacToe
Opponent = players.getPlayer(opp)

CMAOpts = {}

if outFn!="x.json" and os.path.exists(outFn):
    raise Exception("Output path [%s] exists!" % outFn)

nh = [18,18]
npf = NNPlayerFactory(nh = nh)

print ("PARAMS: NRounds0 = %d nWorkers = %d nh = %s MinLosses = %s" % ( NRounds0,  nWorkers, nh, MinLosses))
print ("PARAMS: Sigma0 = %.4e numParams = %d RewardWin = %.4f" % (Sigma0, npf.numParams(), RewardWin))
print ("PARAMS: Opponent = %s NSeeds = %s" % (str(Opponent), NSeeds))
print ("PARAMS: CMAOpts = %s" % (CMAOpts))
es = cma.CMAEvolutionStrategy([0] * npf.numParams(), Sigma0, CMAOpts)

stdMax = 1
nIter = 1
nEval = 0
iBench = 0
wBest = None
bmEst = Benchmark("Est", NRoundsBenchmark, outFn, nWorkers)
gts0 = time.time()
bts0 = gts0
wOpp = es.result[5]
iWOpp = 0
while time.time() - gts0 < MaxRunningTime:
    Opponent.reconfigure(npf(wOpp))
    ev = Evaluator(Game, [Opponent], rW=RewardWin, nWorkers=nWorkers, nSeeds=NSeeds)
    ev.setNRounds(NRounds0)

    ws = es.ask()
    t0 = time.time()
    players = [npf(w) for w in ws]
    phis = np.array([ee.w for ee in ev.evaluate(players)])
    nEval += len(ws)
    t1 = time.time()
    es.tell(ws, -phis)
    ws = np.array(ws)
    t2 = time.time()
    stdw = ws.std(axis=1)
    wEst = es.result[5]
    eeEst = ev.evaluate([npf(wEst)])[0]

    gts = time.time() - gts0
    print ("EVAL: gts = %d nIter = %d dt1 = %.2f dt2 = %.2f nW = %d nRounds = %d iWOpp = %d phiEst = %f phiStd = %f phiMin = %f phiMax = %f stdMean = %.4e stdMax = %.4e meanW2 = %.4e %s" %
           (gts, nIter, t1-t0, t2-t1, len(ws), ev.nRounds, iWOpp,
            eeEst.w, phis.std(), phis.min(), phis.max(), stdw.mean(), stdw.max(), (wEst**2).mean(), eeEst))
    sys.stdout.flush()

    if time.time()-bts0 >= TimeBetweenBenchmarks:
        if NRoundsBenchmark > 0:
            bmEst.benchMark("gts = %d" % gts, npf(wEst))
            iBench += 1
        bts0 = time.time()

    if eeEst.L <= ThreshOpp:
        wOpp = wEst
        iWOpp += 1

    if eeEst.L <= MinLosses:
        dn = max([1, int((KRounds-1) * ev.nRounds)])
        ev.setNRounds( min([MaxNRounds, ev.nRounds + dn]) )

    nIter += 1
    ev.stop()

bmEst.benchMark("gts = %d" % gts, npf(wEst))

