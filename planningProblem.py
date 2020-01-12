from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from Parser import Parser
from action import Action

# try:
#   from search import SearchProblem
#   from search import aStarSearch

# except:
from CPF.search import SearchProblem
from CPF.search import aStarSearch


class PlanningProblem():
    def __init__(self, domain, problem):
        """
        Constructor
        """
        p = Parser(domain, problem)
        self.actions, self.propositions = p.parseActionsAndPropositions()
        # list of all the actions and list of all the propositions
        self.initialState, self.goal = p.pasreProblem()
        # the initial state and the goal state are lists of propositions
        self.createNoOps()  # creates noOps that are used to propagate existing propositions from one layer to the next
        PlanGraphLevel.setActions(self.actions)
        PlanGraphLevel.setProps(self.propositions)
        self._expanded = 0

    def getStartState(self):
        return self.initialState

    def isGoalState(self, state):
        """
        Hint: you might want to take a look at goalStateNotInPropLayer function
        """
        for g in self.goal:
            if g not in state:
                return False

        return True

    def getSuccessors(self, state):
        """
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor, 1 in our case.
        You might want to this function:
        For a list of propositions l and action a,
        a.allPrecondsInList(l) returns true if the preconditions of a are in l
        """
        self._expanded += 1
        successors = []

        for a in self.actions:

            if not a.isNoOp() and a.allPrecondsInList(state):
                # connect states between state and action add and then delete what action remove
                states_dict = dict()
                for i in state:
                    states_dict[i.getName()] = i
                for i in a.getAdd():
                    states_dict[i.getName()] = i
                for i in a.getDelete():
                    if states_dict.has_key(i.getName()):
                        states_dict.pop(i.getName())

                successors.append((states_dict.values(), a, 1))
        return successors

    def getCostOfActions(self, actions):
        return len(actions)

    def goalStateNotInPropLayer(self, propositions):
        """
        Helper function that returns true if all the goal propositions
        are in propositions
        """
        for goal in self.goal:
            if goal not in propositions:
                return True
        return False

    def createNoOps(self):
        """
        Creates the noOps that are used to propagate propositions from one layer to the next
        """
        for prop in self.propositions:
            name = prop.name
            precon = []
            add = []
            precon.append(prop)
            add.append(prop)
            delete = []
            act = Action(name, precon, add, delete, True)
            self.actions.append(act)


def maxLevel(state, problem):
    """
    The heuristic value is the number of layers required to expand all goal propositions.
    If the goal is not reachable from the state your heuristic should return float('inf')
    A good place to start would be:
    propLayerInit = PropositionLayer()          #create a new proposition layer
    for prop in state:
      propLayerInit.addProposition(prop)        #update the proposition layer with the propositions of the state
    pgInit = PlanGraphLevel()                   #create a new plan graph level (level is the action layer and the propositions layer)
    pgInit.setPropositionLayer(propLayerInit)   #update the new plan graph level with the the proposition layer
    """
    propLayerInit = PropositionLayer()  # create a new proposition layer
    for prop in state:
        propLayerInit.addProposition(prop)  # update the proposition layer with the propositions of the state
    pgInit = PlanGraphLevel()  # create a new plan graph level (level is the action layer and the propositions layer)
    pgInit.setPropositionLayer(propLayerInit)

    graph = []
    level = 0
    graph.append(pgInit)

    while problem.goalStateNotInPropLayer(graph[level].getPropositionLayer().getPropositions()):
        if isFixed(graph, level):
            return float("inf")  # this means we stopped the while loop above because we reached a fixed point in the graph. nothing more to do, we failed!

        # self.noGoods.append([])
        level = level + 1
        pgNext = PlanGraphLevel()  # create new PlanGraph object
        pgNext.expandWithoutMutex(graph[level - 1])  # calls the expand function, which you are implementing in the PlanGraph class
        graph.append(pgNext)  # appending the new level to the plan graph

    return level



def levelSum(state, problem):
    """
    The heuristic value is the sum of sub-goals level they first appeared.
    If the goal is not reachable from the state your heuristic should return float('inf')
    """
    "*** YOUR CODE HERE ***"


def isFixed(Graph, level):
    """
    Checks if we have reached a fixed point,
    i.e. each level we'll expand would be the same, thus no point in continuing
    """
    if level == 0:
        return False
    return len(Graph[level].getPropositionLayer().getPropositions()) == len(
        Graph[level - 1].getPropositionLayer().getPropositions())


if __name__ == '__main__':
    import sys
    import time

    if len(sys.argv) != 1 and len(sys.argv) != 4:
        print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
        exit()
    domain = 'dwrDomain.txt'
    problem = 'dwrProblem.txt'
    heuristic = lambda x, y: 0
    if len(sys.argv) == 4:
        domain = str(sys.argv[1])
        problem = str(sys.argv[2])
        if str(sys.argv[3]) == 'max':
            heuristic = maxLevel
        elif str(sys.argv[3]) == 'sum':
            heuristic = levelSum
        elif str(sys.argv[3]) == 'zero':
            heuristic = lambda x, y: 0
        else:
            print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
            exit()

    prob = PlanningProblem(domain, problem)
    start = time.clock()
    plan = aStarSearch(prob, heuristic)
    elapsed = time.clock() - start
    if plan is not None:
        print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
    else:
        print("Could not find a plan in %.2f seconds" % elapsed)
    print("Search nodes expanded: %d" % prob._expanded)
