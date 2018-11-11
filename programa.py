import fileinput
import re
from collections import defaultdict

'''
M = (Q, Σ, Γ, δ, q0)

Q (Lista de estados)                    = STATES
Σ (Alfabeto)                            = ALPHABET
Γ (Alfabeto da fita (Σ ∪ B))            = TAPE_ALPHABET
δ (Dicionário de funções de transição)¹ = DELTA
q0 (Estado inicial)                     = q0

¹ δ está no formato de dicionário da seguinte maneira:
{
    'qi,x': 'qj,y,D'
}
'''

STATES = []
ALPHABET = []
TAPE_ALPHABET = []
DELTA = defaultdict(list)
q0 = ''

TAPE = ''

def line_to_list (line):
    return line[1:-2].split(',')

found_end_fn = False
for counter, data in enumerate(fileinput.input()):
    line = re.sub(r'[\t\s]', '', data)

    if (counter == 1):
        STATES = line_to_list(line)
        continue
    if (counter == 2):
        ALPHABET = line_to_list(line)
        continue
    if (counter == 3):
        TAPE_ALPHABET = line_to_list(line)
        continue

    if counter > 3 and not found_end_fn and line != '{':
        if line == '}' and not found_end_fn:
            found_end_fn = True
        else:
            FN = re.search(r'\((.*)\)->\((.*)\)', line).groups()
            DELTA[FN[0]] = FN[1]
        continue

    if found_end_fn and counter == len(DELTA) + 6:
        q0 = line
        continue

    if found_end_fn and counter == len(DELTA) + 8:
        TAPE = line
        continue
decomposition = q0 + TAPE
while True:
    print(decomposition)
    transition = re.search(r'.*\{(.*)\}(.).*', decomposition).groups()
    current_state = transition[0]
    reading_symbol = transition[1]
    current_transition = current_state + ',' + reading_symbol

    if current_transition not in DELTA:
        break

    replacement = DELTA[current_transition].split(',')
    next_state = '{' + replacement[0] +'}'
    write = replacement[1]
    move_to = replacement[2]

    index = decomposition.find(current_state) - 1

    decomposition = re.sub(r'\{.*?\}', '', decomposition)

    if (move_to == 'R'):
        R = decomposition[index + 1:]
        L = decomposition[:index] + write + next_state
    else:
        L = decomposition[:index - 1]
        R = next_state + decomposition[index - 1] + write + decomposition[index + 1:]
        
    decomposition = L + R