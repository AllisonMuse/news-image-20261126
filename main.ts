// The World in One Day — 26 November 2026. Entry program for make.fun's
// "Sum up 26 November's world news in one image" bounty (Node 22, standard
// library only). The image itself was drawn at build time by draw_news.py and
// ships in this repository as entry.png; this program's only job is to place
// that exact file into the output directory the grader provides, so the two
// runs the grader does write byte-identical files.
//
// Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const imagePath = join(here, 'entry.png');

const image = statSync(imagePath);
if (image.size > 1024 * 1024) {
  throw new Error('entry.png is over the 1 MiB limit: ' + image.size + ' bytes');
}

mkdirSync(outputDir, { recursive: true });
const destination = join(outputDir, 'entry.png');
copyFileSync(imagePath, destination);

const written = statSync(destination);
console.log(
  'entry.png (' + written.size + ' bytes) copied to ' + destination,
);
