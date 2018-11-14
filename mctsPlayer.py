#!/usr/bin/env python

import numpy as np

from randomPlayer import RandomPlayer
import game
import play

# Run MCTS with MC to estimate the rest of the game.
# http://mcts.ai/about/index.html
# http://ccg.doc.gold.ac.uk/wp-content/uploads/2016/10/browne_tciaig12_1.pdf

class UCT:
    def __init__(self, c):
        self._c = c

    def parts(self, pNode, node):
        return (node.sum/node.n, 2*self._c*np.sqrt(2*np.log(pNode.n) / node.n))

    def __call__(self, pNode, node):
        if node.n == 0:
            return np.inf

        (exploit, explore) = self.parts( pNode, node )
        return exploit + explore

class UCTNegamax:
    def __init__(self, c):
        self._uct = UCT(c)

    def __call__(self, pNode, node):
        if node.n == 0:
            return np.inf

        # pNode.chi gives us negamax
        # Actually, our scores (like node.sum/node.n) are in [0,1] not [-1,1].
        # So to change to the opponent's perspective, we might prefer
        #       scoreOpponent_A = 1 - score
        # to
        #       scoreOpponent_B = -score
        # Note that scoreOpponent_B = scoreOpponent_A - 1.  This offset of -1 in exploit
        #  won't affect which node maximizes exploit + explore.
        (exploit, explore) = self._uct.parts( pNode, node )
        return pNode.chi*exploit + explore

class Node:
    def __init__(self, nprand, ttt, chi, maxPlies, parent=None, move=None):
        self._nprand = nprand
        # each Node has a clone of ttt with the Node's game state
        self.maxPlies = maxPlies
        self.chi = chi
        self.parent = parent
        self.ttt = ttt
        self.move = move
        self.sum = 0
        self.n = 0
        self.children = []
        self._needMoves = list(self.ttt.validMoves())

    def dump(self):
        n = 0
        queue = [self]
        while len(queue) > 0:
            # queue[0].ttt.dump()
            s = [str(n), " "*n]
            newQueue = []
            n += 1
            for node in queue:
                s.append("%d/%d(%d)" % (2*node.sum, 2*node.n, node.maxPlies))
                newQueue.extend(node.children)
            print (' '.join(s))
            queue = newQueue


    def check_parentage(self):
        # Am I may children's parent?
        for c in self.children:
            assert(c.parent == self)
            c.check_parentage()

    def bestChild(self, uct):
        assert(len(self.children)>0)

        phis = []
        for c in self.children:
            # print ("CHILD:", uct(self, c))
            phis.append(uct(self, c))
        phis = np.array(phis)

        i = self._nprand.choice(np.where(phis > phis.max() - 1e-6)[0])
        return self.children[i]

    def findBoard(self, ttt):
        # exactly one ply ahead
        for c in self.children:
            if ttt.equivBoard(c.ttt.board()):
                return c
        return None

    def select(self, uct):
        # "Starting at the root node, a child selection policy is recursively applied to descend
        # through the tree until the most urgent expandable node is reached. A node is expandable if
        # it represents a nonterminal state and has unvisited (i.e. unexpanded) children"

        if len(self._needMoves) > 0:
            return self

        if len(self.children)==0:
            return None

        return self.bestChild(uct).select(uct)

    def expand(self):
        # "One (or more) child nodes are added to expand the tree, according to the
        #  available actions."

        assert( len(self._needMoves) > 0 )

        if self.maxPlies==0:
            # just run another sim from here
            return self

        m = self._nprand.choice(self._needMoves)
        self._needMoves.remove(m)
        ttt = self.ttt.clone()
        ttt.add(m)
        c = Node(self._nprand, ttt, -self.chi, self.maxPlies - 1, self, m.clone())
        self.children.append(c)
        return c

    def backpropagate(self, score):
        # "The simulation result is “backed up” (i.e. backpropagated)
        #  through the selected nodes to update their statistics."

        self.n += 1
        self.sum += score
        if self.parent is not None:
            self.parent.backpropagate(score)

    def __str__(self):
        return "sum = %.4f n = %d nChildren = %d self = %s parent = %s" % (self.sum, self.n, len(self.children), id(self), id(self.parent))


class MCTSPlayer:

    def __init__(self, nPlay, maxPlies, bNegamax, cUct = 1/np.sqrt(2), bDump=False):
        self._nPlay = nPlay
        self._maxPlies = maxPlies
        if bNegamax:
            self._uct = UCTNegamax(cUct)
        else:
            self._uct = UCT(cUct)
        self._cUct = cUct
        self._bNegamax = bNegamax
        self._bDump = bDump
        self._uctMove = UCT(0)
        self._rp = RandomPlayer()
        self._nprand = np.random.RandomState()

        self._root = None

    def __str__(self):
        return ("%s nPlay = %d maxPlies = %d bNegamax = %s cUct = %.4f" %
                (self.__class__.__name__, self._nPlay, self._maxPlies,
                 self._bNegamax, self._cUct))

    def _simulate(self, node):
        # "A simulation is run from the new node(s) according to the
        #  default policy to produce an outcome."
        return play.playRest(self._rp, self._rp, node.ttt.clone(), False, 99999)[0]

    def setSeed(self, seed):
        self._nprand.seed(seed)
        self._rp.setSeed(seed+1)

    def move(self, ttt):
        if self._root is not None:
            self._root = self._root.findBoard(ttt)

        if self._root is None:
            self._root = Node(self._nprand, ttt, 1, maxPlies=self._maxPlies)

        marker = ttt.whoseTurn()
        for _ in range(self._nPlay):
            nodeLeaf = self._root.select(self._uct)
            if nodeLeaf is not None:
                nodeSim = nodeLeaf.expand()
                if nodeSim is not None:
                    # print ("START:", nodeSim.maxPlies, nodeSim.move)
                    w = self._simulate(nodeSim)
                    if w == ttt.whoseTurn():
                        score = 1
                    elif w == game.Draw:
                        score = .5
                    else:
                        score = 0
                    # print ("SCORE:", marker, w, score)
                    nodeSim.backpropagate(score)


        if self._bDump:
            self._root.dump()
        self._root = self._root.bestChild(self._uctMove)
        return self._root.move


    def tests(self):
        self._root.check_parentage()


if __name__ == "__main__":
    from ticTacToe import TicTacToe
    from mmPlayer import MMPlayer
    from mcPlayer import MCPlayer


    nPlay = 100
    maxPlies = 1000
    bNegamax = True
    cUct = 1/np.sqrt(2)
    if True:
        mcts = MCTSPlayer(nPlay = nPlay, maxPlies = maxPlies, bNegamax = bNegamax,
                          cUct = cUct, bDump=True)
        mcts.setSeed(1)
        mc10 = MCPlayer(nPlay=10)
        mc10.setSeed(2)
        play.play(TicTacToe, mcts, mc10, bShow = True)
    else:
        score = []
        for _ in range(100):
            mcts = MCTSPlayer(nPlay = nPlay, maxPlies = maxPlies, bNegamax = bNegamax,
                              cUct = cUct)
            # mc10 vs. mc10 gives .79, fyi
            # mcts100_mp=1_c=1e6 vs. mc 10 gives .82
            # mcts100_mp=1_c=1/sqrt(2) vs. mc 10 gives .82
            # mcts100_mp=1_c=0 vs. mc 10 gives .82
            # mcts100_mp=2_c=0 vs. mc 10 gives .855
            # mcts100_mp=3_c=0 vs. mc 10 gives .83
            # mcts100_mp=3_c=1/sqrt(2) vs. mc 10 gives .86
            # mcts100_mp=3_c=1/sqrt(2)_negamax vs. mc 10 gives .86
            # mcts100_mp=1000_c=1/sqrt(2)_negamax vs. mc 10 gives .83
            # mcts1000_mp=1000_c=1/sqrt(2)_negamax vs. mc 10 gives .94
            # mcts1000_mp=1000_c=1/sqrt(2) vs. mc 10 gives .83
            w = play.play(TicTacToe,  MCPlayer(nPlay=100), mcts, bShow = False)
            if w == 'X':
                score.append(1)
            elif w == 'D':
                score.append(.5)
            else:
                score.append(0)
        print (np.array(score).mean())






