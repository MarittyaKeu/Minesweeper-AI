import baseGeneticAlgorithm
import random
import time
import copy

LOSE = 0
WIN = 1
CONTINUE = 2

class basicGA(baseGeneticAlgorithm.baseGeneticAlgorithm):
    def __init__(self, boardWidth = 5, boardHeight = 5, bombs = 10, populationSize = 100, generationCount = 100, crossoverRate = .75, mutationRate = .05):
        super(basicGA,self).__init__(boardWidth,boardHeight,bombs,populationSize,generationCount,crossoverRate,mutationRate)

    def fitnessFunction(self, solution):
        score, x_cord, y_cord = 0, 0, 0

        # Iterates through solution and provides corresponding score
        for node in solution:
            if self.board[y_cord][x_cord] == 0 and node == 0:   # Node in chromosome matches the board
                score = score + 1
            if self.board[y_cord][x_cord] == 1 and node == 1:   # Node in chromosome matches the board
                score = score + 2
            elif node == 0 and self.board[y_cord][x_cord] == 1:    # Mistakes empty tile for bomb tile - loss
                score = score - 10
                # return score + self.checkBombLocation(solution, x_cord, y_cord) - 10    # If the string ends early, add correct bomb location guesses to the score
            elif node == 1 and self.board[y_cord][x_cord] == 0:   # Mistakes bomb tile for empty tile - minus 1pt
                score = score - 5

            # Iterates to the next coordinate on the board
            if x_cord < self.boardWidth - 1:
                x_cord = x_cord + 1
            elif y_cord < self.boardHeight - 1:
                x_cord = 0
                y_cord = y_cord + 1

        return score

    def checkBombLocation(self, solution, x_cord, y_cord):
        """
            Continues where the last iteration left off. +2pts for every correct bomb location
        """
        score = 0
        x_cord = x_cord
        y_cord = y_cord

        num = (y_cord * self.boardWidth) + x_cord
        for node in solution[num:]:
            if node == 1:
                if node == self.board[y_cord][x_cord]:
                    score = score + 2
                else:
                    score = score - 5
            if x_cord < self.boardWidth - 1:
                x_cord = x_cord + 1
            elif y_cord < self.boardHeight - 1:
                x_cord = 0
                y_cord = y_cord + 1
        return score

    def setMaxFitness(self):
        """
            1pt for correct empty tile guess
            2pts for every correct bomb guess
            -1pt for every incorrect flag
        """
        self.maxFitness = (self.boardHeight * self.boardWidth) + self.bombs

    def parentSelection(self, sortedTuples):
        '''
        Need to implement:
            Takes in list of tuples of form (chromosome, fitness)
            returns tuple of form (parentChromosome1, parentChromosome2)
        '''
        parList = []
        for i in range(5):
            parList.append(sortedTuples[random.randint(0,self.populationSize - 1)])
        parent1 = max(parList, key=lambda item:item[1])
        parList.remove(parent1)
        parent2 = max(parList, key=lambda item:item[1])
        return (parent1[0],parent2[0])

    def crossoverAlg(self, parents):
        '''
        Need to implement:
            Takes in a tuple of form (parentChromosome1, parentChromosome2)
            Returns a tuple of form (childChromsome1, childChromsome2)
        '''
        pars = copy.copy(parents)
        parent1 = pars[0]
        parent2 = pars[1]

        usedPoints = set()
        for i in range(self.bombs // 2):
            crossPoint = random.randint(0, self.bombs - 1)
            while crossPoint in usedPoints:
                crossPoint = random.randint(0, self.bombs - 1)
            usedPoints.add(crossPoint)

            old_idx_1 = (parent1[1])[crossPoint]
            old_idx_2 = (parent2[1])[crossPoint]
            if (parent1[0])[old_idx_2] == 0:
                (parent1[0])[old_idx_1] = 0
                (parent1[1])[crossPoint] = old_idx_2
                (parent1[0])[old_idx_2] = 1

            if (parent2[0])[old_idx_1] == 0:
                (parent2[0])[old_idx_2] = 0
                (parent2[1])[crossPoint] = old_idx_1
                (parent2[0])[old_idx_1] = 1

        return (parent1,parent2)

    def mutationAlg(self):
        '''
        Need to implement:
            Updates current population according in desired manner
        '''

        threshhold = self.mutationRate * 100
        for ch in self.population:
            for i in range(len(ch[1])):
                if random.randint(0,100) < threshhold:
                    cur_idx = (ch[1])[i]
                    new_idx = random.randint(0,len(ch[0]) - 1)
                    if (ch[0])[new_idx] != 1:
                        (ch[0])[new_idx] = 1
                        (ch[0])[cur_idx] = 0
                        (ch[1])[i] = new_idx


if __name__ == '__main__':
    random.seed(time.time())
    import code; code.interact(banner='', local = locals())
