(() => {
  const header = document.querySelector('[data-header]');
  const menuButton = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-nav]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const onScroll = () => header?.classList.toggle('is-scrolled', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  const closeMenu = () => {
    menuButton?.setAttribute('aria-expanded', 'false');
    nav?.classList.remove('is-open');
    document.body.classList.remove('menu-open');
  };

  menuButton?.addEventListener('click', () => {
    const opening = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(opening));
    nav?.classList.toggle('is-open', opening);
    document.body.classList.toggle('menu-open', opening);
  });
  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });

  // Content stays visible if either animation library fails to load.
  const { gsap, ScrollTrigger } = window;
  if (gsap && ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    const media = gsap.matchMedia();
    // Dock-style magnification from the button animation reference.
    media.add('(min-width: 1121px) and (hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)', () => {
      const buttons = [...document.querySelectorAll('[data-nav] a')];
      // Stable hit areas prevent hover flicker while the visible labels move.
      const faces = buttons.map((button) => {
        const face = document.createElement('span');
        face.className = 'header-button-face';
        while (button.firstChild) face.append(button.firstChild);
        button.append(face);
        return face;
      });
      const setters = faces.map((face) => ({
        scaleX: gsap.quickTo(face, 'scaleX', { duration: 0.32, ease: 'power3.out' }),
        scaleY: gsap.quickTo(face, 'scaleY', { duration: 0.32, ease: 'power3.out' }),
        x: gsap.quickTo(face, 'x', { duration: 0.32, ease: 'power3.out' }),
        y: gsap.quickTo(face, 'y', { duration: 0.32, ease: 'power3.out' }),
      }));
      const animateDock = (pointerX = null) => {
        const boxes = buttons.map((button) => button.getBoundingClientRect());
        const weights = boxes.map((box) => {
          if (pointerX === null) return 0;
          const distance = Math.abs(pointerX - (box.left + box.width / 2));
          return Math.max(0, 1 - distance / 150) ** 2;
        });
        const growth = weights.map((weight, i) => boxes[i].width * weight * 0.32);
        const total = growth.reduce((sum, value) => sum + value, 0);
        let offset = -total / 2;
        setters.forEach((set, i) => {
          set.scaleX(1 + growth[i] / boxes[i].width);
          set.scaleY(1 + growth[i] / boxes[i].width);
          set.x(offset + growth[i] / 2);
          set.y(-8 * weights[i]);
          offset += growth[i];
        });
      };
      const onMove = (event) => {
        const first = buttons[0].getBoundingClientRect();
        const last = buttons[buttons.length - 1].getBoundingClientRect();
        animateDock(event.clientX >= first.left - 16 && event.clientX <= last.right + 16 ? event.clientX : null);
      };
      const reset = () => animateDock();
      const onFocus = (event) => {
        const button = event.target.closest('[data-nav] a');
        if (!button) return;
        const box = button.getBoundingClientRect();
        animateDock(box.left + box.width / 2);
      };
      header.addEventListener('pointermove', onMove);
      header.addEventListener('pointerleave', reset);
      header.addEventListener('focusin', onFocus);
      header.addEventListener('focusout', reset);
      return () => {
        header.removeEventListener('pointermove', onMove);
        header.removeEventListener('pointerleave', reset);
        header.removeEventListener('focusin', onFocus);
        header.removeEventListener('focusout', reset);
        gsap.killTweensOf(faces);
        faces.forEach((face) => face.replaceWith(...face.childNodes));
      };
    });
    media.add('(prefers-reduced-motion: no-preference)', () => {
      if (!header) return;
      let lastScroll = window.scrollY;
      let hidden = false;
      const showHeader = (hide = false, immediate = false) => {
        if (hide === hidden && !immediate) return;
        hidden = hide;
        // Animate top so the mobile menu keeps its viewport positioning.
        gsap.to(header, {
          top: hide ? -header.offsetHeight - 36 : 0,
          duration: immediate ? 0 : 0.3,
          ease: 'power2.out', overwrite: true,
        });
      };
      ScrollTrigger.create({
        start: 0,
        end: 'max',
        onUpdate: (self) => {
          const scroll = Math.max(0, self.scroll());
          const keyboardFocus = header.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
          if (scroll < header.offsetHeight || nav?.classList.contains('is-open') || keyboardFocus) {
            showHeader();
            lastScroll = scroll;
            return;
          }
          if (Math.abs(scroll - lastScroll) < 8) return;
          showHeader(self.direction === 1);
          lastScroll = scroll;
        },
      });
      const onHeaderFocus = () => showHeader(false, true);
      const onMenuClick = () => showHeader(false, true);
      header.addEventListener('focusin', onHeaderFocus);
      menuButton?.addEventListener('click', onMenuClick);
      return () => {
        header.removeEventListener('focusin', onHeaderFocus);
        menuButton?.removeEventListener('click', onMenuClick);
        gsap.killTweensOf(header);
        gsap.set(header, { clearProps: 'top' });
      };
    });
    media.add({
      desktop: '(min-width: 821px)',
      motion: '(prefers-reduced-motion: no-preference)',
    }, (context) => {
      if (!context.conditions.motion) return;
      const desktop = context.conditions.desktop;
      document.documentElement.classList.add('scroll-animations');
      const revealItems = gsap.utils.toArray('.reveal');
      revealItems.forEach((item) => item.classList.add('is-animating'));
      gsap.set(revealItems, { opacity: 0, y: desktop ? 48 : 24 });
      ScrollTrigger.batch(revealItems, {
        start: 'top 94%',
        once: true,
        interval: 0.1,
        onEnter: (items) => gsap.to(items, {
          opacity: 1, y: 0, duration: 0.9,
          stagger: 0.1, ease: 'power3.out', overwrite: 'auto',
          clearProps: 'opacity,transform',
          onComplete: () => items.forEach((item) => item.classList.remove('is-animating')),
        }),
      });

      // Keyboard navigation must never land on an invisible control.
      const revealFocused = (event) => {
        const item = event.target.closest('.reveal');
        if (!item) return;
        gsap.killTweensOf(item);
        gsap.set(item, { clearProps: 'opacity,transform' });
        item.classList.remove('is-animating');
      };
      document.addEventListener('focusin', revealFocused);

      gsap.to('.scroll-progress', {
        scaleX: 1, ease: 'none',
        scrollTrigger: { start: 0, end: 'max', scrub: true },
      });
      if (desktop && document.querySelector('.hero')) {
        gsap.fromTo('.hero-media img', { scale: 1.04, yPercent: 0 }, {
          scale: 1.15, yPercent: 7, ease: 'none',
          scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 },
        });
        gsap.to('.hero-copy', {
          y: -65, ease: 'none',
          scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 },
        });
        gsap.utils.toArray('.project-visual img').forEach((img) => {
          gsap.fromTo(img, { scale: 1.12, yPercent: -3 }, {
            scale: 1.04, yPercent: 0, ease: 'none',
            scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: 1 },
          });
        });
      }
      return () => {
        document.documentElement.classList.remove('scroll-animations');
        revealItems.forEach((item) => item.classList.remove('is-animating'));
        document.removeEventListener('focusin', revealFocused);
      };
    });
    // Recalculate after web fonts and lazy images settle.
    document.fonts?.ready.then(() => ScrollTrigger.refresh());
    document.querySelectorAll('img').forEach((img) => {
      if (!img.complete) img.addEventListener('load', () => ScrollTrigger.refresh(), { once: true });
    });
    window.addEventListener('load', () => ScrollTrigger.refresh(), { once: true });
  }

  if (!reduceMotion && 'IntersectionObserver' in window) {
    document.querySelectorAll('[data-counter]').forEach((counter) => {
      const original = counter.dataset.counter || '';
      const match = original.match(/[\d,.]+/);
      if (!match) return;
      const target = Number(match[0].replaceAll(',', ''));
      if (!Number.isFinite(target)) return;
      const prefix = original.slice(0, match.index);
      const suffix = original.slice((match.index || 0) + match[0].length);
      const decimals = (match[0].split('.')[1] || '').length;
      counter.textContent = `${prefix}0${suffix}`;
      const observer = new IntersectionObserver((entries) => {
        if (!entries[0].isIntersecting) return;
        const started = performance.now();
        const draw = (now) => {
          const progress = Math.min((now - started) / 1100, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const value = (target * eased).toFixed(decimals);
          counter.textContent = `${prefix}${Number(value).toLocaleString()}${suffix}`;
          if (progress < 1) requestAnimationFrame(draw);
        };
        requestAnimationFrame(draw);
        observer.disconnect();
      }, { threshold: .6 });
      observer.observe(counter);
    });
  }

  const toast = document.querySelector('.toast-stack');
  if (toast) window.setTimeout(() => toast.remove(), 5000);

  if (window.location.search.includes('sent=1')) {
    window.history.replaceState({}, '', `${window.location.pathname}#contact`);
  }
})();
