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
    console.log('Setting theme to:', theme);
    
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
    console.log('Toggle theme clicked');
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;
    console.log('Switching from', currentTheme, 'to', newTheme);
    setTheme(newTheme);
  }

  // Update toggle button icon
  function updateToggleIcon(theme) {
    const toggleBtn = document.getElementById('themeToggle');
    if (!toggleBtn) {
      console.warn('Theme toggle button not found');
      return;
    }

    const sunIcon = toggleBtn.querySelector('.sun-icon');
    const moonIcon = toggleBtn.querySelector('.moon-icon');

    if (!sunIcon || !moonIcon) {
      console.warn('Theme icons not found');
      return;
    }

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

  // Initialize theme on page load
  function initTheme() {
    console.log('Initializing theme system...');
    
    // Get stored theme or default to light
    const storedTheme = getStoredTheme();
    console.log('Stored theme:', storedTheme);
    
    // Set the theme
    setTheme(storedTheme);

    // Add click handler to toggle button
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
      console.log('Adding click handler to theme toggle button');
      toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        toggleTheme();
      });
    } else {
      console.warn('Theme toggle button not found during initialization');
    }
  }

  // Run immediately to prevent flash
  const storedTheme = localStorage.getItem(THEME_KEY);
  if (storedTheme === THEME_DARK) {
    document.documentElement.setAttribute('data-theme', THEME_DARK);
  }

  // Run on DOM load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }

  // Expose toggle function globally
  window.toggleTheme = toggleTheme;
  
  console.log('Theme system loaded');
})();
