import copy
import time
import random
from msgame import MSGame

class baseGeneticAlgorithm(object):
    def __init__(self, boardWidth = 16, boardHeight = 30, bombs = 99, populationSize = 100, generationCount = 100, mutationRate = .05, crossoverRate = .75):
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
        '''
        return 0
        
    def getFitnessVals(self):
        ret = []
        for chromosome in self.population:
            ret.append(self.fitnessFunction(chromosome, copy.deepcopy(self.staticGame)))
        return ret
        
    def setMaxFitness(self):
        '''
        Needs to be implemented:
            Needs to set maximum fitness value according to whatever fitness algorithm is being used
        '''
        self.maxFitness = float('inf')
        
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
            #print(fitnesses)
            popFitness = list(zip(self.population, fitnesses))
            #print(popFitness)
            if self.maxFitness == max(fitnesses):
                break
            population = self.recombinationAlg(popFitness)
            self.mutationAlg()
        finalChromosome = self.getMaxChromosome(popFitness)
        return finalChromosome
            
if __name__ == '__main__':
    random.seed(time.time())
    import code; code.interact(banner='', local = locals())
            