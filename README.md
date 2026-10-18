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

`scripts/import_additional.py <extract-directory>` reproduces the four follow-up imports (Lakshmi Ashtottara upgrade, Kalabhairava Ashtakam, Hanuman Chalisa and Mahalakshmi Ashtakam). Namavali chapters use `layout: "names"`. An upgraded scan-based entry can set `preserve_original_transcription: true` to retain its original Kannada rows and source photos below the three-script reading edition. Hanuman Chalisa's Devanagari view is tagged Awadhi, not mislabeled as Sanskrit.

## Expand a checked family reading without changing editions
`scripts/expand_family_scripts.py` renders the seven original Sanskrit readings into Devanagari and IAST while retaining the exact family Kannada edition. It requires the import-only pinned package in `requirements-import.txt`; regular `build.py` remains standard-library only. The importer performs reverse-transliteration checks and records provenance. Regional Kannada lateral-letter normalization for classical Sanskrit is explicit; the original Kannada is never overwritten. Chapter `layout: "verses"` preserves the original verse/selected-mantra units and supports a `number_start` offset.

## Reading collections
Set an entry's `collections` list in `data/songs.json`, then rebuild. Supported values: `daily`, `weekly`, `friday`, `paduka-puja-bhajans`. Multiple memberships are allowed without duplicating the work; Karavalamba belongs to both Weekly and Friday. Optional `collection_order` maps each membership to its position in that list. Unassigned entries default to Daily. Paduka Puja Bhajans is the separate Sringeri bhajan collection, not a regular chanting schedule; it currently contains Amma Baaramma. Import refreshes preserve assigned memberships.

Category pages use real static routes (`/daily/`, `/weekly/`, `/friday/`, `/paduka-puja-bhajans/` and the same under `/en/`) and work without JavaScript. All keeps the flat view. Reading URLs remain unchanged when an entry is moved between collections. Language switching preserves the selected collection.

The Safari groups could not be enumerated, but Kashyap subsequently supplied the Weekly URLs and Friday list explicitly. Those confirmed lists now drive membership and order: 12 distinct Friday entries, 4 Weekly entries, 7 otherwise Daily entries, plus Amma Baaramma in Paduka Puja Bhajans (23 unique works, with Karavalamba in both schedules). Mahishasura Mardini and Aigiri Nandini are one entry; Bhagyaada Lakshmi Baaramma and Amma Baaramma are distinct. Amma Baaramma is in Paduka Puja Bhajans; further Sringeri bhajans can be added there.

## Festival tags

`tags: ["navaratri"]` is independent of an entry's reading schedules. The Kannada and Roman landing pages expose a Navaratri filter (`/navaratri/`, `/en/navaratri/`); reading pages link back to the tag. Lalitha Sahasra Namavali retains Weekly membership while also appearing under Navaratri.

## Vedic accents

Vedic entries have explicit `vedic` and `svara_status` metadata. Sri Sukta and Durga Sukta now use the published, accent-marked Stotra Nidhi three-script edition, with Dad's original transcription/scans preserved separately. Ganapati Atharvashirsha, Rudram/Chamakam and Mantra Pushpam retain their existing marked Vignanam sources. Each view has an expandable printing/pronunciation key; Roman vowel diacritics are not confused with pitch marks.

Devanagari uses a bundled Noto Serif Devanagari font because the system fallback missed the Vedic double-svarita glyph. Its OFL license is in `assets/fonts/`; no remote font service or tracking is used.

Run `python3 scripts/import_vedic.py /path/to/reviewed-extracts` **after** any import that refreshes these texts. It stores mark counts and a mark-sequence hash per script. Validation checks exact source-mark preservation through generated HTML, stable counts and normalized cross-script pitch sequences; it does not invent marks or claim a critical recension. Rudram's source-specific nasal expansion is an explicit, bounded exception, not silently normalized.

**Remaining limitation:** the seven selected daily-puja passages have an accent-marked original photo but not a completely accent-verified digital edition. All three digital views clearly say so and prominently link the original marked scan for svara chanting. Do not remove that status or mark the plain transcription verified without checking every mark against a reliable source. This is separate from ordinary non-Vedic stotras, which should not have Vedic accents mechanically added.

## Navaratri family recording

`data/navaratri-recording.json` holds the original YouTube ID, separate chanter/recorder credits, and half-open time cues `[start,end)` in seconds. `navaratri.py` renders a static full-text fallback; `assets/navaratri.js` progressively adds the YouTube IFrame player, source-backed script switching, seek buttons and section following. YouTube loads only after an explicit click. No audio is rehosted and there is no backend. A missing text match is displayed explicitly, never silently filled with a different prayer. Timing is section-level, not phoneme alignment. The recording is a family archive, not generated audio.

There are two separate Lalitha 108-name editions: `lalitha-ashtottara-bhurupa` matches the distinctive names in the family recording; `lalitha-ashtottara-shatanamavali` is the separately requested Rajatachala edition. Neither is a substitute for the 1,000-name Namavali. These festival-only entries have `collections: []` and `tags: ["navaratri"]`. Source extract hashes and transliteration provenance are retained; automatic audio transcripts are identification aids only, never public prayer text.

Browser integration checks (with a server on 8769 and Playwright installed):
```
node tests/recording-browser.cjs
```
`PLAYWRIGHT_MODULE` may point to an existing local Playwright installation. The simulated player verifies interface/seek behavior; it does not prove real YouTube playback. Check the actual embed separately.

The Navaratri page now sequences the Ganapathy prelude from35:06 in `tw9uOA5d7-A`, then the41:15Lalitha recording. `preludes` in the recording config are ordered before the main source; YouTube's ended event advances to the next part. The initial Start button begins at the specified Ganapathy offset. Section buttons, manual text selection and script changes do not require an account.

Current collection:26unique works,76reading pages. The3festival-only additions are the2distinct108-name editions and19bounded ritual excerpts (`navaratri-puja-passages`). The excerpts preserve227source Vedic marks in matching cross-script order. Unmatched family-specific passages are intentionally labelled; this is not advertised as a complete word-for-word transcript. See `TEXT-REVIEW.md` for the exact scope and remaining limitation.
