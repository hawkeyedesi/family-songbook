"""Reviewed family scans 2026-10-19. Import-only indic-transliteration==2.3.82."""
from pathlib import Path
import json,hashlib,unicodedata
from importlib.metadata import version
assert version('indic-transliteration')=='2.3.82'
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as tr
ROOT=Path(__file__).resolve().parents[1];songs=json.loads((ROOT/'data/songs.json').read_text());by={s['slug']:s for s in songs}
B=[]
def add(slug,title,kn,paragraphs,scans,**kw):B.append(dict(slug=slug,title=title,kn=kn,paragraphs=paragraphs,scans=scans,**kw))
add('durga-saptashloki','Durga Saptashloki','ದುರ್ಗಾ ಸಪ್ತಶ್ಲೋಕೀ',[
'ज्ञानिनामपि चेतांसि देवी भगवती हि सा ।\nबलादाकृष्य मोहाय महामाया प्रयच्छति ॥ 1 ॥',
'दुर्गे स्मृता हरसि भीतिमशेषजन्तोः\nस्वस्थैः स्मृता मतिमतीव शुभां ददासि ।\nदारिद्र्यदुःखभयहारिणि का त्वदन्या\nसर्वोपकारकरणाय सदार्द्रचित्ता ॥ 2 ॥',
'सर्वमङ्गलमाङ्गल्ये शिवे सर्वार्थसाधिके ।\nशरण्ये त्र्यम्बके गौरि नारायणि नमोऽस्तु ते ॥ 3 ॥',
'शरणागतदीनार्तपरित्राणपरायणे ।\nसर्वस्यार्तिहरे देवि नारायणि नमोऽस्तु ते ॥ 4 ॥',
'सर्वस्वरूपे सर्वेशे सर्वशक्तिसमन्विते ।\nभयेभ्यस्त्राहि नो देवि दुर्गे देवि नमोऽस्तु ते ॥ 5 ॥',
'रोगानशेषानपहंसि तुष्टा\nरुष्टा तु कामान् सकलानभीष्टान् ।\nत्वामाश्रितानां न विपन्नराणां\nत्वामाश्रिता ह्याश्रयतां प्रयान्ति ॥ 6 ॥',
'सर्वाबाधाप्रशमनं त्रैलोक्यस्याखिलेश्वरि ।\nएवमेव त्वया कार्यमस्मद्वैरिविनाशनम् ॥ 7 ॥'],[1],title_sa='दुर्गासप्तश्लोकी')
add('om-jai-jagdish-hare','Om Jai Jagdish Hare','ಓಂ ಜಯ ಜಗದೀಶ ಹರೇ',[
'ॐ जय जगदीश हरे, स्वामी जय जगदीश हरे ।\nभक्त जनों के संकट, क्षण में दूर करे ॥',
'जो ध्यावे फल पावे, दुख विनसे मन का ।\nसुख सम्पति घर आवे, कष्ट मिटे तन का ॥',
'मात पिता तुम मेरे, शरण गहूँ मैं किसके ।\nतुम बिन और न दूजा, आस करूँ जिसकी ॥',
'तुम पूरण परमात्मा, तुम अन्तर्यामी ।\nपारब्रह्म परमेश्वर, तुम सबके स्वामी ॥',
'तुम करुणा के सागर, तुम पालनकर्ता ।\nमैं मूरख खल कामी, मैं सेवक तुम स्वामी, कृपा करो भर्ता ॥',
'तुम हो एक अगोचर, सबके प्राणपति ।\nकिस विधि मिलूँ दयामय, तुमको मैं कुमति ॥',
'दीनबन्धु दुख हर्ता, तुम रक्षक मेरे ।\nअपने हाथ उठाओ, अपनी शरण लगाओ, द्वार पड़ा तेरे ॥',
'विषय विकार मिटाओ, पाप हरो देवा ।\nश्रद्धा भक्ति बढ़ाओ, सन्तन की सेवा ॥',
'तन मन धन जो कुछ है, सब ही है तेरा ।\nतेरा तुझको अर्पण, क्या लागे मेरा ॥',
'ॐ जय जगदीश हरे, स्वामी जय जगदीश हरे ।\nभक्त जनों के संकट, क्षण में दूर करे ॥'],[2],title_sa='ॐ जय जगदीश हरे',lang='hi',roman=[
'Om Jai Jagdeesh Hare, Swami Jai Jagdeesh Hare\nBhakta Janon Ke Sankat (rep.), Kshan Men Door Kare',
'Jo Dhyaaye Phal Paave, Dukh Vinashe Man Ka, Swami (rep.)\nSukh Sampati Ghar Aave (rep.), Kasht Mite Tan Ka',
'Maat Pitaa Tum Mere, Sharan Gahoon Main Kiskee, Swami (rep.)\nTum Bin Aur Na Dooja (rep.), Aas Karoon Main Jiskee',
'Tum Pooran Paramaatmaa, Tum Antaryaamee, Swami (rep.)\nPaara Brahma Parameshwar (rep.), Tum Sabke Swaami',
'Tum Karuna Ke Saagar, Tum Paalan Karta, Swami (rep.)\nMain Moorakh Khal Kaami, Main Sevak Tum Swami, Kripa Karo Bharta',
'Tum Ho Ek Agochar, Sabke Praanapati, Swami (rep.)\nKis Vidhi Miloon Dayaamaye (rep.), Tumko Main Kumati',
'Deen Bandhu Dukh Harta, Tum Rakshak Mere, Swami (rep.)\nApne Haath Uthaao, Apne Sharan Lagao, Dwaar Padaa Mein Tere',
'Vishay Vikaar Mitaao, Paap Haro Deva, Swami (rep.)\nShraddha Bhakti Badaao (rep.), Santan Ki Seva',
'Tan, Man, Dhan, Sab Kuchh Hai Tera, Swami Sab Kuchh Hai Tera\nTera Tujh Ko Arpan (rep.), Kya Lage Mera',
'Om Jai Jagdeesh Hare, Swami Jai Jagdeesh Hare\nBhakta Janon Ke Sankat (rep.), Kshan Men Door Kare'])
add('sharade-sharade','Sharade Sharade','ಶಾರದೇ ಶಾರದೇ',[
'शारदे शारदे ज्ञानदायिके ।\nशारदे शारदे शारदाम्बिके ॥',
'पार्वति भगवति भक्तिदायिके ।\nतुङ्गातीरे शृङ्गगिरि शारदाम्बिके ॥',
'भक्तिदायिके ज्ञानदायिके मोक्षदायिके ।\nशारदाम्बिके ॥'],[7],title_sa='शारदे शारदे',chorus=True)
add('dehi-dehi-sharada','Dehi Dehi Sharada','ದೇಹಿ ದೇಹಿ ಶಾರದಾ',[
'देहि देहि शारदा ।\nज्ञानं देहि सर्वदा ॥',
'प्रेमरूपिणि शारदा ।\nभक्तिं देहि सर्वदा ॥',
'योगरूपिणि शारदा ।\nयोगं देहि सर्वदा ॥',
'मुक्तिरूपिणि शारदा ।\nमोक्षं देहि सर्वदा ॥'],[7],title_sa='देहि देहि शारदा',chorus=True)
refrain='गुरोरङ्घ्रिपद्मे मनश्चेन्न लग्नं\nततः किं ततः किं ततः किं ततः किम् ॥'
add('guru-bhakti-gurvashtakam','Guru Bhakti — Gurvashtakam','ಗುರುಭಕ್ತಿ — ಗುರ್ವಷ್ಟಕಮ್',[
'शरीरं सुरूपं तथा वा कलत्रं\nयशश्चारुचित्रं धनं मेरुतुल्यम् ।',
'कलत्रं धनं पुत्रपौत्रादि सर्वं\nगृहं बान्धवाः सर्वमेतद्धि जातम् ।',
'षडङ्गादिवेदो मुखे शास्त्रविद्या\nकवित्वादिगद्यं सुपद्यं करोति ।',
'विदेशेषु मान्यः स्वदेशेषु धन्यः\nसदाचारवृत्तेषु मत्तो न चान्यः ।',
'क्षमामण्डले भूपभूपालवृन्दैः\nसदा सेवितं यस्य पादारविन्दम् ।',
'यशो मे गतं दिक्षु दानप्रतापा-\nज्जगद्वस्तु सर्वं करे यत्प्रसादात् ।',
'न भोगे न योगे न वा वाजिराजौ\nन कान्तामुखे नैव वित्तेषु चित्तम् ।',
'अरण्ये न वा स्वस्य गेहे न कार्ये\nन देहे मनो वर्तते मे त्वनर्घ्ये ।',
'अनर्घ्याणि रत्नानि मुक्तानि सम्यक्\nसमालिङ्गिता कामिनी यामिनीषु ।',
'गुरोरष्टकं यः पठेत्पुण्यदेही\nयतिर्भूपतिर्ब्रह्मचारी च गेही ।\nलभेद्वाञ्छितार्थं पदं ब्रह्मसंज्ञं\nगुरोरुक्तवाक्ये मनो यस्य लग्नम् ॥'],[9,8],title_sa='गुरुभक्तिः — गुर्वष्टकम्',refrain=refrain,extra='The family book includes an additional Anarghyani verse as stanza9, then the phalashruti as10; this extended family order is preserved. The refrain is the book’s sung order, not silently replaced by the alternate published order.',refs=[dict(label='Sanskrit Documents — comparison for the eight core verses',url='https://sanskritdocuments.org/doc_deities_misc/gurvashtakam.html')])
add('jagadguru-pancharatnamala','Sri Jagadguru Pancharatnamala','ಶ್ರೀ ಜಗದ್ಗುರು ಪಂಚರತ್ನಮಾಲಾ',[
'चन्द्रमौलिपूजकं समस्तपापनाशकं\nभक्तचित्तवशकं सदात्मनिष्ठमानसम् ।\nभस्मना विभूषितं करात्तदण्डशोभितं\nशृङ्गशैलभूषणं नमामि तं जगद्गुरुम् ॥ 1 ॥',
'चन्द्रचूडसद्गुरोः कराब्जसम्भवं विभुं\nज्ञानमुक्तिदायिनं नतोत्तमाकृतिं प्रभुम् ।\nमन्त्रशास्त्रवारिधिं क्षमानिधिं तपोनिधिं\nशृङ्गशैलभूषणं नमामि तं जगद्गुरुम् ॥ 2 ॥',
'वेदतत्त्वबोधकं स्वधर्ममार्गदर्शकं\nभक्तवत्सलं शुभं सुतीक्ष्णबुद्धिदायकम् ।\nहासपूर्वभाषिणं स्मिताननं परात्परं\nशृङ्गशैलभूषणं नमामि तं जगद्गुरुम् ॥ 3 ॥',
'दीनलोकरक्षकं हि पापलोकदुर्लभं\nआदरेण शिष्यकोटिसेविताङ्घ्रिपङ्कजम् ।\nभक्ततापहारिणं यतीश्वरं महेश्वरं\nशृङ्गशैलभूषणं नमामि तं जगद्गुरुम् ॥ 4 ॥',
'चन्द्रशेखराख्यसद्गुरोः पदाब्जसेवकं\nमोहनाशकं शिवं गणेशशारदार्चकम् ।\nद्वैतभीतिवारणं दयानिधिं गुरोर्गुरुं\nशृङ्गशैलभूषणं नमामि तं जगद्गुरुम् ॥ 5 ॥',
'पञ्चकं सद्गुरोर्नित्यं भक्त्या प्रपठतां नृणाम् ।\nआयुरारोग्यमैश्वर्यं भविष्यति न संशयः ॥'],[10],title_sa='श्रीजगद्गुरुपञ्चरत्नमालास्तोत्रम्',extra='The family page’s five verses and closing verse are retained. Roman spellings are rendered into Sanskrit orthography; Sharadacakam is read as Sharadarcakam (worshipper of Sharada). The original page remains available for comparison.')
add('shankara-guru','Shankara Guru','ಶಂಕರ ಗುರು',[
'शङ्कर गुरु जय शङ्कर गुरु ।\nशङ्कर भगवत्पाद शङ्कर गुरु ॥',
'दीनदयाल गुरुनाथ ।\nपूर्णकृपाल गुरुनाथ ।\nगुरुनाथ जय गुरुनाथ ।\nसद्गुरुनाथ गुरुनाथ ॥',
'अपारमहिमा गुरुनाथ ।\nकृपासागर गुरुनाथ ।\nगुरुनाथ जय गुरुनाथ ।\nसद्गुरुनाथ गुरुनाथ ॥'],[],title_sa='शङ्कर गुरु',lang='bhajan',extra='Devotional text transcribed from the supplied family page. The source photograph is not published because its handwritten margin contains contact information.')

def canonical(t):return unicodedata.normalize('NFD',t).translate(str.maketrans('०१२३४५६७८९','0123456789'))
def digest(chapters):return hashlib.sha256('\n\n'.join('\n\n'.join(c['paragraphs']) for c in chapters).encode()).hexdigest()
for entry in B:
 slug=entry['slug'];base=entry['paragraphs'];chapters=[]
 if entry.get('refrain'):
  base=[p+'\n'+entry['refrain']+f' {i} ॥' if i<10 else p for i,p in enumerate(base,1)]
  chapters=[dict(id='main',title='गुरुभक्तिः',paragraphs=base[:8]),dict(id='family-extra',title='परिवारपाठस्य अधिकश्लोकः',paragraphs=base[8:9]),dict(id='closing',title='फलश्रुतिः',paragraphs=base[9:])]
 else:chapters=[dict(id='main',title=entry['title_sa'],paragraphs=base)]
 if entry.get('chorus'):chapters.append(dict(id='refrain',title='पुनरावर्तनम्',paragraphs=[base[0]]))
 versions=[]
 for vid,lang,label,scheme in [('kannada','kn','ಕನ್ನಡ',sanscript.KANNADA),('devanagari','sa' if entry.get('lang','sa')=='sa' else 'hi','संस्कृतम्' if entry.get('lang','sa')=='sa' else 'देवनागरी',sanscript.DEVANAGARI),('roman','en','English (Roman)',sanscript.IAST)]:
  cs=[]
  for c in chapters:
   ps=[tr(p,sanscript.DEVANAGARI,scheme) if vid!='devanagari' else p for p in c['paragraphs']]
   if vid=='roman':ps=[p.replace('||','॥').replace('|','।') for p in ps]
   if vid!='devanagari':
    for old,new in zip(c['paragraphs'],ps):assert canonical(tr(new,scheme,sanscript.DEVANAGARI))==canonical(old),(slug,vid,old,new,tr(new,scheme,sanscript.DEVANAGARI))
   if vid=='roman' and entry.get('roman'):ps=entry['roman']
   cs.append({**c,'title':tr(c['title'],sanscript.DEVANAGARI,scheme),'paragraphs':ps})
  refs=[dict(label='Family book — supplied page',url=f'https://hawkeyedesi.github.io/family-songbook/assets/paduka-family-{n:02}.jpg') for n in entry['scans']]+entry.get('refs',[])
  if not refs:refs=[dict(label='Family scan — text transcribed; contact-bearing photograph kept private',url='https://hawkeyedesi.github.io/family-songbook/en/paduka-puja-bhajans/')]
  v=dict(id=vid,lang=lang,label=label,title=entry['kn'] if vid=='kannada' else entry['title_sa'] if vid=='devanagari' else entry['title'],chapters=cs,references=refs,source_sha256=digest(cs))
  if vid!='devanagari' and not(vid=='roman' and entry.get('roman')):v['derivation']=dict(tool='indic-transliteration',version='2.3.82',from_script='devanagari',from_sha256=digest(chapters),roundtrip_verified=True,normalization='Canonical Unicode equivalence and decimal digit values; lexical characters preserved.')
  versions.append(v)
 (ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
 s=by.get(slug) or dict(slug=slug,collections=['paduka-puja-bhajans'])
 s.update(title=entry['kn'],title_en=entry['title'],category='ಭಜನೆ / ಸ್ತೋತ್ರ',category_en='Bhajan / Stotra',language='ಕನ್ನಡ · देवनागरी · Roman',language_en='Kannada · Devanagari · Roman',script='kannada',versions_file=f'texts/{slug}.json',description='ಪಾದುಕಾ ಪೂಜೆಯ ಕುಟುಂಬದ ಭಜನೆ ಪುಸ್ತಕದಿಂದ.',description_en='From the family Paduka Puja bhajan book.',scans=[f'paduka-family-{n:02}.jpg' for n in entry['scans']],note='ಕುಟುಂಬದ ಪುಸ್ತಕದ ಪಾಠ ಮತ್ತು ಕ್ರಮವನ್ನು ಉಳಿಸಲಾಗಿದೆ. ಕನ್ನಡ ಮತ್ತು ದೇವನಾಗರಿ ಲಿಪಿಗಳು ಹಾಗೂ ರೋಮನ್ ಉಚ್ಚಾರಣಾ ಪಾಠ; ಅರ್ಥಾನುವಾದವಲ್ಲ.',note_en='Family-book reading and song order. Kannada/Devanagari are script renderings; Roman is pronunciation text, not an English meaning translation. '+entry.get('extra',''))
 if entry.get('chorus') or slug=='om-jai-jagdish-hare':
  s['note_en']+=' Return to the opening chorus after each stanza, as marked in the book.'
  s['note']+=' ಪ್ರತಿ ಚರಣದ ನಂತರ ಆರಂಭದ ಪಲ್ಲವಿಯನ್ನು ಪುನರಾವರ್ತಿಸಿ.'
 if slug=='om-jai-jagdish-hare':s['note_en']+=' This is a Hindi arati, not a Sanskrit translation. The supplied Roman lines resolve the damaged Devanagari printing; the family Roman singing expansions are retained.'
 if slug not in by:songs.append(s);by[slug]=s
# Reuse existing entries rather than duplicate them; retain other collection memberships.
for slug,nums in [('hanuman-chalisa',[4,3]),('mahalakshmi-ashtakam',[5]),('amma-baaramma',[6])]:
 s=by[slug]
 if 'paduka-puja-bhajans' not in s['collections']:s['collections'].append('paduka-puja-bhajans')
 s['scans']=list(dict.fromkeys(s.get('scans',[])+[f'paduka-family-{n:02}.jpg' for n in nums]))
order=['durga-saptashloki','om-jai-jagdish-hare','hanuman-chalisa','mahalakshmi-ashtakam','amma-baaramma','sharade-sharade','dehi-dehi-sharada','guru-bhakti-gurvashtakam','jagadguru-pancharatnamala','shankara-guru']
for i,slug in enumerate(order,1):by[slug].setdefault('collection_order',{})['paduka-puja-bhajans']=i
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')
print('Imported7new works; reused3existing works; PadukaPuja10distinct entries in supplied batch order.')
