const fs = require('fs');

String.prototype.removeSpaces = function () {
  return this.replace(/\s*/g, '');
}

const listObjectsNames = ['states', 'alphabet', 'tapeAlphabet', 'q0'];

const file = fs.readFileSync('./entrada.txt');
const data = file.toString('utf-8');
const str = data
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
console.log(JSON.parse(str));
// console.log((str));