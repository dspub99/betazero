#!/usr/bin/env python

import copy

import game

_rows = [0,3,6]
_cols = [0,1,2]


class BoardEvaluator:
    def __init__(self, board):
        self.board = board

    def _rowWinner(self, i0):
        if self.board[i0]==game.Empty:
            return None
        if self.board[i0] == self.board[i0+1] == self.board[i0+2]:
            return self.board[i0]
        return None

    def _colWinner(self, i0):
        if self.board[i0]==game.Empty:
            return None
        if self.board[i0] == self.board[i0+3] == self.board[i0+6]:
            return self.board[i0]
        return None

    def checkWinner(self):
        for i0 in _rows:
            w = self._rowWinner(i0)
            if w is not None:
                return w
        for i0 in _cols:
            w = self._colWinner(i0)
            if w is not None:
                return w

        if self.board[0] != game.Empty:
            if self.board[0] == self.board[4] == self.board[8]:
                return self.board[0]
        if self.board[6] == game.Empty:
            return None
        if self.board[6] == self.board[4] == self.board[2]:
            return self.board[6]

        for b in self.board:
            if b == game.Empty:
                return None # game still in progress
        return game.Draw


class Move:
    def __init__(self):
        self.iSpace = None
        self.marker = None

    @staticmethod
    def make(iSpace, marker):
        m = Move()
        m.iSpace = iSpace
        m.marker = marker
        return m

    def clone(self):
        return Move.make(self.iSpace, self.marker)

    def __str__(self):
        return "iSpace = %d marker = %s" % (self.iSpace, self.marker)

class UndoMove:
    def __init__(self):
        self.iSpace = None
        self.winner = None
        self.turn = None

class TicTacToe:

    def __init__(self, board=None):
        self._markers = [game.X, game.O]
        self._turn = 0  # X always goes first
        if board is None:
            self._board = [game.Empty]*9
        else:
            self._board = board

        self._boardEval = BoardEvaluator(self._board)
        self._winner = self._boardEval.checkWinner()
        self._validMoves = None
        self._moves = [Move() for _ in range(9)]
        self._undo = UndoMove()

    def clone(self):
        ttt = TicTacToe(copy.copy(self.board()))
        ttt._turn = self._turn
        return ttt

    def board(self):
        return self._board

    def validMoves(self):
        if self._validMoves is None:
            vm = []
            iMove = 0
            marker = self.whoseTurn()
            for iSpace, b in enumerate(self._board):
                if b==game.Empty:
                    m = self._moves[iMove]
                    iMove += 1
                    m.iSpace = iSpace
                    m.marker = marker
                    vm.append(m)
            self._validMoves = vm
        return self._validMoves

    def add(self, move):
        if move.marker != self.whoseTurn():
            raise Exception("Wrong player")

        if self._board[move.iSpace]!=game.Empty:
            # Illegal move
            return False

        self._undo.iSpace = move.iSpace
        self._undo.winner = self._winner
        self._undo.turn = self._turn

        self._board[move.iSpace] = move.marker
        self._turn = 1 - self._turn
        self._winner = self._boardEval.checkWinner()
        self._validMoves = None
        
        return True

    def undo(self):
        self._board[self._undo.iSpace] = game.Empty
        self._turn = self._undo.turn
        self._winner = self._undo.winner


    def checkWinner(self):
        return self._winner

    def whoseTurn(self):
        if self._winner is not None:
            return None
        return self._markers[self._turn]

    @staticmethod
    def _printRow(i0, board):
        print ("|", board[i0], board[i0+1], board[i0+2],"|")

    def equivBoard(self, board):
        for i, b in enumerate(self._board):
            if b != board[i]:
                return False
        return True

    def dump(self):
        TicTacToe.dumpBoard(self._board)

    @staticmethod
    def dumpBoard(board):
        for i0 in _rows:
            TicTacToe._printRow(i0, board)
        w = BoardEvaluator(board).checkWinner()
        if w is None:
            print ("No winner")
        elif w==game.Draw:
            print ("Draw")
        else:
            print ("%s wins" % w)




if __name__ == "__main__":

    def colWin():
        ttt = TicTacToe()
        ttt.dump()
        m = ttt.whoseTurn()
        ttt.add(Move.make(4, m))
        ttt.dump()
        m = ttt.whoseTurn()
        ttt.add(Move.make(4, m))
        ttt.dump()

        try:
            ttt.add(Move.make(0, m))
        except Exception as e:
            print (e)

        m = ttt.whoseTurn()
        ttt.add(Move.make(1, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(3, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(7, m))
        ttt.dump()
        assert(ttt.checkWinner()==game.X)

    def diagWin():
        ttt = TicTacToe()
        ttt.dump()
        m = ttt.whoseTurn()
        ttt.add(Move.make(4, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(5, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(2, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(8, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(6, m))
        ttt.dump()
        assert(ttt.checkWinner()==game.X)

    def rowWin():
        ttt = TicTacToe()
        ttt.dump()
        m = ttt.whoseTurn()
        ttt.add(Move.make(7, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(5, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(6, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(2, m))
        ttt.dump()

        m = ttt.whoseTurn()
        ttt.add(Move.make(8, m))
        ttt.dump()
        assert(ttt.checkWinner()==game.X)


if __name__=="__main__":
    colWin()
    diagWin()
    rowWin()










