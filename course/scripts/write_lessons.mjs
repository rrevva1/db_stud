import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT_DIRS = [
  path.join(ROOT, "content", "lessons"),
  path.join(ROOT, "public", "content", "lessons"),
];

function writeLesson(id, content) {
  for (const dir of OUT_DIRS) {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, `${id}.md`), content.md.trim() + "\n", "utf8");
    fs.writeFileSync(
      path.join(dir, `${id}.quiz.json`),
      JSON.stringify(content.quiz, null, 2) + "\n",
      "utf8"
    );
    fs.writeFileSync(path.join(dir, `${id}.tasks.md`), content.tasks.trim() + "\n", "utf8");
  }
}

// Load lesson definitions from Python modules via dynamic import of compiled JSON exports
const parts = ["p6", "p7", "p8", "p9"];
const LESSONS = {};
for (const p of parts) {
  const data = JSON.parse(
    fs.readFileSync(path.join(__dirname, "data", `${p}.json`), "utf8")
  );
  Object.assign(LESSONS, data);
}

let count = 0;
for (const [id, content] of Object.entries(LESSONS)) {
  writeLesson(id, content);
  count += 3;
}
console.log(`Written ${count} files (${Object.keys(LESSONS).length} lessons)`);
