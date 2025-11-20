/**
 * Theme Toggle System
 * Handles light/dark mode switching with localStorage persistence
 */

(function() {
  'use strict';

  // Constants
  const THEME_KEY = 'happyness-theme';
  const THEME_DARK = 'dark';
  const THEME_LIGHT = 'light';

  // Get stored theme or default to light
  function getStoredTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    return stored || THEME_LIGHT;
  }

  // Get current theme from document
  function getCurrentTheme() {
    const theme = document.documentElement.getAttribute('data-theme');
    return theme || THEME_LIGHT;
  }

  // Set theme
  function setTheme(theme) {
    if (theme === THEME_DARK) {
      document.documentElement.setAttribute('data-theme', THEME_DARK);
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    
    localStorage.setItem(THEME_KEY, theme);
    updateToggleIcon(theme);
  }

  // Toggle between light and dark
  function toggleTheme() {
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;
    setTheme(newTheme);
  }

  // Update toggle button icon
  function updateToggleIcon(theme) {
    const toggleBtn = document.getElementById('themeToggle');
    if (!toggleBtn) return;

    const sunIcon = toggleBtn.querySelector('.sun-icon');
    const moonIcon = toggleBtn.querySelector('.moon-icon');

    if (!sunIcon || !moonIcon) return;

    if (theme === THEME_DARK) {
      // Dark mode: show sun icon (to switch back to light)
      sunIcon.classList.remove('hidden');
      moonIcon.classList.add('hidden');
    } else {
      // Light mode: show moon icon (to switch to dark)
      sunIcon.classList.add('hidden');
      moonIcon.classList.remove('hidden');
    }
  }

  // Initialize theme logic
  function initTheme() {
    // 1. Set initial theme (idempotent)
    const storedTheme = getStoredTheme();
    setTheme(storedTheme);

    // 2. Attach event listener to toggle button
    // This needs to happen every time the button is re-rendered (e.g. HTMX swap)
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
      // Remove old listener to be safe (though replacing element removes it anyway)
      toggleBtn.removeEventListener('click', handleToggleClick);
      toggleBtn.addEventListener('click', handleToggleClick);
    }
  }

  function handleToggleClick(e) {
    e.preventDefault();
    toggleTheme();
  }

  // Run immediately to prevent flash (if script is in head)
  const storedTheme = localStorage.getItem(THEME_KEY);
  if (storedTheme === THEME_DARK) {
    document.documentElement.setAttribute('data-theme', THEME_DARK);
  }

  // Initialize on load and after HTMX swaps
  if (typeof htmx !== 'undefined') {
    htmx.onLoad(initTheme);
  } else {
    // Fallback if HTMX isn't loaded yet
    document.addEventListener('DOMContentLoaded', initTheme);
  }

  // Expose toggle function globally
  window.toggleTheme = toggleTheme;
  
})();
