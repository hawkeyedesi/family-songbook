/* Playback is optional; published prayer text always remains independent of ASR. */
(() => {
  const node = document.getElementById('recording-config');
  if (!node) return;
  const config = JSON.parse(node.textContent);
  const labels = config.labels;
  const text = document.getElementById('recording-text');
  const scroll = document.getElementById('recording-scroll');
  const work = document.getElementById('recording-work');
  const follow = document.getElementById('follow-recording');
  const status = document.getElementById('reading-status');
  const playerStatus = document.getElementById('player-status');
  const cueLabel = document.getElementById('active-recording-cue');
  const fullLink = document.getElementById('recording-full-text');
  const scriptLinks = [...document.querySelectorAll('[data-reader-script]')];
  let script = config.script, currentWork = config.defaultWork, request = 0;
  let player = null, interval = null, activeCue = undefined, started = false, playerReady = false, pendingStart = null;
  let partIndex = config.parts.length - 1;
  const cache = new Map();
  const formatTime = t => `${Math.floor(t / 60).toString().padStart(2, '0')}:${Math.floor(t % 60).toString().padStart(2, '0')}`;
  const findCue = (cues, time) => cues.find(c => time >= c.start && time < c.end) || null;
  const cueTitle = c => config.ui === 'en' ? (c.label_en || c.label) : c.label;
  const textURL = (slug, s) => new URL(`${config.base}songs/${slug}/${s === 'kannada' ? '' : s + '/'}`, location.href).href;
  function updateScriptLinks() {
    for (const a of scriptLinks) {
      a.href = textURL(currentWork, a.dataset.readerScript);
      if (a.dataset.readerScript === script) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    }
    fullLink.href = textURL(currentWork, script);
  }
  function visibleAnchor() {
    const top = scroll.getBoundingClientRect().top;
    let candidates = text.querySelectorAll('[data-name], [data-verse]');
    if (!candidates.length) candidates = text.querySelectorAll('.text-chapter');
    for (const el of candidates) {
      if (el.getBoundingClientRect().bottom > top + 18) return el.id;
    }
    return null;
  }
  function jump(anchor) {
    if (!anchor) return;
    const target = text.querySelector(`#${CSS.escape(anchor)}`);
    if (!target) return;
    for (const el of text.querySelectorAll('.recording-current-line')) el.classList.remove('recording-current-line');
    target.classList.add('recording-current-line');
    scroll.scrollTop += target.getBoundingClientRect().top - scroll.getBoundingClientRect().top - 18;
  }
  async function read(slug, anchor = null) {
    const token = ++request;
    currentWork = slug; work.value = slug; updateScriptLinks();
    const url = textURL(slug, script); status.textContent = labels.textLoading;
    text.hidden = true;
    try {
      if (!cache.has(url)) {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Reading page unavailable');
        const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
        const article = doc.querySelector('article.lyrics');
        if (!article) throw new Error('Missing published reading');
        cache.set(url, { article, title: doc.querySelector('h1').textContent, notes: [...doc.querySelectorAll('.svara-notice, .svara-key, .source > p')] });
      }
      if (token !== request) return; // Never show a stale result after a fast seek/script change.
      const result = cache.get(url);
      text.replaceChildren(...result.notes.map(n => n.cloneNode(true)), ...[...result.article.childNodes].map(n => n.cloneNode(true)));
      text.className = result.article.className; text.lang = result.article.lang;
      text.hidden = false;
      document.getElementById('recording-text-title').textContent = result.title;
      scroll.scrollTop = 0; status.textContent = '';
      await document.fonts.ready;
      if (token === request) jump(anchor);
    } catch (error) {
      if (token !== request) return;
      status.textContent = labels.textError; text.hidden = true;
    }
  }
  function sync(force = false) {
    if (!player?.getCurrentTime) return;
    const time = player.getCurrentTime();
    document.getElementById('current-recording-time').textContent = `${formatTime(time)} / ${formatTime(config.duration)}`;
    if (!follow.checked || !started) return;
    const cue = findCue(config.cues, time);
    if (!force && cue?.id === activeCue?.id && (cue || activeCue === null)) return;
    activeCue = cue;
    for (const b of document.querySelectorAll('[data-cue]')) {
      if (cue && b.dataset.cue === cue.id) b.setAttribute('aria-current', 'true');
      else b.removeAttribute('aria-current');
    }
    cueLabel.textContent = cue ? cueTitle(cue) : '';
    if (!cue?.work) {
      ++request; text.hidden = true; status.textContent = labels.unmapped;
      return;
    }
    if (currentWork !== cue.work || text.hidden || force) read(cue.work, cue.anchor);
    else jump(cue.anchor);
  }
  function seek(cue) {
    follow.checked = true; started = true; activeCue = undefined;
    cueLabel.textContent = cueTitle(cue);
    if (cue.work) read(cue.work, cue.anchor);
    else { ++request; text.hidden = true; status.textContent = labels.unmapped; }
    pendingStart = cue.start;
    if (playerReady) { player.seekTo(pendingStart, true); player.playVideo(); }
    else loadPlayer(cue.start);
  }
  function createPlayer() {
    player = new YT.Player('nav-player', {
      host: 'https://www.youtube-nocookie.com', width: '100%', height: '230', videoId: config.videoId,
      playerVars: { playsinline: 1, origin: location.origin, rel: 0, start: Math.floor(pendingStart || 0) },
      events: {
        onReady: () => {
          playerReady = true;
          playerStatus.textContent = labels.ready;
          interval = setInterval(sync, 500);
          if (pendingStart !== null) { started = true; player.loadVideoById({videoId: config.videoId, startSeconds: pendingStart}); }
        },
        onStateChange: event => {
          if (event.data === 0 && partIndex < config.parts.length - 1) { selectPart(partIndex + 1); return; }
          if ([1, 2, 0].includes(event.data)) { started = true; sync(); }
        },
        onError: () => { playerStatus.textContent = labels.error; }
      }
    });
  }
  let loading = false;
  function loadPlayer(startAt = null) {
    if (startAt !== null) pendingStart = startAt;
    if (loading || player) return;
    loading = true; document.getElementById('load-recording').disabled = true;
    playerStatus.textContent = labels.loading;
    if (window.YT?.Player) { createPlayer(); return; }
    const previous = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => { if (previous) previous(); createPlayer(); };
    const api = document.createElement('script'); api.src = 'https://www.youtube.com/iframe_api';
    api.onerror = () => {
      playerStatus.textContent = labels.error; loading = false;
      document.getElementById('load-recording').disabled = false;
    };
    document.head.append(api);
  }
  function selectPart(index) {
    partIndex = index;
    const part = config.parts[index];
    for (const key of ['videoId', 'sourceUrl', 'duration', 'cues', 'defaultWork', 'start']) config[key] = part[key];
    pendingStart = part.start || 0; started = true; activeCue = undefined; follow.checked = true;
    document.querySelector('.recording-external').href = part.sourceUrl;
    for (const b of document.querySelectorAll('[data-recording-part]')) {
      if (Number(b.dataset.recordingPart) === index) b.setAttribute('aria-current', 'true');
      else b.removeAttribute('aria-current');
    }
    const list = document.getElementById('recording-sequence'); list.replaceChildren();
    for (const cue of config.cues) {
      const li = document.createElement('li'), button = document.createElement('button');
      button.type = 'button'; button.dataset.cue = cue.id;
      button.textContent = `${formatTime(cue.start)}  ${cueTitle(cue)}`;
      button.addEventListener('click', () => seek(cue)); li.append(button); list.append(li);
    }
    const first = findCue(config.cues, pendingStart);
    if (first?.work) read(first.work, first.anchor);
    else { ++request; text.hidden = true; status.textContent = labels.unmapped; }
    if (playerReady) player.loadVideoById({videoId: part.videoId, startSeconds: pendingStart});
    else loadPlayer(pendingStart);
  }
  for (const b of document.querySelectorAll('[data-recording-part]')) b.addEventListener('click', () => selectPart(Number(b.dataset.recordingPart)));
  document.getElementById('load-recording').addEventListener('click', () => selectPart(0));
  for (const b of document.querySelectorAll('[data-cue]')) b.addEventListener('click', () => seek(config.cues.find(c => c.id === b.dataset.cue)));
  follow.addEventListener('change', () => { if (follow.checked) sync(true); else status.textContent = labels.manual; });
  work.addEventListener('change', () => { follow.checked = false; activeCue = undefined; cueLabel.textContent = ''; read(work.value); });
  for (const link of scriptLinks) link.addEventListener('click', event => {
    event.preventDefault();
    const anchor = visibleAnchor(); script = link.dataset.readerScript;
    try { localStorage.setItem('bhakti-script', script); } catch {}
    updateScriptLinks();
    if (started && follow.checked && !activeCue?.work) {
      ++request; text.hidden = true; status.textContent = labels.unmapped;
    } else read(currentWork, anchor || activeCue?.anchor);
  });
  for (const [id, delta] of [['nav-text-smaller', -.12], ['nav-text-larger', .12]]) {
    document.getElementById(id).addEventListener('click', () => {
      const current = parseFloat(getComputedStyle(scroll).getPropertyValue('--lyrics-size')) || 1.28;
      scroll.style.setProperty('--lyrics-size', `${Math.max(.9, Math.min(2.2, current + delta))}rem`);
    });
  }
  try {
    const preferred = localStorage.getItem('bhakti-script');
    if (['kannada', 'devanagari', 'roman'].includes(preferred) && preferred !== script) {
      script = preferred; read(currentWork);
    }
  } catch {}
  updateScriptLinks();
  window.addEventListener('pagehide', () => clearInterval(interval));
  window.BhaktiRecording = { findCue, sync, config, selectPart };
})();
