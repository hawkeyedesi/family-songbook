'use strict';
const search = document.querySelector('#search');
if (search) search.addEventListener('input', () => {
  const query = search.value.trim().toLocaleLowerCase();
  const cards = [...document.querySelectorAll('.song-card')];
  for (const card of cards) card.hidden = !(card.textContent + ' ' + (card.dataset.search || '')).toLocaleLowerCase().includes(query);
  document.querySelector('#empty').hidden = cards.some(card => !card.hidden);
});
let size = 1.28;
try { const saved = Number(localStorage.getItem('bhakti-text-size')); if (saved >= 1 && saved <= 2) size = saved; } catch {}
function applySize() {
  document.documentElement.style.setProperty('--lyrics-size', `${size}rem`);
  const smaller = document.querySelector('#smaller');
  const larger = document.querySelector('#larger');
  if (smaller) smaller.disabled = size <= 1;
  if (larger) larger.disabled = size >= 2;
}
function resize(delta) {
  size = Math.min(2, Math.max(1, Math.round((size + delta) * 100) / 100));
  applySize();
  try { localStorage.setItem('bhakti-text-size', String(size)); } catch {}
}
applySize();
document.querySelector('#smaller')?.addEventListener('click', () => resize(-.12));
document.querySelector('#larger')?.addEventListener('click', () => resize(.12));
document.querySelector('#print')?.addEventListener('click', () => window.print());
document.querySelector('#share')?.addEventListener('click', async () => {
  const status = document.querySelector('#share-status');
  const english = document.documentElement.dataset.ui === 'en';
  try {
    if (navigator.share) { await navigator.share({ title: document.title, url: location.href }); status.textContent = english ? 'Link shared.' : 'ಲಿಂಕ್ ಹಂಚಿಕೊಳ್ಳಲಾಗಿದೆ.'; }
    else if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(location.href); status.textContent = english ? 'Link copied. Paste it into a message.' : 'ಲಿಂಕ್ ನಕಲಿಸಲಾಗಿದೆ. ಸಂದೇಶದಲ್ಲಿ ಅಂಟಿಸಿ ಹಂಚಿಕೊಳ್ಳಿ.'; }
    else { status.textContent = `${english ? 'Copy this link:' : 'ಈ ಲಿಂಕ್ ನಕಲಿಸಿ:'} ${location.href}`; }
  } catch (error) { if (error.name !== 'AbortError') status.textContent = `${english ? 'Copy this link:' : 'ಈ ಲಿಂಕ್ ನಕಲಿಸಿ:'} ${location.href}`; }
});

// Store only the reading-script preference on this browser, never centrally.
const scriptLinks = document.querySelectorAll('[data-script]');
for (const link of scriptLinks) {
  if (location.hash) link.hash = location.hash;
  link.addEventListener('click', () => {
    try { localStorage.setItem('bhakti-script', link.dataset.script); } catch {}
  });
}
try {
  const preferred = localStorage.getItem('bhakti-script');
  if (['kannada', 'devanagari', 'roman'].includes(preferred)) {
    for (const card of document.querySelectorAll('.song-card[data-multiscript="true"]')) {
      card.href = card.dataset.base + (preferred === 'kannada' ? '' : preferred + '/');
    }
  }
} catch {}
