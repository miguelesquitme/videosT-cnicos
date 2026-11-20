import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
const [,, id, ...secs] = process.argv;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.jsx'), publicDir: path.resolve('public')});
const browserExecutable = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome';
const composition = await selectComposition({serveUrl, id, browserExecutable});
for (const s of secs) {
  await renderStill({composition, serveUrl, output: `/tmp/claude-0/hh/st_${id}_${s}.png`, frame: Math.round(parseFloat(s) * 30), browserExecutable, scale: 0.25});
}
console.log('ok');
