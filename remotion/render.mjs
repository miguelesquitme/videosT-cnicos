import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import path from 'path';
const [,, id, out, propsFile] = process.argv;
const inputProps = propsFile ? JSON.parse((await import('fs')).readFileSync(propsFile, 'utf8')) : {};
const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx'), publicDir: path.resolve('public')});
const browserExecutable = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome';
const composition = await selectComposition({serveUrl, id, inputProps, browserExecutable});
let last = -1;
await renderMedia({composition, serveUrl, codec: 'h264', outputLocation: out, inputProps, browserExecutable, crf: 18,
  concurrency: 2, onProgress: ({progress}) => { const p = Math.floor(progress * 10); if (p !== last) { last = p; console.log('progreso', p * 10, '%'); } }});
console.log('LISTO', out);
