#!/usr/bin/env python

class HumanPlayer:

    def move(self, ttt):
        vm = ttt.validMoves()
        while True:
            iSpace = int( input("%s's move: " % ttt.whoseTurn()) )
            for m in vm:
                if iSpace == m.iSpace:
                    return m

            print ("Invalid move.  Choose from %s" % validMoves)
