import fileinput
import re
from collections import defaultdict
import sys
sys.tracebacklimit = 0

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
try:
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
except Exception as inst:
    print('A linguagem não pertence a máquina.')

# Representa a fita a ser decomposta no formato "{qi}B...B"
decomposition = q0 + TAPE
while True:
    # Imprimindo a decomposição da fita no terminal cada iteração.
    print(decomposition)
    # Busca na fita a transição atual atribuindo a dois grupos onde o primeiro é o estado atual e o segundo é o símbolo sendo lido.
    transition = re.search(r'.*\{(.*)\}(.).*', decomposition).groups()
    # Atribuindo os grupos encontrados.
    current_state = transition[0]
    reading_symbol = transition[1]
    # Monta uma string no formato "qi,x" válido para uma solução O(1) no dicionário de funções de transição.
    current_transition = current_state + ',' + reading_symbol
    # Se a transição não estiver no conjunto de transições a iteração para.    
    if current_transition not in DELTA:
        break
 
    # Divide a transição em 3 items de uma lista sendo o primeiro o estado destino, o segundo o símbolo a ser escrito e o terceiro para qual direção a cabeça de leitura irá.
    replacement = DELTA[current_transition].split(',')
    # Monta uma string representando o próximo estado no formato "{qj}".
    next_state = '{' + replacement[0] +'}'

    # Símbolo a ser escrito.
    write = replacement[1]
    # Direção da cabeça de leitura.
    move_to = replacement[2]

    # Busca o index do estado na fita decomposta.
    index = decomposition.find(current_state) - 1

    # Remove o que não pertence ao afabeto na fita, ou seja, a substring representando a posição atual da fita ({qj}).
    decomposition = re.sub(r'\{.*\}', '', decomposition)

    # Se a cabeça ir para direita.
    if (move_to == 'R'):
        # A parte da esquerda da fita é tudo até onde a cabeça está + o símbolo escrito + o próximo estado.
        L = decomposition[:index] + write + next_state
        # A parte da direita da fita é composta por tudo após a cabeça de leitura, exceto o símbolo que foi lido.
        R = decomposition[index + 1:]
    # Se a cabeça ir para esquerda.
    else:
        # A parte da esquerda da fita é tudo até onde a cabeça está, exceto o símbolo anterior a própria cabeça.
        L = decomposition[:index - 1]
        # A parte da direita da fita é composta pelo próximo estado mais o símbolo anterior a cabeça mais o símbolo a ser escrito e o resto da fita exceto o símbolo lido.
        R = next_state + decomposition[index - 1] + write + decomposition[index + 1:]
    
    # Monta a nova fita para ser decomposta durante a próxima iteração.
    decomposition = L + R
