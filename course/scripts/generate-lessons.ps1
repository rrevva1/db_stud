# Generates lesson content from curriculum.json (UTF-8 safe)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$curriculumPath = Join-Path $root "content\curriculum.json"
$lessonsDir = Join-Path $root "content\lessons"
$sqlDir = Join-Path $root "sql"

New-Item -ItemType Directory -Path $lessonsDir -Force | Out-Null
New-Item -ItemType Directory -Path $sqlDir -Force | Out-Null

$json = [System.IO.File]::ReadAllText($curriculumPath, [System.Text.Encoding]::UTF8)
$curriculum = $json | ConvertFrom-Json
$utf8 = New-Object System.Text.UTF8Encoding $false
$count = 0

foreach ($part in $curriculum.parts) {
  foreach ($mod in $part.modules) {
    foreach ($lesson in $mod.lessons) {
      $id = $lesson.id
      $title = $lesson.title
      $dialect = $lesson.dialect
      $objLines = ($lesson.objectives | ForEach-Object { "- $_" }) -join "`n"
      $srcLines = ($lesson.requiredSources | ForEach-Object { "- **$($_.sourceId)**: $($_.ref)" }) -join "`n"

      $dialectNote = switch ($dialect) {
        "sql" { "Praktika: **PostgreSQL** (psql ili pgAdmin)." }
        "lab" { "Laboratornaya. Sreda: **PostgreSQL**." }
        "theory" { "Fokus na teorii i teste; SQL ne obyazatelen." }
        "exam" { "Itogovyy test chasti." }
        default { "Sm. blok praktiki." }
      }

      $md = @"
## $title

**Chast:** $($part.title) · **Modul:** $($mod.title)

$dialectNote

### Tseli uroka

$objLines

### Kratkaya teoriya

Urok vkhodit v kurs «Bazy dannykh: ot proektirovaniya do SQL». Eto szhatyy pereskaz; podrobnosti — v PDF-istochnikakh (papka db_stud).

Posledovatelnost: etot tekst → glavy iz istochnikov → test → praktika.

### Chto chitat v istochnikakh

$srcLines

### Klyuchevye ponyatiya

- Zakrepite terminologiyu iz tseley uroka.
- Vypishite opredeleniya svoimi slovami.
- Podgotovte 2–3 voprosa po neponyatnym mestam.

Skvoznaya predmetnaya oblast: **universitet** (student, s_group, performance) i proekt **aviakompaniya**.
"@

      $obj0 = if ($lesson.objectives.Count -gt 0) { $lesson.objectives[0] } else { $title }
      $src0 = if ($lesson.requiredSources.Count -gt 0) { "$($lesson.requiredSources[0].sourceId): $($lesson.requiredSources[0].ref)" } else { "programma kursa" }

      $quizObj = [ordered]@{
        lessonId = $id
        passingScore = 70
        questions = @(
          [ordered]@{
            id = "q1"
            type = "single"
            question = "Osnovnaya tsel uroka?"
            options = @($obj0, "Tolko sintaksis bez teorii", "Propustit praktiku", "Zamenit PostgreSQL na MongoDB")
            correct = @(0)
            explanation = "Pervyy variant = pervaya tsel iz programmy uroka."
          },
          [ordered]@{
            id = "q2"
            type = "single"
            question = "Gde lezhat PDF-istochniki?"
            options = @("Papka db_stud i dop", "Tolko vneshniy sayt", "Vnutri lessons kak tekst knigi", "GitHub Postgres Pro")
            correct = @(0)
            explanation = "Vse knigi lokalno v proekte db_stud."
          },
          [ordered]@{
            id = "q3"
            type = "single"
            question = "Kakoy SQL dlya praktiki yadra kursa?"
            options = @("PostgreSQL", "MySQL", "T-SQL", "MongoDB")
            correct = @(0)
            explanation = "Yadro: Morgunov + praktikum na PostgreSQL."
          },
          [ordered]@{
            id = "q4"
            type = "single"
            question = "Obyazatelnyy istochnik etogo uroka?"
            options = @($src0, "Tolko Wikipedia", "Tolko Graph DB", "Net istochnikov")
            correct = @(0)
            explanation = "Sm. blok Istochiki na stranitse uroka."
          },
          [ordered]@{
            id = "q5"
            type = "multi"
            question = "Chto vkhodit v format uroka? (vse vernye)"
            options = @("Teoriya", "Ssylki na PDF", "Test", "Praktika")
            correct = @(0, 1, 2, 3)
            explanation = "Format Stepik: teoriya, istochniki, test, praktika."
          }
        )
      }

      if ($dialect -eq "exam") {
        $tasks = @"
## Itogovaya rabota

1. Povtorite vse uroki chasti.
2. Proydite testy esli nizhe 70%.
3. Vypolnite sbornuyu zadachu po temam chasti.
4. Oformite otchet: chto izucheno, kakie zaprosy/skhemy postroeny.
"@
      } elseif ($dialect -eq "theory") {
        $tasks = @"
## Zadaniya

1. Prochitayte obyazatelnye glavy iz bloka Istochiki.
2. Vypishite 5 opredeleniy po teme uroka.
3. Narisuyte skhemu ili tablitsu (draw.io).
4. Otvet: kak tema svyazana so sleduyushchim urokom?
"@
      } elseif ($dialect -eq "lab") {
        $tasks = @"
## Laboratornaya

**Sreda:** PostgreSQL 16.

1. Vypolnite shagi iz prakticheskoy raboty v PDF Praktikum.
2. Sohranite skript: ``course/sql/$id.sql``
3. Skrinshot rezultata.
4. Kontrolnye voprosy iz praktikuma.

Eталon: ``course/sql/$id.sql`` esli est.
"@
      } else {
        $tasks = @"
## Praktika PostgreSQL

1. Podklyuchites k uchebnoy BD.
2. Zadaniya po teme: **$title**
3. Sohranite: ``course/sql/$id-solution.sql``
4. Svertes s ``course/sql/$id.sql``

### Mini-zadanie

Odin SQL-zapros ili DDL po glavnoy idee uroka. Kommentariy: chto proveryaet.

### Samoproverka

- [ ] Bez oshibok
- [ ] Rezultat ozhidaemyy
- [ ] Mozhete obyasnit kazhduyu stroku
"@
      }

      [System.IO.File]::WriteAllText((Join-Path $lessonsDir "$id.md"), $md.Trim(), $utf8)
      [System.IO.File]::WriteAllText((Join-Path $lessonsDir "$id.quiz.json"), ($quizObj | ConvertTo-Json -Depth 8), $utf8)
      [System.IO.File]::WriteAllText((Join-Path $lessonsDir "$id.tasks.md"), $tasks.Trim(), $utf8)
      $count++
    }
  }
}

Write-Host "Generated $count lessons"
