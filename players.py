#!/usr/bin/env python

import json_tricks
from ticTacToe import TicTacToe
from mmPlayer import MMPlayer
from mcPlayer import MCPlayer
from nnPlayer import NNPlayer
from oaPlayer import OmniscientAdversary
from mctsPlayer import MCTSPlayer
from humanPlayer import HumanPlayer
from randomPlayer import RandomPlayer

def getPlayer(nn):
    if nn.endswith(".json"):
        return NNPlayer(json_tricks.loads(open(nn).read())['player'])
    elif nn=='mm':
        return MMPlayer()
    elif nn[:4]=='mcts':
        return MCTSPlayer(nPlay=int(nn[4:]), maxPlies=9999, bNegamax=True)
    elif nn[:2]=='mc':
        return MCPlayer(nPlay=int(nn[2:]))
    elif nn=='rp':
        return RandomPlayer()
    elif nn=='hu':
        return HumanPlayer()
    elif nn[:2]=='oa':
        return OmniscientAdversary(nPlay=int(nn[2:]))
    else:
        raise Exception("Unsupported player [%s]" % nn)

def getPlayers(key1, key2):
    p1 = getPlayer(key1)
    p2 = getPlayer(key2)

    if getattr(p1, 'reconfigure', None) is not None:
        p1.reconfigure(p2)
    elif getattr(p2, 'reconfigure', None) is not None:
        p2.reconfigure(p1)

    return (p1,p2)

if __name__=="__main__":
    import sys
    import play

    (p1,p2) = getPlayers(sys.argv[1], sys.argv[2])

    play.play(TicTacToe, p1, p2, bShow=True)


