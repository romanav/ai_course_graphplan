import itertools
from itertools import product


def createDomainFile(domainFileName, n):
    pegs = ['a', 'b', 'c']
    combinations = generate_all_possible_combinations(n)
    possible_peg_switches = get_all_peg_switches()

    with open(domainFileName, 'w') as domain_file:
        domain_file.write("Propositions:\n")
        for p, x in product(pegs, combinations):
            domain_file.write(str(p) + str(x).replace(' ', '') + " ")

        domain_file.write('Actions:\n')
        for x, y in possible_peg_switches:
            for cx, cy in product(combinations, combinations):
                if is_pegs_state_valid(cx, cy) and is_switch_from_x_to_y_valid(cx, cy):
                    pre = "%s%s %s%s" % (x, lst_to_str(cx), y, lst_to_str(cy))  # preconditions formatting
                    domain_file.write("Name: S_" + pre.replace(' ', '') + '\n')  # action name just as precondition
                    domain_file.write("pre: " + pre + '\n')  # precondition
                    cx_new, cy_new = make_switch(cx, cy)
                    # add next state and delete precondition
                    domain_file.write("add: %s%s %s%s" % (y, lst_to_str(cx_new), y, lst_to_str(cy_new)) + '\n')
                    domain_file.write("delete: " + pre + '\n')


def lst_to_str(l):
    """This method get array and delete white spaces from it"""
    return str(l).replace(' ', '')


def is_pegs_state_valid(x, y):
    """we check here that ring is not duplicated on pegs"""
    return len(set(x) | set(y)) == len(x) + len(y)


def get_all_peg_switches():
    """
    This method return all permutations of pegs for example (a,b) and also (b,a)
    We use it program transfer from a to b and also from b to a (left to right)
    """
    pegs = ['a', 'b', 'c']
    to_return = list(itertools.combinations(pegs, 2))
    pegs.reverse()
    to_return += list(itertools.combinations(pegs, 2))
    return to_return


def is_switch_from_x_to_y_valid(x_state, y_state):
    if len(x_state) == 0:
        return False
    if len(y_state) == 0:
        return True
    return x_state[-1] < y_state[-1]


def make_switch(x_state, y_state):
    """
    Make ring switch
    """
    # first need to copy arrays to prevent changes in caller
    x_state = [i for i in x_state]
    y_state = [i for i in y_state]

    y_state.append(x_state.pop())

    return x_state, y_state


def generate_all_possible_combinations(n):
    """
    This method generate all possible placements of rings on peg including empty peg
    """
    ok_combinations = []
    for x in xrange(0, n):
        # get all possible valid ring combinations for x rings
        ok_combinations += [list(i) for i in list(itertools.combinations(xrange(n), x + 1))]

    # we want to present the lowest ring coming first in array
    for i in ok_combinations:
        i.reverse()

    # empty peg it's something we need to consider also
    return [[]] + ok_combinations


def createProblemFile(problemFileName, n):
    numbers = list(range(n))  # [0,...,n-1]
    pegs = ['a', 'b', 'c']
    problemFile = open(problemFileName, 'w')  # use problemFile.write(str) to write to problemFile
    "*** YOUR CODE HERE ***"

    problemFile.close()


import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: hanoi.py n')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    domainFileName = 'hanoi' + str(n) + 'Domain.txt'
    problemFileName = 'hanoi' + str(n) + 'Problem.txt'

    createDomainFile(domainFileName, n)
    createProblemFile(problemFileName, n)
