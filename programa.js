// FileSystem do NodeJS para manipular arquivos.
const fs = require('fs');

// Método auxiliar para remover espaços de uma string.
String.prototype.removeSpaces = function () {
  return this.replace(/\s*/g, '');
}

// Definindo uma lista de propriedades para o objeto final que representa a Máquina de turing.
const listObjectsNames = ['states', 'alphabet', 'tapeAlphabet', 'q0'];

/**
 *Lê o arquivo passado pelos args do CLI.
 * Formato: node programa.js entrada.txt
 */ 
const file = fs.readFileSync(process.argv[2]);

// Realizando o parser do arquivo.
const data = 

  /**
   * Converte os chunks (em ASCII) para UTF-8.
   * Transforma o conteúdo do arquivo em um arquivo JSON válido. 
   */
  file.toString('utf-8')
  
  /**
   * Para toda ocorrência do estilo: {.*} transformar em [.*].
   * Exemplo: {q0, q1, q2} para ["q0", "q1", "q2"]
   */
  .replace(/\{(.*)\}/gm, 
    (_, item) => 
      '[' +
      item
        .split(',')
        .map(match => `"${match.trim()}"`)
        .join(',') + ']'
  )

  /**
   * Transformas as funções de transição em um objeto JSON válido no formato domínio-imagem,
   * onde o domínio é uma propriedade do objeto a imagem e seu valor.
   * Exemplo: (q0, B) -> (q1, B, R) para "q0,B": "q1,B,R"
   */
  .replace(/\((.*)\)\s*->\s*\((.*)\)(,?)/gm,
    (_, reading, transition, eol) =>
      `"${reading.removeSpaces()}": "${transition.removeSpaces()}"${eol}`
  )

  //Faz alterações finais na estrutura do arquivo (trocar "(" e ")" por "{" e "}" respectivamente, por exemplo).
  .replace(/\[/gm, 
    () =>
      `"${listObjectsNames.shift()}": [`
  )
  .replace('}', '},')
  .replace('{', '"delta": {')
  .replace('(', '{')
  .replace(/\)$/m, ',')
  .replace(/(B.*B$)/g, '"tape": "$1"}');

/**
 * Faz o parser final da string representando o arquivo em um objeto JSON válido.
 * 
 * M = (Q, Σ, Γ, δ, q0)
 * Q (Lista de estados)                    = M.states
 * Σ (Alfabeto)                            = M.alphabet
 * Γ (Alfabeto da fita (Σ ∪ B))            = M.tapeAlphabet
 * δ (Dicionário de funções de transição)¹ = M.delta
 * q0 (Estado inicial)                     = M.q0
 *  
 * ¹ δ está no formato de um objeto da seguinte maneira:
 * {
 *     'qi,x': 'qj,y,D'
 * }
 */
const M = JSON.parse(data);

// Representação da fita a ser decomposta.
let decomposition = `{${M.q0[0]}}${M.tape}`;

// Loop infinito (até não encontrar uma transição válida).
while(true) {
  // Imprime a fita no formato "B.*{estado}.*B".
  console.log(decomposition);

  // ER para ler a decomposição o estado atual e o símbolo que está lendo.
  const { state, reading } = /.*\{(?<state>.*)\}(?<reading>.).*/.exec(decomposition).groups;

  // Monta uma string no estilo "<estado>,<leitura>", que se válido tenta achar uma imagem no objeto de transições.
  const currentTransition = state + ',' + reading;

  // Acessa o objeto que contém as funções de transição e retorna sua imagem.
  const replacement = M.delta[currentTransition];
  // Se não achar o loop para, pois não existe mais transições.
  if (!replacement) break;

  // Desctrutor dos resultado da imagem no formato "<próximo estado>,<símbolo a ser escrito>,<direita ou esquerda>".
  let [nextState, write, moveTo] = replacement.split(',');
  // Monta uma string a ser escrita para a próxima decomposição.
  nextState = '{' + nextState + '}';

  // Busca o index da posição da cabeça na string decomposta.
  const index = decomposition.indexOf(state) - 1;

  // Right e Left, a decomposição será a concatenação de R + L.
  let R = L = '';

  // Remove a string da cabeça (a essa altura já se sabe onde está a cabeça e não é necessário manter ela na fita).
  decomposition = decomposition.replace(/{.*}/, '');
  // Tamanho da fita sem a cabeça.
  const len = decomposition.length;

  // Se a cabeça ir para direita...
  if (moveTo === 'R') {
    // A direita da nova fita é tudo, exceto o símbolo sendo lido.
    R = decomposition.substring(index + 1, len);
    // A esquerda da nova fita é tudo que existia mais o símbolo a ser escrito mais a cabeça mais o novo estado.
    L = decomposition.substring(0, index) + write + nextState;

  // ... se ir para esquerda.
  } else {
    // A esquerda da nova fita é tudo que existia exceto o símbolo anterior a cabeça.
    L = decomposition.substring(0, index - 1);
    // A direita da nova fita é composta pelo novo estado, o primeiro símbolo antes da cabeça, o símbolo a ser escrito e o resto da fita a direita da cabeça.
    R = nextState + decomposition[index - 1] + write + decomposition.substring(index + 1, len);
  }

  // Monta a nova fita.
  decomposition = L + R;
}