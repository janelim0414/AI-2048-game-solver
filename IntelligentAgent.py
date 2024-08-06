# Name: Jane Lim
# UNI: jl6094

import random
from BaseAI import BaseAI
import time
import math

timeLimit = 0.2

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        # start the timer for each branch, allow 0.2 seconds for each iteration
        self.prevTime = time.process_time()
        for i in range(0, 4):
            output = self.maximize(grid, float('-inf'), float('inf'), i)
        return output[0][0]

    # min node (computer)
    def minimize(self, grid, a, b, depth, value):
        moveset = grid.getAvailableCells()
        # if computer is able to insert a new tile
        if moveset and time.process_time() - self.prevTime < timeLimit and depth > 0:
            depth -= 1
            (minchild, minutil) = (None, float('inf'))
            for move in moveset:
                # insert new tile in the available cell
                grid.setCellValue(move, value)
                util = self.maximize(grid, a, b, depth)[1]
                grid.setCellValue(move, 0)
                # if current node minimizes
                if util < minutil:
                    # minimize and update beta
                    (minchild, minutil) = (move, util)
                # if it doesn't minimize, check for a - b pruning
                if minutil <= a:
                    break
                if minutil < b:
                    b = minutil
            return minchild, minutil
        # else, the node is a terminal
        else:
            # re-start the timer for next branch
            self.prevTime = time.process_time()
            return None, self.eval(grid)

    # max node (player)
    def maximize(self, grid, a, b, depth):
        moveset = grid.getAvailableMoves()
        # if player is able to make a move
        if moveset and time.process_time() - self.prevTime < 0.2 and depth > 0:
            depth -= 1
            (maxchild, maxutil) = (None, float('-inf'))
            for move in moveset:
                util2 = self.minimize(move[1], a, b, depth, 2)[1]
                util4 = self.minimize(move[1], a, b, depth, 4)[1]
                util = util2 * 0.9 + util4 * 0.1

                # if current node maximizes
                if util > maxutil:
                    # maximize and update beta
                    (maxchild, maxutil) = (move, util)
                # if it doesn't maximize, check for a - b pruning
                if maxutil >= b:
                    break
                if maxutil > a:
                    a = maxutil
            return maxchild, maxutil
        # else, the node is a terminal
        else:
            # re-start the timer for next branch
            self.prevTime = time.process_time()
            return None, self.eval(grid)



    def eval(self, grid):
        return self.monotonicity(grid) + 0.7 * self.smoothness(grid) + 100 * len(grid.getAvailableCells()) + math.log2(grid.getMaxTile())

    def monotonicity(self, grid):
        score1, score2, score3, score4 = 0, 0, 0, 0
        # weight matrices that represents 4 possible monotonic grid structure
        m1 = [[2 ** 6, 2 ** 5, 2 ** 4, 2 ** 3],
              [2 ** 5, 2 ** 4, 2 ** 3, 2 ** 2],
              [2 ** 4, 2 ** 3, 2 ** 2, 2 ** 1],
              [2 ** 3, 2 ** 2, 2 ** 1, 1]]
        m2 = [[2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6],
              [2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5],
              [2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4],
              [1, 2 ** 1, 2 ** 2, 2 ** 3]]
        m3 = [[1, 2 ** 1, 2 ** 2, 2 ** 3],
              [2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4],
              [2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5],
              [2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6]]
        m4 = [[2 ** 3, 2 ** 2, 2 ** 1, 1],
              [2 ** 4, 2 ** 3, 2 ** 2, 2 ** 1],
              [2 ** 5, 2 ** 4, 2 ** 3, 2 ** 2],
              [2 ** 6, 2 ** 5, 2 ** 4, 2 ** 3]]
        # check monotonicity for every corner in the grid
        for row in range(0, 4):
            for col in range(0, 4):
                score1 = grid.map[row][col] * m1[row][col] + score1
                score2 = grid.map[row][col] * m2[row][col] + score2
                score3 = grid.map[row][col] * m3[row][col] + score3
                score4 = grid.map[row][col] * m4[row][col] + score4

        return max(score1, score2, score3, score4)

    def smoothness(self, grid):
        directionVectors = ((-1, 0), (1, 0), (0, -1), (0, 1))
        score = 0
        for row in range(0, 4):
            for col in range(0, 4):
                if grid.map[row][col]:
                    # Look Adjacent Cell Value
                    for i in range(4):
                        move = directionVectors[i]
                        adjCellValue = grid.getCellValue((row + move[0], col + move[1]))
                        if adjCellValue:
                            score -= abs(adjCellValue - grid.map[row][col])
                        # If Value is the Same
                        # if adjCellValue == grid.map[row][col] and adjCellValue:
                        #     score += 1

        return score
