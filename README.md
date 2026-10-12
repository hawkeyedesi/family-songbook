# Bhakti — a family songbook
A mobile-friendly, static collection of shlokas and bhajans. No server, login, analytics, external fonts, or build dependencies.

## Add an entry
1. Add the original photo to `assets/`.
2. Add an object to `data/songs.json` with a unique slug, title, category (`Bhajan` or `Shloka`), language, description, scan filename, source note, optional chorus, and verses (arrays of lines).
3. Run `python3 build.py` and review the generated pages against the scan.
4. Commit and push to `main`. GitHub Pages serves the root directory.

Each entry lives at `songs/<slug>/`. Keep slugs stable so family bookmarks continue working. Generated HTML is committed so hosting needs no build tools.

## Checks
- Open the home page and a song at mobile width; check text sizing and horizontal overflow.
- Search for a title, language, and a nonexistent term.
- Test larger/smaller text, persistence, share fallback, and print preview.
- Open/download the original scan and compare every verse before correcting lyrics.

The lyrics are a transcription of the supplied scan, not an independently verified edition. No license or authorship is claimed over the devotional text or source image.
