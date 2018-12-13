import copy
import time
import random
from msgame import MSGame

class baseGeneticAlgorithm(object):
    def __init__(self, boardWidth = 5, boardHeight = 3, bombs = 4, populationSize = 10, generationCount = 10, mutationRate = .05, crossoverRate = .75):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.bombs = bombs
        self.populationSize = populationSize
        self.generationCount = generationCount
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate

        self.staticGame = MSGame(boardWidth, boardHeight, bombs)

        self.population = self.generatePopulation(populationSize, boardHeight * boardWidth, bombs)
        self.setMaxFitness()

    def generateChromosome(self, boardSize, bombCount):
        ret = [0] * boardSize
        for i in range(bombCount):
            bomb_idx = random.randint(0, boardSize - 1)
            while ret[bomb_idx] == 1:
                bomb_idx = random.randint(0, boardSize - 1)
            ret[bomb_idx] = 1
        return ret

    def generatePopulation(self, popSize, boardSize, bombCount):
        ret = []
        for i in range(popSize):
            ret.append(self.generateChromosome(boardSize, bombCount))
        return ret

    def fitnessFunction(self, solution, game):
        '''
        Need to implement:
            Takes in a particular solution string and a board to evaluate.
            determines fitness of solution and returns fitness values
            If the solution guesses the correct
        '''
        score, x_cord, y_cord = 0, 0, 0
        board = game.get_mine_map()

        for node in solution:
            if node == 0:
                game.qplay("click", x_cord, y_cord)
                if game.game_status == 2:
                    score = score + 1
                elif game.game_status == 1 or game.game_status == 0:    # game will be over either on a win or loss
                    return score
            elif node == 1:
                game.qplay("flag", x_cord, y_cord)
                if board[y_cord][x_cord] == 1:
                    score = score + 1
                else:
                    score = score - 1
            if x_cord < self.boardWidth - 1:
                x_cord = x_cord + 1
            elif y_cord < self.boardHeight - 1:
                x_cord = 0
                y_cord = y_cord + 1

    def parentalSelection(self, fitPopulation):
        while 1:
            p1 = self.tournament(fitPopulation)
            p2 = self.tournament(fitPopulation)
            return (p1, p2)

    def tournament(self, fitPopulation):
        fit1, ch1 = fitPopulation[random.randint(0, len(fitPopulation) - 1)]
        fit2, ch2 = fitPopulation[random.randint(0, len(fitPopulation) - 1)]
        print ("FIT1", fit1)
        print ("CH1", ch1)
        print ("\n")
        return ch1 if fit1 > fit2 else ch2

    def getFitnessVals(self):
        ret = []
        for chromosome in self.population:
            ret.append(self.fitnessFunction(chromosome, copy.deepcopy(self.staticGame)))
        return ret

    def setMaxFitness(self):
        '''
        Needs to be implemented:
            Needs to set maximum fitness value according to whatever fitness algorithm is being used
        Score will be the length of the chromosome because +1 is given for each correct guess - PG Edit
        '''
        #self.maxFitness = float('inf')
        self.maxFitness = self.boardWidth * self.boardHeight
        return self.maxFitness

    def recombinationAlg(self, tupleList):
        '''
        Need to implement:
            Takes in a list of tuples of form (chromosome, fitness).
            returns a list of chromosomes representing the newly recombined pop
        '''
        pop, fitness = zip(*tupleList)
        return pop

    def mutationAlg(self):
        '''
        Need to implement:
            Updates current population according in desired manner
        '''
        pass

    def getMaxChromosome(self, tupleList):
        maxVal = None
        for item in tupleList:
            if maxVal is None or maxVal < item[1]:
                maxChromosome = item[0]
                maxVal = item[1]
        return maxChromosome

    def runEpoch(self):
        finalChromosome = None
        for generation_idx in range(self.generationCount):
            fitnesses = self.getFitnessVals()
            print(fitnesses)
            popFitness = list(zip(self.population, fitnesses))
            # print(popFitness)
            print ("RETURN STATEMENT: ", self.parentalSelection(popFitness))

            if self.maxFitness == max(fitnesses):
                break
            population = self.recombinationAlg(popFitness)
            self.mutationAlg()
        finalChromosome = self.getMaxChromosome(popFitness)
        return finalChromosome

if __name__ == '__main__':
    random.seed(time.time())
    AI = baseGeneticAlgorithm()
    AI.runEpoch()
    #import code; code.interact(banner='', local = locals())
