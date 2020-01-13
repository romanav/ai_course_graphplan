import itertools
from itertools import product


def createDomainFile(domainFileName, n):
    # numbers = list(range(n))  # [0,...,n-1]
    pegs = ['a', 'b', 'c']

    string_combinations = []

    for rings in xrange(0, n):
        # get all possible ring combinations even not permitted
        combinations_list = [i for i in itertools.combinations(xrange(n), rings + 1)]

        # filter all combinations that are ok and write them to the output
        for combination in combinations_list:
            if all(combination[i] <= combination[i + 1] for i in xrange(len(combination) - 1)):  # is sorted tuple
                string_combinations.append(''.join(map(str, combination)))

    with open(domainFileName, 'w') as domain_file:
        domain_file.write("Propositions:\n")
        for i in product(pegs, string_combinations):
            domain_file.write("%s%s " % i)

    # propositions = ["%s%d" % (peg, number) for peg, number in product(pegs, range(n))]

    # with open(domainFileName, 'w') as domain_file:  # use domainFile.write(str) to write to domainFile
    #     domain_file.write("Propositions:\n")
    #     for i in propositions:
    #         domain_file.write(i+" ")
    #     domain_file.write("\nActions:\n")


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
