#!/usr/bin/env node
// Valida la sintaxis de los <script> inline de los HTML del repo.
// No requiere dependencias: extrae el código y lo compila con `new Function`.
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const root = process.argv[2] || '.';
const files = [];
(function walk(dir){
  for(const name of readdirSync(dir)){
    if(name === 'node_modules' || name === '.git' || name === '.vercel') continue;
    const p = join(dir, name);
    if(statSync(p).isDirectory()) walk(p);
    else if(extname(p).toLowerCase() === '.html') files.push(p);
  }
})(root);

let failed = 0;
for(const file of files){
  const html = readFileSync(file, 'utf8');
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let m, i = 0;
  while((m = re.exec(html))){
    i++;
    const attrs = m[1] || '';
    const code = m[2] || '';
    if(/\bsrc\s*=/i.test(attrs)) continue;      // script externo: no se comprueba aquí
    if(!code.trim()) continue;
    try{
      // eslint-disable-next-line no-new-func
      new Function(code);
      console.log(`OK   ${file} <script #${i}> (${code.split('\n').length} líneas)`);
    }catch(err){
      failed++;
      console.error(`FAIL ${file} <script #${i}>: ${err.message}`);
    }
  }
}

if(!files.length){
  console.error('No se encontró ningún HTML que validar.');
  process.exit(1);
}
if(failed){
  console.error(`\n${failed} script(s) con errores de sintaxis.`);
  process.exit(1);
}
console.log('\nJS inline OK');
