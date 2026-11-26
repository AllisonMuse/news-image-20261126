// Entry point for the "Sum up 26 November's world news in one image" bounty.
// The rendered image lives in the repository as entry.png, next to this file.
// All this program has to do is place an exact copy of it into the
// directory the grader hands us, so the submitted image is the one we drew.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Where the entry image lives: the same folder as this script.
const scriptFolder = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(scriptFolder, "entry.png");

// The grader tells us where to write via MAKEFUN_OUTPUT_DIR.
// Fall back to /output when the variable is not set.
const targetFolder = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const targetImage = join(targetFolder, "entry.png");

// The bounty caps the image at 1 MiB; refuse to hand over anything bigger.
const MAX_BYTES = 1024 * 1024;

if (!existsSync(sourceImage)) {
  console.error(`entry.png not found next to main.ts (${sourceImage})`);
  process.exit(1);
}

const size = statSync(sourceImage).size;
if (size > MAX_BYTES) {
  console.error(`entry.png is ${size} bytes, over the 1 MiB limit`);
  process.exit(1);
}

mkdirSync(targetFolder, { recursive: true });
copyFileSync(sourceImage, targetImage);

console.log(`Wrote ${targetImage} (${size} bytes)`);
