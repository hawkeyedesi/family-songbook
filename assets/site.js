'use strict';
const search = document.querySelector('#search');
if (search) search.addEventListener('input', () => {
  const query = search.value.trim().toLocaleLowerCase();
  const cards = [...document.querySelectorAll('.song-card')];
  for (const card of cards) card.hidden = !card.textContent.toLocaleLowerCase().includes(query);
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
  try {
    if (navigator.share) { await navigator.share({ title: document.title, url: location.href }); status.textContent = 'Link shared.'; }
    else if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(location.href); status.textContent = 'Link copied. Paste it into WhatsApp or a message.'; }
    else { status.textContent = `Copy this link: ${location.href}`; }
  } catch (error) { if (error.name !== 'AbortError') status.textContent = `Copy this link: ${location.href}`; }
});
