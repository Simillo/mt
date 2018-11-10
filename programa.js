const fs = require('fs');

String.prototype.removeSpaces = function () {
  return this.replace(/\s*/g, '');
}

const listObjectsNames = ['states', 'alphabet', 'tapeAlphabet', 'q0'];

const file = fs.readFileSync('./entrada.txt');
const data = 
  file.toString('utf-8')
  .replace(/\{(.*?)\}/g, 
    (_, item) => 
      '[' +
      item
        .split(',')
        .map(match => `"${match.trim()}"`)
        .join(',') + ']')
        
  .replace(/\((.*?)\)\s*?->\s*?\((.*?)\)(,?)/g,
    (_, reading, transition, eol) =>
      `"${reading.removeSpaces()}": "${transition.removeSpaces()}"${eol}`)

  .replace(/\[/g, 
    () =>
      `"${listObjectsNames.shift()}": [`)

  .replace('}', '},')
  .replace(/\{/g, '"delta": {')
  .replace('(', '{')
  .replace(')', ',')
  .replace(/(B.*B$)/g, '"tape": "$1"}')

const M = JSON.parse(data);
let decomposition = `{${M.q0}}${M.tape}`;

while(true) {
  const transition = /.*\{(?<state>.*)\}(?<reading>.).*/.exec(decomposition).groups;
  console.log(transition);
  break;
}