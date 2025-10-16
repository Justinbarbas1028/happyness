document.addEventListener('DOMContentLoaded', () => {
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  const btn = document.getElementById('helloBtn');
  const msg = document.getElementById('helloMsg');
  if (btn && msg) {
    btn.addEventListener('click', () => {
      msg.textContent = 'Hello from static JS!';
      msg.classList.remove('hidden');
    });
  }

  // Mobile menu toggle (robust init with touch support)
  function initMobileMenu() {
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (!mobileBtn || !mobileMenu) return;

    // Prevent double-binding
    if (mobileBtn.dataset.bound === '1') return;
    mobileBtn.dataset.bound = '1';

    // Toggle function
    const toggleMenu = (e) => {
      e.preventDefault();
      e.stopPropagation();
      const isOpen = !mobileMenu.classList.contains('hidden');
      mobileMenu.classList.toggle('hidden');
      mobileBtn.setAttribute('aria-expanded', String(!isOpen));
    };

    // Add both click and touch events for better mobile support
    mobileBtn.addEventListener('click', toggleMenu, { passive: false });
    mobileBtn.addEventListener('touchend', (e) => {
      e.preventDefault();
      toggleMenu(e);
    }, { passive: false });

    // Close when clicking outside
    const closeMenu = (e) => {
      if (!mobileMenu.classList.contains('hidden')) {
        const clickInside = mobileMenu.contains(e.target) || mobileBtn.contains(e.target);
        if (!clickInside) {
          mobileMenu.classList.add('hidden');
          mobileBtn.setAttribute('aria-expanded', 'false');
        }
      }
    };
    
    document.addEventListener('click', closeMenu);
    document.addEventListener('touchend', closeMenu);

    // Close after navigation clicks (HTMX boost or normal links)
    mobileMenu.addEventListener('click', (e) => {
      const target = e.target.closest('a');
      if (target) {
        mobileMenu.classList.add('hidden');
        mobileBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  initMobileMenu();

  // Re-init menu on HTMX content swaps
  document.body.addEventListener('htmx:afterSwap', initMobileMenu);

  // Safety: ensure body is scrollable and no modal overlay is visible
  function resetInteractionLocks() {
    // Clear any leftover overflow lock
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    // Hide logout modal if it somehow persisted
    const modal = document.getElementById('logoutModal');
    if (modal && !modal.classList.contains('hidden')) {
      modal.classList.add('hidden');
    }
  }

  // Run on load
  resetInteractionLocks();
  // And after HTMX swaps
  document.body.addEventListener('htmx:afterSwap', resetInteractionLocks);
});
