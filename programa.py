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
count = 0
while not is_solved and not is_chomsky_dead:
    print('--------------')
    print(tape)
    transition = re.findall(r'.*\{(.*)\}(.).*', tape)
    current_state = transition[0][0]
    reading_symbol = transition[0][1]
    current_transition = current_state + ',' + reading_symbol

    print ([current_transition])
    print (M[current_transition])
    replacement = M[current_transition].split(',')
    next_state = '{' + replacement[0] +'}'
    write = replacement[1]
    move_to = replacement[2]

    index = tape.find(current_state)

    tape = re.sub(r'\{.*?\}', '', tape)

    index_end_left = index - 1
    index_init_right = index - 1
    L = ''
    R = ''

    if (move_to == 'R'):
        R = tape[index_init_right + 1:]
        L = tape[:index_end_left] + write + next_state
    else:
        L = tape[:index_end_left - 1]
        R = next_state + write + tape[index_init_right:]
        
    tape = L + R
    print(tape, L, R)
