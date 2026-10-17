# Bhakti — a family songbook
Static, mobile-friendly shlokas and bhajans. No server, login, analytics, external fonts or build dependencies.

## Build and validate
```
python3 build.py
python3 tests/validate_content.py
python3 -m http.server 8769 --bind 127.0.0.1
```
GitHub Pages serves the committed root on `main`. `/` is the Kannada landing page; `/en/` has English controls and Roman titles. Stable entry links live at `songs/<slug>/`.

## Add a scan-based entry
1. Save the original photos to `assets/`.
2. Add an entry to `data/songs.json`: unique stable `slug`, Kannada `title`, `category`, `language`, `description`, `note`, `script`, `verses` (arrays of lines), optional `chorus`, and `scans` (image filenames). The older singular `scan` field is also supported.
3. Supply `title_en`, `category_en`, `language_en`, `description_en` for the English landing page. This metadata does not transliterate the prayer itself.
4. Review text against originals and actual published texts; add `references` with `label`/`url`. Record uncertain readings, edition differences and externally completed portions in the public note.
5. Build, inspect on a phone, validate and commit/push.

## Add a multiscript entry
Metadata references a `versions_file` relative to `data/`, such as `texts/lalitha-sahasranama.json`. That file holds Kannada/Devanagari/Roman `versions` with localized titles, chapter IDs/titles, complete source `paragraphs`, source references and a source SHA-256. The builder creates the root Kannada page, `/devanagari/` and `/roman/` for each work.

`scripts/import_multiscript.py <extract-directory>` reproduces the five current imports from reviewed full source extracts. It is intentionally not an indiscriminate scraper. The source IDs and script filenames are specified in the importer. Do not import truncated previews. Preserve content/verse sequence; do not mix editions silently. `TEXT-REVIEW.md` records source boundaries and editorial choices.

The script selector uses real links and works without JavaScript. JavaScript remembers the chosen script in that browser's `localStorage` (`bhakti-script`) and uses it for subsequent supported entries. Root Kannada remains the default in a fresh browser. Storage denial does not break navigation.

## Manual checks
- Test 320px phone and desktop layouts, particularly long Kannada/Devanagari words.
- Search both Kannada and Roman titles and a nonexistent term.
- Switch all three scripts, return to the collection and open another supported work.
- Verify independent browsers retain independent choices; test without JavaScript too.
- Test text size, share/copy fallback and print preview. Check source links and scans.

Texts are a sourced devotional collection, not a critical edition. Notes identify editions, supplements and simplified accent notation where applicable. No license or authorship is claimed over traditional texts or family scans.
