// News-image entry for make.fun (Node 22, standard library only).
// The image is drawn at build time by draw_news.py and shipped as
// entry.png beside this file; this program copies it to the output
// directory the grader provides, so both runs write identical bytes.
//
// Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);

if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}
copyFileSync(source, join(outDir, 'entry.png'));
console.log('wrote entry.png to ' + outDir);
