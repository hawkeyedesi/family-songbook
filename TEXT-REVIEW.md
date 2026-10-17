# Kannada text review — 2026-10-16

Scope: eight additions from the saved family scans; existing Amma Baaramma keeps its original Roman-script source text. All new prayer text uses Kannada script. Most of the new works are Sanskrit, so metadata distinguishes language from script.

## Review passes
1. Visually identified all 16 new scan files and the text boundaries. Did not trust the noisy OCR output.
2. Compared verse order, openings, endings, names and ambiguous readings against the scans and actual fetched Kannada pages. Search summaries were discovery leads only; a generated 108-name search answer was rejected because it contained fabricated repetitions.
3. Checked generated page counts, script, source linkage, mobile rendering and interaction. This is a careful editorial comparison, not a scholarly critical edition or a guarantee that every traditional variant is resolved.

## Source decisions
- Aditya Hridayam: 31 verses, scanned book pp. 16–19. The image named `surya-pushpanjali-p18.jpg` actually continues Aditya Hridayam; it is grouped accordingly. Vaidika Vignanam used for comparison where margins are cut.
- Lakshmi Nrisimha Karavalamba: 17-verse edition, not a different expanded edition. Closing verses are on the left side of the Krishna photo. Keep the book's `ಪತತೋ ದಯಾಳೋ` at verse 8; Vaidika Vignanam lists it as an alternate.
- Durga Suktam: seven main verses, Gayatri and Shanti. Photos are from Vaidika Vignanam itself. Readable text omits Vedic accent notation; originals retain it.
- Sri Suktam: 15 principal verses, the book's Lakshmi Gayatri and closing prayer. Preserve the book's Surya/Chandra order/readings at 13–14 rather than silently replacing them with a different edition. The separate Purusha Sukta and ritual directions below are available in the scan, not mislabeled as Sri Sukta verses. Accent notation is available in the scan.
- Krishna Ashtakam: Shankaracharya's `ಶ್ರಿಯಾಶ್ಲಿಷ್ಟೋ ವಿಷ್ಣುಃ`, not `ವಸುದೇವಸುತಂ ದೇವಂ`. Only verses 1–2 are in the photo; verses 3–8 are explicitly sourced from the matching Stotra Nidhi Kannada page.
- Surya Kavacham: Yajnavalkya's seven-verse version, not Vaidika Vignanam's longer Vajrapanjara version. Matched with Stotra Nidhi.
- Lakshmi Ashtottara: the scan filename mentioning Nrisimha is misleading. It is Lakshmi's names, continued on `namavali-sheet-a.jpg`. Exactly 108 names; compared with Stotra Nidhi and Sanatan Veda. Do not copy the latter's obvious `ವಿಕೃತ್ರೈ` / `ನಿತ್ಯಪುಷ್ಪಾಯೈ` errors. Book variants at names 28–29 are called out on the page.
- Daily puja page: seven mantra sections in scan order, including unmarked portions; not seven verses of one work. Compare Kubera/Vishnu portions with Mantra Pushpam and Ganapati portion with the published Ganapati prayer. Original Vedic accent marks remain in the photo.

The public pages link their comparison sources and preserve every original image. No new Roman transliteration was created.

# Multiscript additions — 2026-10-16

Five additional works imported from complete Vaidika Vignanam extracts in Kannada, Devanagari and Roman (IAST-style) script. “English” means pronunciation transliteration, not translated meaning, as explicitly clarified by Kashyap. Kannada remains the default root landing page; `/en/` has English controls and Roman titles for every entry. Existing nine prayer texts were not transliterated or changed.

- Lalitha Sahasranama: nyasa, four dhyana verses, puja and the 183 numbered main verses; same source edition in all three scripts. Compared principal section boundaries and ending with Stotra Nidhi's Kannada edition (183 main verses).
- Vishnu Sahasranama: opening prayers/dhyana, main sequence 1–108 (107 is the end of the name hymn, 108 the Vanamali protection verse), and closing prayers/phalashruti. Source number sequences match across scripts. Source verses 6 (opening/dhyana) and 62 (main) use a single danda before the number rather than a double danda; the parser recognizes both without altering the source text. Compared the main hymn and boundaries with Stotra Nidhi; closing-section numbering differs by edition, so editions were not blended.
- Sri Rudram: both Namakam and Chamakam, 11 anuvakas each, plus the source's closing prayers. Each has its own chapter jump link. Namakam also checked against Stotra Nidhi. Source-provided Vedic accents remain intact in all scripts; this is not an audio/pronunciation verification.
- Ganesha Atharvashirsham: all 14 numbered sections and opening/closing peace invocations; compared numbering/termini with Stotra Nidhi (14).
- Soundarya Lahari: main verses 1–100, split at 41/42 (Ananda/Soundarya), plus a visibly separate closing/supplementary section containing 101–103. Stotra Nidhi supplies the conventional 100 principal verses; its absence of the three extras is not treated as an omission in either edition.

Long English/Roman `web_fetch` responses were presentation-truncated. The complete tool-provided spill files were read, so the imported versions include their actual endings. A normalized text comparison at import and SHA-256 verification in `tests/validate_content.py` ensure no source paragraphs were lost, invented, translated, or silently rewritten. Script numbering equality alone is not treated as proof of phonetic perfection.

Reading pages are generated as real static links (Kannada root, `/devanagari/`, `/roman/`). They work without JavaScript. `bhakti-script` is a local browser preference used only to choose subsequent multilingual card destinations. Preferences are not sent to a server or shared between browsers. Original source URLs are linked from each script page; comparison editions are labeled separately.

Local browser checks: 2 landing pages + 24 reading pages, all tested at 320/390/1280px. Tested bilingual search/empty results, script navigation, per-browser preference isolation, Roman/Devanagari content, text sizing/persistence, locale-correct share fallback, print controls, and navigation with JavaScript disabled.

# Four further three-script updates — 2026-10-16

- Lakshmi Ashtottara upgrades the existing entry (no duplicate card or broken bookmark). The three reading scripts use Stotra Nidhi's matching 108-name list. It differs from the family's transcription at some names; the public note makes the edition difference explicit. All 108 original Kannada rows remain in `verses` and are available in a labeled disclosure, along with both original scans. Published alternate names remain bracketed as in the source. Source-only running counts at 9/18/etc. are suppressed cosmetically because the name rows receive continuous UI numbering; stored paragraphs/source hashes are unchanged.
- Kalabhairava Ashtakam: eight main verses, followed by unnumbered phalashruti and colophon. Compared with the Stotra Nidhi version, which numbers the phalashruti as verse 9; source editions are kept separate, not combined.
- Hanuman Chalisa: all 40 chaupais, opening and closing dohas, with the primary source's additional Sanskrit dhyana prayers in a separate labeled section. Source is Awadhi, so its Devanagari selector is labeled `देवनागरी`, not falsely called a Sanskrit translation; Devanagari view is tagged `lang="awa"`. Kannada and Roman are script renderings of the same original words. Compared with Stotra Nidhi's 40-verse text.
- `Namaste Astu Mahamaye` is identified as Mahalakshmi Ashtakam: eight main verses plus three unnumbered phalashruti stanzas and colophon. Stotra Nidhi numbers these concluding stanzas 9–11. Both the familiar opening and the formal work title are searchable.

The three newly added works use matching Vaidika Vignanam Kannada/Devanagari/Roman editions with source variants retained, and Stotra Nidhi comparison links. Lakshmi uses Stotra Nidhi's actual three-script lists, not Vaidika Vignanam's differently divided name list. No Roman pronunciation text was fabricated from a search summary. Completeness and source-preservation tests cover all four updates.

Local browser verification: all 37 routes (2 landing pages +35 reading pages) at 320/390/1280px; all four new/updated script selectors, 108 main names and 108 preserved family names, both Lakshmi scans, 40 Chalisa verses, opening-name search, independent script preferences and non-JavaScript navigation.

# Earlier scan-entry coverage correction — 2026-10-16

Audit found seven remaining Kannada-only Sanskrit entries: Aditya Hridayam, Karavalamba, Durga Suktam, Sri Suktam, Shankaracharya Krishna Ashtakam, Yajnavalkya Surya Kavacham and daily puja mantras. All now use the same three-view model. Lakshmi Ashtottara was already upgraded and was rechecked, not duplicated.

For these family readings, Devanagari and Roman are deterministically rendered from the already checked Kannada paragraphs using `indic-transliteration==2.3.82`, not assembled from a potentially different edition. The Kannada rows, wording, sequence, book-specific variants and all original scans are preserved. Each rendered paragraph was converted back to Kannada and compared, allowing only equivalent danda/pipe punctuation. Aditya and Karavalamba's regional Kannada `ಳ` spellings correspond to classical Sanskrit `ल/l` in their published Devanagari comparison texts; that explicit normalization is applied to the rendering input, not to the original Kannada. Derivation, original hash, tool version and round-trip result are recorded per view.

Published Devanagari comparison pages were retrieved for all six named standalone works, including the correct Surya Kavacham and the `ಶ್ರಿಯಾಶ್ಲಿಷ್ಟೋ` Krishna Ashtakam. Daily puja stays the exact seven selected mantra units; it is not replaced by a different generic manual, and missing Vedic accents are not guessed. Chapter jumps use the opening words of each selected mantra.

Current coverage: sixteen Sanskrit/Awadhi works with Kannada/Devanagari/Roman views; Amma Baaramma retains the original Roman-script Kannada bhajan from its photograph. Coverage validation now fails if any other entry lacks a version bundle. Original nine transcription fields remain unchanged. Browser checks cover all 51 routes and original scan URLs in every newly added script view.

# Collection navigation — 2026-10-16

Added schedule collections Daily, Weekly and Friday, with All as the flat view. Current17 entries provisionally assigned Daily as requested for otherwise unclassified items. No Friday/Weekly membership was guessed from shloka names. Both supplied iCloud Safari share links returned Apple's Safari-only notice rather than their tab lists. Native Safari access did not produce a usable group listing. Actual page URLs, labeled by group, have been requested; import remains pending.

Category moves do not change reading URLs. Category views exist in Kannada and English; language switching preserves the group, search works within the group, and real links work without JavaScript. Browser checks cover all8 landing/category routes at320/390/1280px, entry counts, empty categories and deep script-reading links.

# Confirmed Weekly / Friday lists and bhajan collection — 2026-10-16

Supersedes the provisional grouping above. Kashyap confirmed the supplied four unique URLs as Weekly, then supplied thirteen Friday labels; Mahishasura Mardini and Aigiri Nandini refer to one hymn. Friday therefore contains twelve distinct works, in the requested order. Karavalamba appears in both Weekly and Friday without duplicating its page. Eight other entries remain Daily. Paduka Puja Bhajans is a separate, initially empty Sringeri collection, not a regular chanting schedule.

Six new works imported in all three scripts:

- Ya Devi Sarva Bhuteshu: Vaidika Vignanam's Devi Aparajita Stotram, all 28 numbered verses; compared with the actual Stotra Nidhi Devanagari page.
- Sharada Bhujanga Prayata Ashtakam: all 8 verses and colophon; compared with Sanskrit Documents' actual HTML. Verses 3 and 5 have variants (`patra/pratna`, `sarga/sanga`); reading consistently retains the Vignanam edition.
- Mahishasura Mardini / Aigiri Nandini: one entry, all 21 numbered verses, matching sequences in Vignanam's three script versions.
- Bhagyada Lakshmi Baramma: pallavi and five charanams, not Amma Baaramma. Compared with Bhakti Nidhi's Kannada text; musical/word variants retained, not blended. Source music metadata omitted from the chanting text. This is a Kannada composition by Purandara Dasa; Devanagari is explicitly labelled as script, not a Sanskrit translation.
- Mantra Pushpam: complete Vignanam three-script text, including opening peace prayer and closing mantras. Stotra Nidhi's actual Kannada page has a more expanded puja compilation (Narayana Sukta and more Gayatris); these extras are not silently combined.
- Lalitha Sahasra Namavali: genuinely distinct from the existing metrical Sahasranama. Family-shared temple PDF confirmed as a 35-page namavali; its legacy-font extraction is unreliable. Vignanam's extract has malformed/split name rows, so the matched Stotra Nidhi three-script edition is used instead: exactly 1,000 names in each script, every printed decade marker checked against list position. Temple PDF is linked for comparison; it is not falsely presented as a verbatim transcription.

The other two shared PDFs were downloaded and inspected: `lalita.pdf` is the existing Sahasranama stotram, and `saundaryalahari.pdf` is the existing Soundarya Lahari. Linked as comparison editions without copying their annotated PDF editions or creating duplicate pages.

Important Karavalamba correction: the shared Stotra Nidhi edition has 25 verses, not the family scan's 17. The reading now includes all 25 in each of its published three scripts. Pipe punctuation alone is normalized to danda marks. The original family Kannada transcription and scans remain separately visible below; original `verses` data is unchanged. The family transliteration refresh skips entries explicitly marked with a published edition.

Coverage is now 23 unique entries, 67 reading pages, and 10 landing/category pages. Original nine transcription fields are still unchanged. Imports validate complete verse sequences (28 / 8 / 21 / 25), all five bhajan charanams, 1,000 names, source hashes, schedule overlaps and Friday order. This is a sourced family reading collection, not a critical edition or a claim of independent philological proofreading of every syllable.

# Vedic svara correction — 2026-10-16

User explicitly flagged missing accents as a correctness problem. Audit found that the family-derived Sri Sukta, Durga Sukta and seven daily-mantra digital transcriptions lacked svara entirely; prior plain transliteration preserved letters, not chant notation. Ganapati Atharvashirsha, Rudram/Chamakam and Mantra Pushpam already had source accents. This supersedes earlier claims that plain renderings were sufficient for Vedic chanting.

Sri and Durga Sukta now follow Stotra Nidhi's actual marked Kannada/Devanagari/Roman pages. Sri retains all 15 numbered principal richas, followed separately by Lakshmi Gayatri and Shanti; Durga retains all 7 main mantras, Durga Gayatri and Shanti. Original family texts and scans stay in their disclosure. Extra poetic Sri Sukta stotras from the source compilation are not mixed into the Vedic reading; one source Roman/Indian-script mark discrepancy occurred there, outside the selected reading. The final selected pitch-mark sequences match in all three scripts: Sri279, Durga156.

Retained Vignanam source mark totals: Ganapati391/391/391; Rudram2317/2318/2318; Mantra Pushpam403/403/403 (Kannada/Devanagari/Roman). Rudram Namakam9 prints `ಗ್ಂ` with a different nasal expansion from Devanagari `ग्॒म्॒`; one additional low mark in Devanagari/Roman belongs to that expansion. Each source is preserved, not mechanically repaired. Tests lock this exact bounded exception and otherwise compare normalized pitch sequences.

Roman source styles differ: Vignanam uses U+0320 below for anudatta; Stotra Nidhi uses U+0331. Both are retained; above-line U+030D and double U+030E are pitch notation, distinct from macrons/dots of IAST vowel/consonant transliteration. The visible key explains low/falling/long-double signs, the unmarked-syllable caveat, long vowels, retroflex/sibilant distinctions, anusvara/visarga (including source colon spelling), and source/tradition-dependent timing. No Unicode normalization or generated accent reconstruction is applied.

**Still unverified digitally:** daily-puja selections. The p65 photo visibly contains the original accents and is now prominently linked above the reading in every script. Plain digital text is explicitly labelled not accent-verified. Actual published sources were found for some component mantras, but not a verified matching seven-passage set; no accents from generated search answers were accepted. Complete digital svara verification remains pending; the original photo is the chant reference in the meantime.

Verification: source-mark counts + sequence hashes, exact preservation into generated HTML and browser DOM, all18 Vedic reading views at320/390/1280px, expandable notation key without JS, script navigation, and successful access to the original scan. These checks prove preservation/rendering of the selected published readings, not independent Vedic recitation expertise.

Visual inspection also exposed a real font fallback issue: macOS Kohinoor Devanagari did not render U+1CDA in the notation key. Bundled Google Fonts' Noto Serif Devanagari (OFL license included; no remote font dependency), confirmed its cmap contains U+0951/U+0952/U+1CDA and visually rechecked the long/double-svarita sign. Script-specific examples avoid unsupported mixed-script font fallback in the key. Font source: https://github.com/google/fonts/tree/main/ofl/notoserifdevanagari .
