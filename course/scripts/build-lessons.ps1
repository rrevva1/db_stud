# Build lessons.mjs from Python sources and run
$ErrorActionPreference = "Stop"
$scriptDir = "e:\Projects\db_stud\course\scripts"
$node = "c:\Users\RevvaRR\AppData\Local\Programs\cursor\resources\app\resources\helpers\node.exe"
$utf8 = New-Object System.Text.UTF8Encoding $false

$p1 = [System.IO.File]::ReadAllText("$scriptDir\enhance_p6_p9.py", $utf8)
$p2 = [System.IO.File]::ReadAllText("$scriptDir\enhance_p6_p9_part2.py", $utf8)
$helpers = [System.IO.File]::ReadAllText("$scriptDir\lessons_helpers.mjs", $utf8)

$start = $p1.IndexOf('# ===== PART 6 =====')
$end = $p1.IndexOf('# Continue in part 2')
$p6block = $p1.Substring($start, $end - $start).Trim()
$p7block = $p2.Substring($p2.IndexOf('# ===== PART 7 =====')).Trim()

$combined = $helpers + "`n" + $p6block + "`n" + $p7block

# Python comments to JS
$combined = $combined -replace '(?m)^# ', '// '

# tasks triple-quoted strings -> backticks
$combined = $combined -replace '"tasks": """', 'tasks: `'
$combined = $combined -replace '(?ms)"""\s*,\s*\n\}', "`n},"

# theory strings inside md() that use """ ... """ - replace with backticks carefully
# Pattern: ,\n    """ -> , `
$combined = $combined -replace ',\s*\r?\n\s*"""', ", `"
$combined = $combined -replace '(?ms)"""\s*,\s*\r?\n\s*\[', "`, [`"
$combined = $combined -replace '(?ms)"""\s*,\s*\r?\n\s*\(', "`, ("
$combined = $combined -replace '(?ms)"""\s*\+\s*OPT', "` + OPT"
$combined = $combined -replace '(?ms)"""\s*,\s*\r?\n\s*"quiz"', "`, quiz"

# extra= in md calls
$combined = $combined -replace 'extra="\\n', 'extra="\n'

$writeLogic = @'

for (const [id, content] of Object.entries(LESSONS)) {
  for (const dir of OUT_DIRS) {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, id + ".md"), content.md.trim() + "\n", "utf8");
    fs.writeFileSync(path.join(dir, id + ".quiz.json"), JSON.stringify(content.quiz, null, 2) + "\n", "utf8");
    fs.writeFileSync(path.join(dir, id + ".tasks.md"), content.tasks.trim() + "\n", "utf8");
  }
  count += 3;
}
console.log("Written " + count + " files (" + Object.keys(LESSONS).length + " lessons)");
'@

$header = @'
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT_DIRS = [path.join(ROOT, "content", "lessons"), path.join(ROOT, "public", "content", "lessons")];
let count = 0;
'@

# Insert header after helpers constants - actually helpers don't have imports. Prepend imports.
$final = $header + "`n" + ($combined -replace '^function ', 'function ')

$outPath = "$scriptDir\lessons.mjs"
[System.IO.File]::WriteAllText($outPath, $final + "`n" + $writeLogic, $utf8)
Write-Host "Built lessons.mjs:" (Get-Item $outPath).Length "bytes"
& $node $outPath
