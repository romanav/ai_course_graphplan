import itertools
from itertools import product


def createDomainFile(domainFileName, n):
    # numbers = list(range(n))  # [0,...,n-1]
    pegs = ['a', 'b', 'c']
    combinations = generate_all_possible_combinations(n)
    possible_peg_switches = get_all_peg_switches()

    for x,y in possible_peg_switches:
        for cx, cy in product(combinations, combinations):
            if is_pegs_state_valid(cx, cy) and is_switch_from_x_to_y_valid(cx, cy):
                print("pre: %s%s %s%s" % (x, cx, y, cy))
                cx_new, cy_new = make_switch(cx, cy)
                print("res: %s%s %s%s\n" % (y, cx_new, y, cy_new))


    # propositions = list(product(pegs, combinations))
    # print (str(list(propositions)))

    # with open(domainFileName, 'w') as domain_file:
    #     domain_file.write("Propositions:\n")
    #     :
    #         comb_str =
    #         domain_file.write("%s%s " % (p, comb_str))


def is_pegs_state_valid(x, y):
    """we check here that ring is not duplicated on pegs"""
    return len(set(x) | set(y)) == len(x) + len(y)


def get_all_peg_switches():
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
    return x_state[0] < y_state[0]

def make_switch(x_state, y_state):
    """
    Make ring switch
    """
    # first need to copy arrays to prevent changes in caller
    x_state = [i for i in x_state]
    y_state = [i for i in y_state]

    ring = x_state.pop(0)
    y_state.insert(0, ring)

    return x_state, y_state


def generate_all_possible_combinations(n):
    """
    This method generate all possible placements of rings on peg including empty peg
    """
    ok_combinations = []
    for x in xrange(0, n):
        # get all possible valid ring combinations for x rings
        ok_combinations += [list(i) for i in list(itertools.combinations(xrange(n), x + 1))]
    return ok_combinations + [[]]


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
