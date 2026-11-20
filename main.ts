// gta6-meme-x-01 entry program (make.fun program/v1 harness).
//
// The whole contract, from the kit's RULES.txt ("The post file"): this
// repository holds POST.json at its root, naming the X post that is the
// entry, and this program copies POST.json from the repository into the
// output directory. Nothing else is ours to write: the house reads the
// post from X itself and places its own dossier of the post beside our
// copy in /output.
//
// The program is a pure copy on purpose: no network, no wall clock, no
// randomness and no files outside the repository, so two runs over the
// same repository write exactly the same bytes. The one check it does
// make is that POST.json really is a JSON object naming a post, so a
// broken repository fails loudly here instead of at the gate; the copy
// itself is never altered by the check.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

// The grader sets both variables; the defaults match its sandbox
// (repository as working directory, results in /output).
const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postBytes = readFileSync(join(botDir, "POST.json"));

const post: unknown = JSON.parse(postBytes.toString("utf8"));
if (
  typeof post !== "object" ||
  post === null ||
  typeof (post as { url?: unknown }).url !== "string"
) {
  throw new Error('POST.json must be a JSON object of the form {"url": "..."}');
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), postBytes);
