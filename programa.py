import fileinput
import re
from collections import defaultdict
STATES = []
ALPHABET = []
TAPE_ALPHABET = []
M = defaultdict(list)
q0 = ''
DECOMPOSITION = ''

counter = 0
found_end_fn = False
line_b4_eof = False
for data in fileinput.input():
    line = re.sub(r'[\t\s]', '', data)
    if (counter == 1):
        STATES = line[1:-2].split(',')
    if (counter == 2):
        ALPHABET = line[1:-2].split(',')
    if (counter == 3):
        TAPE_ALPHABET = line[1:-2].split(',')
    
    if counter > 3 and not found_end_fn and line != '{':
        if line == '}' and not found_end_fn:
            found_end_fn = True
        else:
            FN = re.sub(r'([\(\)]|,$)', '', line).split('->')
            M[FN[0]] = FN[1]

    if found_end_fn and counter == len(M) + 6:
        q0 = line
    
    if found_end_fn and counter == len(M) + 8:
        DECOMPOSITION = line
    counter = counter + 1

is_solved = False
is_chomsky_dead = False

original = DECOMPOSITION
tape = q0 + original

while not is_solved and not is_chomsky_dead:
    transition = re.findall(r'.*\{(.*)\}(.).*', tape)
    current_state = transition[0][0]
    #reading = transition[1]
    print(current_state)
    break
