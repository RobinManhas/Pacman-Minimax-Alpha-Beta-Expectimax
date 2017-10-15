# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]



    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        ##print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        ##print "RM action: ", action
        "*** YOUR CODE HERE ***"
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        total = successorGameState.getScore()
        newPos = successorGameState.getPacmanPosition()
        #print "RM position: ", newPos

        newFood = successorGameState.getFood() # this is food grid
        ##print "RM food: ", newFood

        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ##print "RM scared times: ", newScaredTimes

        #for ghostState in newGhostStates:
            ##print "dir: ", ghostState.getDirection()

        ##print "RM score: ",successorGameState.getScore()
        ##print "RM getLegalPacmanActions: ", currentGameState.getLegalPacmanActions()

        # check end game
        maxNum = 99999
        minNum = -maxNum

        # Robin: states that add to score
        if (successorGameState.isWin()):
            return maxNum
        elif (successorGameState.isLose()):
            return minNum

        if (successorGameState.getNumFood() < currentGameState.getNumFood()):
            total += 300

        # Robin: states that decrease the score
        if(action == Directions.STOP):
            total -= 100

        # RM: check ghost in successor
        for ghost in newGhostStates:
            newGhostPos = ghost.getPosition()
            #print "ghost: ",newGhostPos," ,me: ",newPos
            if(newGhostPos == newPos and ghost.scaredTimer == 0):
                return minNum

        foodDist = 99999

        for foods in newFood.asList():
            dist = util.manhattanDistance(newPos,foods)
            if(dist < foodDist):
                foodDist = dist

        # RM: penalize for more dist
        foodDistance = 5*foodDist
        total -= foodDistance

        # Robin: uncomment corner evaluation to get avg score from 1238.9 to 1257.7
        # corners = currentGameState.getCapsules()
        # if(newPos in corners):
        #     total += 300
        return total

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

        #Your minimax agent (question 2)

    def performMinimax(self, depth, agentIndex, gameState):
        #print "recurse called for agent: ",agentIndex, " , depth: ",depth
        if (gameState.isWin() or gameState.isLose() or depth > self.depth):
            return self.evaluationFunction(gameState)

        ret = []  # RM: stores the return value for this node actions
        todo = gameState.getLegalActions(agentIndex)  # Store the actions
        if Directions.STOP in todo:
            todo.remove(Directions.STOP)

        for action in todo:
            successor = gameState.generateSuccessor(agentIndex, action)
            if((agentIndex+1) >= gameState.getNumAgents()):
                ret += [self.performMinimax(depth+1, 0, successor)]
            else:
                ret += [self.performMinimax(depth, agentIndex+1, successor)]


        if agentIndex == 0:
            if(depth == 1): # if back to root, return action, else ret value
                maxscore = max(ret)
                length = len(ret)
                for i in range(length):
                    if (ret[i] == maxscore):
                        return todo[i]
            else:
                retVal = max(ret)

        elif agentIndex > 0: # ghosts
            retVal = min(ret)

        return retVal


    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        pacmanIndex = 0
        return self.performMinimax(1, pacmanIndex, gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def performAlphaBeta(self, depth, agentIndex, gameState, a, b):
        alpha = a
        beta = b

        if (gameState.isWin() or gameState.isLose() or depth > self.depth):
            return self.evaluationFunction(gameState)

        retList = []  # RM: stores the return value for this node actions
        todo = gameState.getLegalActions(agentIndex)  # Store the actions
        if Directions.STOP in todo:
            todo.remove(Directions.STOP)

        for action in todo:
            successor = gameState.generateSuccessor(agentIndex, action)
            if((agentIndex+1) >= gameState.getNumAgents()):
                ret = self.performAlphaBeta(depth+1, 0, successor, alpha, beta)
            else:
                ret = self.performAlphaBeta(depth, agentIndex+1, successor, alpha, beta)

            #print "ret: ",ret," ,agent: ", agentIndex, " , depth: ", depth, "alpha: ", alpha, " , beta: ", beta
            if(agentIndex == 0 and ret > beta):
                return ret
            if (agentIndex > 0 and ret < alpha):
                return ret

            if (agentIndex == 0 and ret > alpha):
                alpha = ret

            if (agentIndex > 0 and ret < beta):
                beta = ret

            retList += [ret]
        if agentIndex == 0:
            if(depth == 1): # if back to root, return action, else retList value
                maxscore = max(retList)
                length = len(retList)
                for i in range(length):
                    if (retList[i] == maxscore):
                        return todo[i]
            else:
                retVal = max(retList)

        elif agentIndex > 0: # ghosts
            retVal = min(retList)

        return retVal


    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        pacmanIndex = 0
        return self.performAlphaBeta(1, pacmanIndex, gameState, -99999, 99999)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def performExpectimax(self, depth, agentIndex, gameState):
        #print "recurse called for agent: ",agentIndex, " , depth: ",depth
        if (gameState.isWin() or gameState.isLose() or depth > self.depth):
            return self.evaluationFunction(gameState)

        ret = []  # RM: stores the return value for this node actions
        todo = gameState.getLegalActions(agentIndex)  # Store the actions
        if Directions.STOP in todo:
            todo.remove(Directions.STOP)

        for action in todo:
            successor = gameState.generateSuccessor(agentIndex, action)
            if((agentIndex+1) >= gameState.getNumAgents()):
                ret += [self.performExpectimax(depth+1, 0, successor)]
            else:
                ret += [self.performExpectimax(depth, agentIndex+1, successor)]


        if agentIndex == 0:
            if(depth == 1): # if back to root, return action, else ret value
                maxscore = max(ret)
                length = len(ret)
                for i in range(length):
                    if (ret[i] == maxscore):
                        return todo[i]
            else:
                retVal = max(ret)

        elif agentIndex > 0: # ghosts
            s = sum(ret)
            l = len(ret)
            retVal = float(s/l)

        return retVal

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.performExpectimax(1, 0, gameState)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

