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

  // ==========================================================================
  // Photo Gallery Slideshow
  // ==========================================================================
  function initGallery() {
    const slidesContainer = document.getElementById('slidesContainer');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (!slidesContainer || !prevBtn || !nextBtn) return;
    
    // Prevent double-binding
    if (slidesContainer.dataset.bound === '1') return;
    slidesContainer.dataset.bound = '1';
    
    let currentIndex = 0;
    const slides = slidesContainer.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let autoSlideInterval;

    function goToSlide(index) {
      slides.forEach((slide, i) => {
        slide.classList.remove('active', 'prev');
        
        if (i === index) {
          slide.classList.add('active');
        } else if (i < index) {
          slide.classList.add('prev');
        }
      });
      currentIndex = index;
    }

    function nextSlide() {
      const nextIndex = (currentIndex + 1) % totalSlides;
      goToSlide(nextIndex);
    }

    function prevSlide() {
      const prevIndex = (currentIndex - 1 + totalSlides) % totalSlides;
      goToSlide(prevIndex);
    }

    function startAutoSlide() {
      autoSlideInterval = setInterval(nextSlide, 3000);
    }

    function resetAutoSlide() {
      clearInterval(autoSlideInterval);
      startAutoSlide();
    }

    // Event listeners
    nextBtn.addEventListener('click', () => {
      nextSlide();
      resetAutoSlide();
    });

    prevBtn.addEventListener('click', () => {
      prevSlide();
      resetAutoSlide();
    });

    // Start auto-sliding
    startAutoSlide();
  }

  initGallery();
  // Re-init gallery on HTMX content swaps
  document.body.addEventListener('htmx:afterSwap', initGallery);

  // ==========================================================================
  // 3D Tilt Effect
  // ==========================================================================
  function init3DTilt() {
    const card = document.getElementById('tiltCard');
    if (!card) return;

    // Prevent double-binding
    if (card.dataset.tiltBound === '1') return;
    card.dataset.tiltBound = '1';

    const container = card.parentElement; // The container with perspective

    container.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      // Calculate rotation (max 15 degrees)
      // Reverse signs for "follow mouse" effect
      const rotateX = ((y - centerY) / centerY) * 15; 
      const rotateY = ((x - centerX) / centerX) * -15;

      card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    container.addEventListener('mouseleave', () => {
      card.style.transform = 'rotateX(0) rotateY(0)';
    });
  }

  init3DTilt();
  document.body.addEventListener('htmx:afterSwap', init3DTilt);
});
