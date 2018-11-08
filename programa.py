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
for data in fileinput.input():
    line = re.sub(r'[\t\s]', '', data)
    if (counter == 1):
        STATES = line[1:-2].split(',')
    if (counter == 2):
        ALPHABET = line[1:-2].split(',')
    if (counter == 3):
        TAPE_ALPHABET = line[1:-2].split(',')
    
    if (counter > 3 and found_end_fn == False and line != '{'):
        if (line == '}' and not found_end_fn):
            found_end_fn = True
        else:
            FN = re.sub(r'([\(\)]|,$)', '', line).split('->')
            print(FN[0] + ' ' + FN[1])
            if (FN[0] in M):
                M[FN[0]].append(FN[1])
            else:
                M[FN[0]] = [FN[1]]
    counter = counter + 1

# print(STATES)
# print(ALPHABET)
# print(TAPE_ALPHABET)
print(M)
