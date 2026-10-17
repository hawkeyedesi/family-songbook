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
