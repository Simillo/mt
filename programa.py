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
# Lista representando estados da máquina M.
STATES = []
# Lista representando o Alfabeto (Σ - B).
ALPHABET = []
# Lista representando o Alfabeto da Fita (Σ ∪ B).
TAPE_ALPHABET = []
# Objeto (dicionário) representando o conjunto de estados de transição.
DELTA = defaultdict(list)
# Estado inicial.
q0 = ''
# Fita.
TAPE = ''

# Método auxiliar para trasnformar um string no formato "{.+}" em uma lista. 
def line_to_list (line):
    return line[1:-2].split(',')

# Variável auxiliar para identificar se terminou de montar o objeto de funções de transição.
found_end_fn = False

# Iterador para cara linha do arquivo de entrada.
for counter, data in enumerate(fileinput.input()):

	# Variável representando a linha atual sendo lida do arquivo. Obs.: Expressão regular para remover os espaços (\s) e os tabs (\t).
    line = re.sub(r'[\t\s]', '', data)

	# Quando for a primeira (significante, ignorando o '(' inicial) linha.
    if (counter == 1):
		''' 
		Atribui a lista de estados os estados a linha.
		Ex: {q0, q1, ..., qn},
		e a variável STATES será composta por: ['q1', 'q2', ..., 'qn']
		'''
        STATES = line_to_list(line)
        continue
	# Quando for a segunda (significante, ignorando o '(' inicial) linha.
	if (counter == 2):
		'''
		Atribui a lista de alfabeto os símbolos pertencentes linha sendo lida.
		Ex: {1, X, Y},
		e a variável ALPHABET será composta por: ['1', 'X', 'Y']
		'''
        ALPHABET = line_to_list(line)
        continue
    # Quando for a terceira (significante, ignorando o '(' inicial) linha.
	if (counter == 3):
		'''
		Atribui a lista de alfabeto da fita os símbolos pertencentes linha sendo lida.
		Ex: {1, X, Y, B},
		e a variável TAPE_ALPHABET será composta por: ['1', 'X', 'Y', 'B']
		'''
        TAPE_ALPHABET = line_to_list(line)
        continue
	# Quando terminou de lê as linhas que contêm os estados, alfabeto e alfabeto da fita, começará a preencher o dicionário de funções de transição.
    if counter > 3 and not found_end_fn and line != '{':
		# Se terminar de ler as funções de transições, a flag que encontrou tudo será verdade.
        if line == '}' and not found_end_fn:
            found_end_fn = True
        else:
			'''
			Expressão regular para achar uma linha (que indica uma função de transição) pertencente a linguagem.
			A linha deve está no formato: (qi,y) -> (qj,x,D),
			onde:
				qi = estado atual;
				qj = estado destino;
				y  = símbolo sendo lido;
				x  = símbolo s ser escrito;
				D  = L (left) ou R (right) direção da cabeça de leitura (Obs.: A Máquina de Turing é padrão, ou seja, sem movimento estático).

			O resultado da expressão da função retorna uma lista de grupos achados onde
			o primeiro item da lista é o estado e o símbolo lidos "(qi,x)" 
			e o segundo a o estado destino, símbolo escrito e direção da fita "(qj,y,D)"
			'''
            FN = re.search(r'\((.*)\)->\((.*)\)', line).groups()

			'''
			Monta o dicionário no formato:
			{
			    'qi,x': 'qj,y,D'
			}
			'''
            DELTA[FN[0]] = FN[1]
        continue
	# Terminou de ler as funções de transição, então a próxima linha reprensenta o estado inicial.
    if found_end_fn and counter == len(DELTA) + 6:
        q0 = line
        continue
	# Leu o estado inicial, então a próxima linha representa a fita.
    if found_end_fn and counter == len(DELTA) + 8:
        TAPE = line
        continue

# Representa a fita a ser decomposta no formato "{qi}B...B"
decomposition = q0 + TAPE
while True:
	# Imprimindo a decomposição da fita no terminal cada iteração.
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

    decomposition = re.sub(r'\{.*\}', '', decomposition)

    if (move_to == 'R'):
        R = decomposition[index + 1:]
        L = decomposition[:index] + write + next_state
    else:
        L = decomposition[:index - 1]
        R = next_state + decomposition[index - 1] + write + decomposition[index + 1:]
        
    decomposition = L + R
