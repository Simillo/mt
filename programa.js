const fs = require('fs');

String.prototype.removeSpaces = function () {
  return this.replace(/\s*/g, '');
}

const listObjectsNames = ['states', 'alphabet', 'tapeAlphabet', 'q0'];

const file = fs.readFileSync(process.argv[2]);
const data = 
  file.toString('utf-8')
  .replace(/\{(.*)\}/g, 
    (_, item) => 
      '[' +
      item
        .split(',')
        .map(match => `"${match.trim()}"`)
        .join(',') + ']'
  )
        
  .replace(/\((.*)\)\s*->\s*\((.*)\)(,?)/g,
    (_, reading, transition, eol) =>
      `"${reading.removeSpaces()}": "${transition.removeSpaces()}"${eol}`
  )

  .replace(/\[/g, 
    () =>
      `"${listObjectsNames.shift()}": [`
  )

  .replace('}', '},')
  .replace(/\{/g, '"delta": {')
  .replace('(', '{')
  .replace(/^\)/m, ',')
  .replace(/(B.*B$)/g, '"tape": "$1"}')

const M = JSON.parse(data);
let decomposition = `{${M.q0}}${M.tape}`;
while(true) {
  console.log(decomposition);

  const { state, reading } = /.*\{(?<state>.*)\}(?<reading>.).*/.exec(decomposition).groups;

  const currentTransition = state + ',' + reading;
  const replacement = M.delta[currentTransition];
  if (!replacement) break;

  let [nextState, write, moveTo] = replacement.split(',');
  nextState = '{' + nextState + '}';
  const index = decomposition.indexOf(state) - 1;
  let R = L = '';

  decomposition = decomposition.replace(/{.*}/, '');
  const len = decomposition.length;

  if (moveTo === 'R') {
    R = decomposition.substring(index + 1, len);
    L = decomposition.substring(0, index) + write + nextState;
  } else {
    L = decomposition.substring(0, index - 1);
    R = nextState + decomposition[index - 1] + write + decomposition.substring(index + 1, len);
  }

  decomposition = L + R;
}