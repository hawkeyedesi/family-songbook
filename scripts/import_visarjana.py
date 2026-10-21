"""Import the family visarjana page with independently sourced Vedic accents.

Run with the pinned import-only indic-transliteration environment.
The photo crop excludes the phone's unrelated family-photo thumbnails.
"""
from pathlib import Path
import hashlib, json, re
from indic_transliteration import sanscript as sc
from indic_transliteration.sanscript import transliterate as tr

ROOT = Path(__file__).resolve().parents[1]
slug = 'visarjana-mantra'
sources = json.loads((ROOT/'data/visarjana-sources/vedic-excerpts.json').read_text())
vedic = []
for source in sources:
    raw = source['itx']
    assert hashlib.sha256(raw.encode()).hexdigest() == source['sha256']
    raw = re.sub(r'\s+\d+\\\.\d+\\\.\d+\s*$', '', raw)
    vedic.append(tr(raw, sc.ITRANS, sc.DEVANAGARI))
assert vedic[0].startswith('उत्ति॑ष्ठ ब्रह्मणस्पते')
assert 'अ॒भ्यार॒मिदद्र॑यो॒' in vedic[1]
vedic[0] = 'ॐ ' + vedic[0]  # Family-book invocation; no pitch mark is inferred.
closing = 'पूजावसाने गच्छत्वं पुनरागमनाय च ॥'
family = [
    ['ಓಂ ಉತ್ತಿಷ್ಠ ಬ್ರಹ್ಮಣಸ್ಪತೇ ದೇವಯಂತಸ್ತ್ವೇಮಹೇ ।',
     'ಉಪಪ್ರಯಂತು ಮರುತಃ ಸುದಾನವ ಇಂದ್ರಪ್ರಾಶೂರ್ಭವಾಸಚಾ ।'],
    ['ಅಭ್ಯಾರಮಿದ ದ್ಯೋ ನಿಷಿಕ್ತಂ ಪುಷ್ಕರೇ ಮಧು । ಅವತಸ್ಯ ವಿಸರ್ಜನೇ ।'],
    ['ಪೂಜಾವಸಾನೇ ಗಚ್ಛತ್ವಂ ಪುನರಾಗಮನಾಯಚ ॥'],
]
instructions = 'ಈ ಮಂತ್ರವನ್ನು ಹೇಳಿ ಕಲಶ-ಪ್ರತಿಮೆಯನ್ನು ಬಲಭಾಗಕ್ಕೆ ಸ್ವಲ್ಪ ಕದಲಿಸಿ, ಹೂಗಳನ್ನು ಪಕ್ಕಕ್ಕೆ ತೆಗೆದಿರಿಸಬೇಕು. ಇದೇ ಉದ್ವಾಸನಾಕ್ರಮ.'
note_en = ('Added from the family-book page (xviii). The two Vedic passages are Rigveda 1.40.1 and 8.72.11; their text and pitch marks come from the cited Sanskrit Documents edition, not from guesses about the unaccented photo. The photo appears to print “ಅಭ್ಯಾರಮಿದ ದ್ಯೋ”; the reading above follows the published “अभ्यारमिदद्रयो”. Printed spacing is normalized in the reading edition. The closing “Pūjāvasāne gacchatvaṃ punarāgamanāya ca” is retained from the family book without invented accents. The original Kannada transcription and cropped page remain below. The book instructs: after this mantra, gently move the kalasha/image slightly to the right and set the flowers aside; it calls this the udvāsana procedure. This is not yet checked against a Sringeri edition. It is a separate closing reading, not a newly timed cue in the 1983 recording.')
note_kn = ('ಕುಟುಂಬದ ಪುಸ್ತಕದ (xviii) ಪುಟದಿಂದ ಸೇರಿಸಲಾಗಿದೆ. ಮೊದಲ ಎರಡು ವೈದಿಕ ಮಂತ್ರಗಳ ಪಾಠ ಮತ್ತು ಸ್ವರಗುರುತುಗಳನ್ನು ಋಗ್ವೇದ ೧.೪೦.೧ ಹಾಗೂ ೮.೭೨.೧೧ರ ಉಲ್ಲೇಖಿತ ಪ್ರಕಟಿತ ಮೂಲದಿಂದ ತೆಗೆದುಕೊಳ್ಳಲಾಗಿದೆ; ಚಿತ್ರದಿಂದ ಊಹಿಸಿ ಸೇರಿಸಿಲ್ಲ. ಚಿತ್ರದಲ್ಲಿ “ಅಭ್ಯಾರಮಿದ ದ್ಯೋ” ಎಂದು ಕಾಣುತ್ತದೆ; ಮುಖ್ಯ ಪಾಠದಲ್ಲಿ ಪ್ರಕಟಿತ “ಅಭ್ಯಾರಮಿದದ್ರಯೋ” ರೂಪವನ್ನು ಬಳಸಲಾಗಿದೆ. ಪಠಣದ ಆವೃತ್ತಿಯಲ್ಲಿ ಪದಗಳ ಅಂತರವನ್ನು ಸರಿಪಡಿಸಲಾಗಿದೆ. “ಪೂಜಾವಸಾನೇ…” ಎಂಬ ಕೊನೆಯ ಸಾಲು ಕುಟುಂಬದ ಪುಸ್ತಕದಿಂದ ಬಂದಿದೆ. ಮೂಲ ಕನ್ನಡ ಪಾಠ ಮತ್ತು ಪುಟವನ್ನು ಕೆಳಗೆ ಉಳಿಸಲಾಗಿದೆ. '+instructions+' ಶೃಂಗೇರಿ ಆವೃತ್ತಿಯೊಡನೆ ಇನ್ನೂ ಪರಿಶೀಲಿಸಿಲ್ಲ. ಇದು ಪ್ರತ್ಯೇಕ ಸಮಾಪ್ತಿಯ ಪಠ್ಯ; ೧೯೮೩ರ ಧ್ವನಿಮುದ್ರಣಕ್ಕೆ ಹೊಸ ಕಾಲಸೂಚಿ ಸೇರಿಸಿಲ್ಲ.')
versions = []
for i, (vid, scheme) in enumerate([('kannada',sc.KANNADA), ('devanagari',sc.DEVANAGARI), ('roman',sc.IAST)]):
    def convert(text):
        if vid == 'devanagari': return text
        # Convert each accent-delimited span, preserving the original mark order.
        # IAST's library mapping otherwise inserts a dotted-circle placeholder.
        parts = re.split('([॒॑᳚])',text)
        out = ''.join(p if p in ['॑','॒','᳚'] else tr(p,sc.DEVANAGARI,scheme) for p in parts)
        if vid == 'roman': out = out.translate(str.maketrans({'॑':'\u030d','॒':'\u0331','᳚':'\u030e'})).replace('||','॥').replace('|','।')
        return out
    chapters = [dict(id='vedic',title=['ವೈದಿಕ ಮಂತ್ರಗಳು','वैदिकमन्त्रौ','Vedic mantras'][i],paragraphs=[convert(x) for x in vedic],layout='verses'),dict(id='closing',title=['ಸಮಾಪ್ತಿ — ಕುಟುಂಬದ ಪುಸ್ತಕ','समापनम् — पारिवारिकपुस्तकात्','Closing — family book'][i],paragraphs=[convert(closing)],layout='verses',number_start=3)]
    text = '\n\n'.join(p for ch in chapters for p in ch['paragraphs'])
    marks = ''.join(c for c in text if c in '॒॑᳚\u030d\u0331\u030e')
    versions.append(dict(id=vid,label=['ಕನ್ನಡ','संस्कृतम्','English (Roman)'][i],lang=['kn','sa','en'][i],title=['ವಿಸರ್ಜನ ಮಂತ್ರ — ಉದ್ವಾಸನೆ','विसर्जनमन्त्रः — उद्वासनम्','Visarjana Mantra — Udvasana'][i],chapters=chapters,references=[dict(label=x['reference']+' — accent-marked source',url=x['url']) for x in sources],source_sha256=hashlib.sha256(text.encode()).hexdigest(),svara_profile=dict(counts={f'U+{ord(c):04X}':marks.count(c) for c in sorted(set(marks))},sequence_sha256=hashlib.sha256(marks.encode()).hexdigest())))
(ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
songs = json.loads((ROOT/'data/songs.json').read_text())
songs = [s for s in songs if s['slug'] != slug]
songs.append(dict(slug=slug,title='ವಿಸರ್ಜನ ಮಂತ್ರ — ಉದ್ವಾಸನೆ',title_en='Visarjana Mantra — Udvasana',category='ಪೂಜಾ ಮಂತ್ರ',category_en='Puja mantra',language='ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Sanskrit · Roman',description='ಪೂಜೆಯ ಸಮಾಪ್ತಿಯಲ್ಲಿ ಹೇಳುವ ವಿಸರ್ಜನ ಮಂತ್ರಗಳು — ಕುಟುಂಬದ ಪುಸ್ತಕದ ಪುಟದೊಂದಿಗೆ.',description_en='Closing prayers for visarjana / udvasana, with the family-book page.',script='kannada',versions_file=f'texts/{slug}.json',verses=family,scans=['visarjana-family-p18.jpg'],note=note_kn,note_en=note_en,preserve_original_transcription=True,collections=[],tags=['navaratri'],collection_order={'navaratri':9999},search_aliases=['Visarjan','Visarjana','Udvasana','Uttishtha Brahmanaspate','ವಿಸರ್ಜನೆ','ಉದ್ವಾಸನೆ'],vedic=True,svara_status='marked',published_edition='rigveda-excerpts-family-closing'))
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')
audit_path = ROOT/'data/sringeri-audit.json'
audit = json.loads(audit_path.read_text())
audit['works'] = [r for r in audit['works'] if r['slug'] != slug]
audit['works'].append(dict(slug=slug,title='Visarjana Mantra — Udvasana',status='not-checked',added='2026-10-21',note='Added after the 2026-10-19 catalog audit. Family ritual sequence with Rigveda-sourced accents for the two Vedic passages; no Sringeri comparison claimed.',source_url='https://www.sringeri.net/stotras',current_text_hashes={v['id']:v['source_sha256'] for v in versions}))
audit_path.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print('Imported visarjana: two sourced Vedic passages and one family closing, in three scripts.')
