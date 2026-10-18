// KrishiAtlas & KrishiGrantha — Core Client-Side Logic & TTS Engine

// 1. Theme Management
function initTheme() {
  const saved = localStorage.getItem('krishi-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcon(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('krishi-theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const btn = document.getElementById('theme-toggle-btn');
  if (btn) {
    btn.innerHTML = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
}

// 2. Web Speech API Text-To-Speech (TTS) Engine
class TTSEngine {
  constructor() {
    this.synth = window.speechSynthesis;
    this.utterance = null;
    this.isPlaying = false;
    this.isPaused = false;
    this.rate = 1.0;
    this.statusEl = document.getElementById('tts-status');
  }

  getCleanArticleText() {
    const articleEl = document.querySelector('.article-content') || document.querySelector('.content-body');
    if (!articleEl) return '';
    // clone to avoid altering DOM
    const clone = articleEl.cloneNode(true);
    // remove non-spoken elements
    clone.querySelectorAll('script, style, code, .no-tts').forEach(el => el.remove());
    return clone.innerText.replace(/\s+/g, ' ').trim();
  }

  play() {
    if (!this.synth) {
      alert("Text-to-Speech is not supported in this browser.");
      return;
    }

    if (this.isPaused) {
      this.synth.resume();
      this.isPlaying = true;
      this.isPaused = false;
      this.updateStatus("Playing audio narration...");
      return;
    }

    const text = this.getCleanArticleText();
    if (!text) {
      alert("No readable article content found on this page.");
      return;
    }

    this.synth.cancel(); // clear queue
    this.utterance = new SpeechSynthesisUtterance(text);
    this.utterance.rate = this.rate;
    this.utterance.lang = 'en-IN'; // Indian English accent preference if available

    this.utterance.onstart = () => {
      this.isPlaying = true;
      this.isPaused = false;
      this.updateStatus("Playing audio narration (Web Speech API)...");
      const playBtn = document.getElementById('tts-play-btn');
      if (playBtn) playBtn.innerText = '⏸️ Pause';
    };

    this.utterance.onend = () => {
      this.isPlaying = false;
      this.isPaused = false;
      this.updateStatus("Narration complete.");
      const playBtn = document.getElementById('tts-play-btn');
      if (playBtn) playBtn.innerText = '▶️ Listen to Article';
    };

    this.utterance.onerror = (e) => {
      console.error("TTS Error:", e);
      this.isPlaying = false;
      this.updateStatus("Narration paused or ended.");
    };

    this.synth.speak(this.utterance);
  }

  pause() {
    if (this.isPlaying && !this.isPaused) {
      this.synth.pause();
      this.isPaused = true;
      this.isPlaying = false;
      this.updateStatus("Narration paused.");
      const playBtn = document.getElementById('tts-play-btn');
      if (playBtn) playBtn.innerText = '▶️ Resume';
    } else if (this.isPaused) {
      this.play();
    }
  }

  stop() {
    if (this.synth) {
      this.synth.cancel();
      this.isPlaying = false;
      this.isPaused = false;
      this.updateStatus("Narration stopped.");
      const playBtn = document.getElementById('tts-play-btn');
      if (playBtn) playBtn.innerText = '▶️ Listen to Article';
    }
  }

  setRate(newRate) {
    this.rate = parseFloat(newRate);
    if (this.isPlaying) {
      this.stop();
      this.play();
    }
  }

  updateStatus(msg) {
    if (this.statusEl) this.statusEl.innerText = msg;
  }
}

let ttsInstance = null;

// 3. Section 10(1) Partial Integration Income Tax Calculator
function calculateAgriTax() {
  const salaryCTC = parseFloat(document.getElementById('tax-ctc')?.value || 360000);
  const farmIncome = parseFloat(document.getElementById('tax-farm')?.value || 150000);
  const regime = document.getElementById('tax-regime')?.value || 'new';

  // Standard deduction
  const stdDed = regime === 'new' ? 75000 : 50000;
  const taxableSalary = Math.max(0, salaryCTC - stdDed);

  let baselineTax = 0;
  let integratedTax = 0;
  let calculationSteps = [];

  if (regime === 'new') {
    // FY 2025-26 / AY 2026-27 Slabs under 115BAC:
    // 0 - 3L: Nil
    // 3L - 7L: 5%
    // 7L - 10L: 10%
    // 10L - 12L: 15%
    // 12L - 15L: 20%
    // Above 15L: 30%
    // Rebate u/s 87A: Full rebate if taxable non-agri income <= 7L (under standard provisions)

    function computeNewSlabTax(income) {
      let t = 0;
      if (income <= 300000) return 0;
      if (income > 300000) t += Math.min(income - 300000, 400000) * 0.05;
      if (income > 700000) t += Math.min(income - 700000, 300000) * 0.10;
      if (income > 1000000) t += Math.min(income - 1000000, 200000) * 0.15;
      if (income > 1200000) t += Math.min(income - 1200000, 300000) * 0.20;
      if (income > 1500000) t += (income - 1500000) * 0.30;
      return t;
    }

    // Check partial integration condition
    const triggersIntegration = farmIncome > 5000 && taxableSalary > 300000;

    if (!triggersIntegration) {
      baselineTax = taxableSalary <= 700000 ? 0 : computeNewSlabTax(taxableSalary);
      integratedTax = baselineTax;
      calculationSteps.push("Partial integration does NOT trigger because either net agricultural income is under ₹5,000 or taxable non-agri income is below the basic exemption slab (₹3,00,000).");
      calculationSteps.push(`Result: Agricultural income of ₹${farmIncome.toLocaleString('en-IN')} is 100% tax-free.`);
    } else {
      // Step 1: Tax on (Non-agri taxable + Net farm income)
      const combinedIncome = taxableSalary + farmIncome;
      const step1Tax = computeNewSlabTax(combinedIncome);

      // Step 2: Tax on (Basic slab ₹3L + Net farm income)
      const step2Income = 300000 + farmIncome;
      const step2Tax = computeNewSlabTax(step2Income);

      // Step 3: Step 1 minus Step 2
      let step3Tax = Math.max(0, step1Tax - step2Tax);

      // Rebate u/s 87A check
      if (taxableSalary <= 700000) {
        step3Tax = 0; // 87A covers up to 7L taxable non-agri income
        calculationSteps.push("Rebate under Section 87A reduces tax to ₹0 because non-agricultural taxable income is <= ₹7,00,000.");
      }

      const cess = Math.round(step3Tax * 0.04);
      integratedTax = step3Tax + cess;

      calculationSteps.push(`Step 1: Tax on Combined Income (₹${taxableSalary.toLocaleString('en-IN')} + ₹${farmIncome.toLocaleString('en-IN')} = ₹${combinedIncome.toLocaleString('en-IN')}): ₹${Math.round(step1Tax).toLocaleString('en-IN')}`);
      calculationSteps.push(`Step 2: Tax on Basic Exemption + Farm Income (₹3,00,000 + ₹${farmIncome.toLocaleString('en-IN')} = ₹${step2Income.toLocaleString('en-IN')}): ₹${Math.round(step2Tax).toLocaleString('en-IN')}`);
      calculationSteps.push(`Step 3: Difference (Step 1 - Step 2): ₹${Math.round(step3Tax).toLocaleString('en-IN')}`);
      calculationSteps.push(`Step 4: Health & Education Cess (4%): ₹${cess.toLocaleString('en-IN')}`);
      calculationSteps.push(`Final Total Tax Payable: ₹${integratedTax.toLocaleString('en-IN')}`);
    }
  }

  // Render results
  const resEl = document.getElementById('tax-calc-results');
  if (resEl) {
    resEl.innerHTML = `
      <div class="calc-result-title">Tax Computation Results (${regime === 'new' ? 'New Regime u/s 115BAC' : 'Old Tax Regime'})</div>
      <p><strong>Non-Agri Taxable Salary:</strong> ₹${taxableSalary.toLocaleString('en-IN')} (Gross ₹${salaryCTC.toLocaleString('en-IN')} minus ₹${stdDed.toLocaleString('en-IN')} standard deduction)</p>
      <p><strong>Reported Net Farm Income:</strong> ₹${farmIncome.toLocaleString('en-IN')} (Exempt u/s 10(1))</p>
      <div style="background: rgba(0,0,0,0.04); padding: 1rem; border-radius: 6px; margin: 1rem 0; font-family: monospace; font-size: 0.9rem;">
        ${calculationSteps.map(s => `<div>• ${s}</div>`).join('')}
      </div>
      <p><strong>Net Additional Tax Incurred Due to Farm Income:</strong> <span style="color: ${integratedTax > baselineTax ? '#b91c1c' : '#047857'}; font-weight: 700;">₹${Math.max(0, integratedTax - baselineTax).toLocaleString('en-IN')}</span></p>
    `;
  }
}

// 4. Instant Search Logic
let searchIndex = [];

async function loadSearchIndex() {
  try {
    const res = await fetch('search_index.json');
    if (res.ok) {
      searchIndex = await res.json();
    }
  } catch (e) {
    console.warn("Could not load search index:", e);
  }
}

function handleSearch(query) {
  const q = query.trim().toLowerCase();
  const resultsContainer = document.getElementById('search-results');
  if (!resultsContainer) return;

  if (!q || q.length < 2) {
    resultsContainer.innerHTML = '';
    resultsContainer.style.display = 'none';
    return;
  }

  const matches = searchIndex.filter(item => {
    return item.keywords.includes(q) || item.title.toLowerCase().includes(q) || item.id.toLowerCase().includes(q);
  }).slice(0, 15);

  if (matches.length === 0) {
    resultsContainer.innerHTML = `<div style="padding: 1rem; color: var(--text-muted); text-align: center;">No matching articles or records found for "${query}".</div>`;
    resultsContainer.style.display = 'block';
    return;
  }

  resultsContainer.innerHTML = matches.map(m => `
    <a href="${m.url}" class="search-result-item" style="display: block; padding: 0.8rem 1rem; border-bottom: 1px solid var(--border-subtle); text-decoration: none; color: inherit;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
        <span style="font-weight: 700; color: var(--primary-deep); font-size: 1rem;">${m.title}</span>
        <span class="badge" style="text-transform: uppercase; font-size: 0.7rem;">${m.type}</span>
      </div>
      <div style="font-size: 0.8rem; color: var(--text-muted);">
        ${m.part > 0 ? `Part ${m.part}: ${m.part_title}` : m.part_title} ${m.id ? `• ${m.id}` : ''}
      </div>
      ${m.snippet ? `<div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.3rem;">${m.snippet}</div>` : ''}
    </a>
  `).join('');
  resultsContainer.style.display = 'block';
}

// Initialization on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  ttsInstance = new TTSEngine();
  loadSearchIndex();

  const themeBtn = document.getElementById('theme-toggle-btn');
  if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

  const ttsPlayBtn = document.getElementById('tts-play-btn');
  if (ttsPlayBtn) ttsPlayBtn.addEventListener('click', () => ttsInstance.play());

  const ttsPauseBtn = document.getElementById('tts-pause-btn');
  if (ttsPauseBtn) ttsPauseBtn.addEventListener('click', () => ttsInstance.pause());

  const ttsStopBtn = document.getElementById('tts-stop-btn');
  if (ttsStopBtn) ttsStopBtn.addEventListener('click', () => ttsInstance.stop());

  const ttsRateSelect = document.getElementById('tts-rate-select');
  if (ttsRateSelect) {
    ttsRateSelect.addEventListener('change', (e) => ttsInstance.setRate(e.target.value));
  }

  const searchInput = document.getElementById('global-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => handleSearch(e.target.value));
  }

  const calcBtn = document.getElementById('tax-calc-btn');
  if (calcBtn) {
    calcBtn.addEventListener('click', calculateAgriTax);
    calculateAgriTax(); // initial run
  }
});
