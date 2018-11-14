#!/usr/bin/env python

from ticTacToe import TicTacToe
import game

class PlayerInterface:
    # return a valid move
    def move(self, game):
        pass

def play(gameClass, pX, pO, bShow = False):
    return playn(gameClass, pX, pO, bShow)[0]

def playn(gameClass, pX, pO, bShow = False):
    ttt = gameClass()
    if bShow: # show empty board
        ttt.dump()
    return playRest(pX, pO, ttt, bShow=bShow, nMoves=99999)

def playRest(pX, pO, ttt, bShow, nMoves):
    p = {game.X:pX, game.O:pO}
    n = 0
    while n < nMoves:
        winner = ttt.checkWinner()
        if winner is not None:
            return (winner, n)
        playOneMove(p, ttt)
        n += 1
        if bShow:
            ttt.dump()
    return (ttt.checkWinner(), n)

def playOneMove(p, ttt):
    marker = ttt.whoseTurn()
    move = p[marker].move(ttt)
    if not ttt.add(move):
        ttt.dump()
        raise Exception("Illegal move: %s" % (move))

def simGame(pX, pO, ttt0, m):
    marker = ttt0.whoseTurn()
    ttt = ttt0.clone()
    ttt.add(m)
    w = ttt.checkWinner()
    if w == marker:
        score1 = 1
    elif w == game.Draw:
        score1 = 0
    elif w is None:
        w = playRest(pX, pO, ttt, False, 99999)[0]
        if w == marker:
            score1 = 1
        elif w == game.Draw:
            score1 = 0
        else:
            score1 = -1
    else:
        assert(False), 'w cannot be [%s] here' % w
    return score1



    
