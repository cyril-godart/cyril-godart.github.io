/* Reveal au scroll (IntersectionObserver) */
const revealEls = document.querySelectorAll('.reveal, .animate');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
}, { threshold: 0.12 });
revealEls.forEach(el => observer.observe(el));

/* Menu mobile overlay */
const toggle = document.getElementById('mobileToggle');
let mobileMenu;
if(toggle) {
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', (!expanded).toString());
    if (!mobileMenu) {
      mobileMenu = document.createElement('div');
      mobileMenu.className = 'mobile-menu';
      mobileMenu.setAttribute('id', 'mobileMenu');
      mobileMenu.innerHTML = `
        <a href="#presentation">À propos</a>
        <a href="#competences">Compétences</a>
        <a href="#contact">Contact</a>
      `;
      document.body.appendChild(mobileMenu);
    }
    mobileMenu.style.display = (mobileMenu.style.display === 'flex') ? 'none' : 'flex';
  });
}

/* Tilt 3D sur cartes */
const tiltCards = document.querySelectorAll('.tilt');
tiltCards.forEach(card => {
  let rafId = null;
  const reset = () => { card.style.transform = ''; };
  card.addEventListener('mousemove', (e) => {
    if (rafId) cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(() => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const rotateX = ((y - cy) / cy) * -4;
      const rotateY = ((x - cx) / cx) * 4;
      card.style.transform = `translateY(-4px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
  });
  card.addEventListener('mouseleave', reset);
});

/* Boutons magnétiques */
const magneticBtns = document.querySelectorAll('.magnetic');
magneticBtns.forEach(btn => {
  btn.style.transform = 'translate3d(0,0,0)';
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const relX = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
    const relY = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
    btn.style.transform = `translate(${relX * 6}px, ${relY * 4}px)`;
  });
  btn.addEventListener('mouseleave', () => { btn.style.transform = 'translate3d(0,0,0)'; });
});

/* Grille: animation séquentielle au chargement */
const gridCells = document.querySelectorAll('#grid .cell');
window.addEventListener('load', () => {
  gridCells.forEach((cell, i) => {
    setTimeout(() => cell.classList.add('visible'), 60 * i);
  });
});

/* Arrière-plan particules discrètes */
const canvas = document.getElementById('bgFlow');
if(canvas) {
  const ctx = canvas.getContext('2d', { alpha: true });
  let w, h, particles = [], lastTime = 0;

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  function initParticles(count = Math.floor((w * h) / 90000) + 20) {
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.6 + 0.6,
      });
    }
  }
  initParticles();

  function step(ts) {
    const dt = Math.min(32, ts - lastTime); lastTime = ts;
    ctx.clearRect(0, 0, w, h);

    particles.forEach(p => {
      p.x += p.vx * dt; p.y += p.vy * dt;
      if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;
      ctx.beginPath();
      ctx.fillStyle = 'rgba(15,23,42,0.08)';
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    });

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const a = particles[i], b = particles[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const d2 = dx*dx + dy*dy;
        if (d2 < 120*120) {
          const alpha = 1 - d2 / (120*120);
          ctx.strokeStyle = `rgba(15,23,42,${alpha * 0.05})`;
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
    }
    requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}