# Kamalamma Ajji archive

Six unchanged original MP3s (55:11) are hosted in assets/audio/kamalamma-ajji/.
The public manifest records SHA-256, byte length, duration and the 34-section index.
Five forwarded WhatsApp files were bit-identical to Drive originals 1–5.
Recording/upload dates have not been inferred.

There are currently twelve reading sets, not twelve fully verified verbatim
transcriptions. Each reading distinguishes its source and oral variants. Kannada
compositions in Devanagari remain Kannada, not Sanskrit translations. Ganesha
Pancharatnam uses Sringeri's own three script-specific witnesses. The main
33-work collection and its Sringeri checks remain unchanged.

Unknown/variant passages remain explicitly audio-only pending family/source
confirmation. In particular, the Shiva alphabetic bhajan's garbled transcript is
not published as lyrics. Ajji's Kannada translation of Hanuman Chalisa is not
silently replaced by the songbook's Awadhi original.

Synchronization is approximate section-level, not per-word/per-name alignment.
Cross-file continuations include Lalitha (2→3), Kaliyugadali (4→5), Kalabhairava
(5→6). Audio remains the authority for sung ordering and repetition.

Regenerate imports with indic-transliteration 2.3.82:
  /tmp/bhakti-script-venv/bin/python scripts/import_kamalamma.py
  python3 build.py

Playback tests need a local server with HTTP byte-range support (as GitHub Pages
provides). Plain Python http.server cannot reliably seek in these long MP3s.
  BHAKTI_TEST_URL=http://127.0.0.1:8770/ node tests/kamalamma-browser.cjs
