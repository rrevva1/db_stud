import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const utf8 = "utf8";

const p1 = fs.readFileSync(path.join(__dirname, "enhance_p6_p9.py"), utf8);
const p2 = fs.readFileSync(path.join(__dirname, "enhance_p6_p9_part2.py"), utf8);
const helpers = fs.readFileSync(path.join(__dirname, "lessons_helpers.mjs"), utf8);

const start = p1.indexOf("# ===== PART 6 =====");
const end = p1.indexOf("# Continue in part 2");
const p6block = p1.slice(start, end).trim();
const p7block = p2.slice(p2.indexOf("# ===== PART 7 =====")).trim();

let combined = helpers + "\n" + p6block + "\n" + p7block;

function pyTripleToJsString(code) {
  return code.replace(/"""([\s\S]*?)"""/g, (_, content) => JSON.stringify(content));
}

combined = combined.replace(/^# /gm, "// ");
combined = combined.replace(/\("([^"]+)", "([^"]+)"\)/g, '["$1", "$2"]');
combined = combined.replace(/"md": md\(/g, "md: md(");
combined = combined.replace(/"quiz": quiz\(/g, "\n  quiz: quiz(");
combined = pyTripleToJsString(combined);
combined = combined.replace(/"tasks": /g, "\n  tasks: ");
combined = combined.replace(/\]\),\s*\n\s*, quiz:/g, "]),\n  quiz:");
combined = combined.replace(/\]\),\s*\n\s*, tasks:/g, "]),\n  tasks:");
combined = combined.replace(/,\s*\n\s*, quiz:/g, ",\n  quiz:");
combined = combined.replace(/,\s*\n\s*, tasks:/g, ",\n  tasks:");
combined = combined.replace(/\[\[(\[")/g, "[$1");
combined = combined.replace(/extra=("(?:[^"\\]|\\.)*")\)/g, "$1)");
combined = combined.replace(/\],\s*\n\s*, "/g, '],\n    "');

const header = `import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT_DIRS = [path.join(ROOT, "content", "lessons"), path.join(ROOT, "public", "content", "lessons")];
let count = 0;
`;

const footer = `
for (const [id, content] of Object.entries(LESSONS)) {
  for (const dir of OUT_DIRS) {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, id + ".md"), content.md.trim() + "\\n", "utf8");
    fs.writeFileSync(path.join(dir, id + ".quiz.json"), JSON.stringify(content.quiz, null, 2) + "\\n", "utf8");
    fs.writeFileSync(path.join(dir, id + ".tasks.md"), content.tasks.trim() + "\\n", "utf8");
  }
  count += 3;
}
console.log("Written " + count + " files (" + Object.keys(LESSONS).length + " lessons)");
`;

const out = header + combined + footer;
const outPath = path.join(__dirname, "lessons.mjs");
fs.writeFileSync(outPath, out, utf8);

// Execute generated module
await import(pathToFileURL(outPath).href);
