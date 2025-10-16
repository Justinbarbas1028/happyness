# Centralized Theme System Documentation

## Overview
The HappyNess Project uses a centralized theme system with support for light and dark modes. The theme is built using CSS custom properties (CSS variables) for easy maintenance and consistency across the entire application.

## Features

### ✅ **Light Mode (Default)**
- Soft pastel gradient background (beige → mint → teal)
- Dark text on light backgrounds
- High contrast for accessibility
- Professional and inviting appearance

### ✅ **Dark Mode**
- Deep blue/gray gradient background
- Light text on dark backgrounds
- Reduced eye strain in low-light conditions
- Modern and sleek appearance

### ✅ **Persistent Theme**
- User's theme preference saved in localStorage
- Theme persists across page reloads and sessions
- No flash of unstyled content (FOUC)

### ✅ **Smooth Transitions**
- All theme changes animate smoothly
- 0.3s transition duration
- Professional user experience

## File Structure

```
static/
├── css/
│   ├── theme.css       # Centralized theme system
│   └── style.css       # Legacy/additional styles
└── js/
    ├── theme.js        # Theme toggle functionality
    └── app.js          # Other app scripts
```

## Color Palette

### Light Mode
- **Primary Background**: `#f5f5f5` (light gray)
- **Secondary Background**: `#ffffff` (white)
- **Gradient**: `#e8d5c4` → `#c8e3d4` → `#a8d5c8`
- **Primary Text**: `#1a1f2e` (dark blue-gray)
- **Secondary Text**: `#4a5568` (medium gray)
- **Brand Primary**: `#7cacf8` (blue)
- **Brand Secondary**: `#39b54a` (green)

### Dark Mode
- **Primary Background**: `#0b0f17` (very dark blue)
- **Secondary Background**: `#1a1f2e` (dark blue-gray)
- **Gradient**: `#0d1322` → `#1a2332` → `#1e2d3d`
- **Primary Text**: `#e6edf3` (light blue-white)
- **Secondary Text**: `#9fb2c8` (light gray-blue)
- **Brand Primary**: `#7cacf8` (blue - same)
- **Brand Secondary**: `#39b54a` (green - same)

## CSS Variables

### Using Theme Variables in CSS
```css
.my-component {
  background-color: var(--card-bg);
  color: var(--text-primary);
  border: 1px solid var(--card-border);
}
```

### Available Variables

#### Colors
- `--bg-primary` - Main background color
- `--bg-secondary` - Secondary background color
- `--text-primary` - Main text color
- `--text-secondary` - Secondary text color
- `--text-muted` - Muted/disabled text
- `--brand-primary` - Primary brand color (blue)
- `--brand-secondary` - Secondary brand color (green)
- `--brand-accent` - Accent color

#### Components
- `--card-bg` - Card background
- `--card-border` - Card border
- `--card-shadow` - Card shadow
- `--input-bg` - Form input background
- `--input-border` - Form input border
- `--input-focus` - Form input focus color
- `--button-primary` - Primary button color
- `--button-secondary` - Secondary button color

#### Status Colors
- `--success` - Success messages/states
- `--error` - Error messages/states
- `--warning` - Warning messages/states
- `--info` - Info messages/states

#### Layout
- `--header-bg` - Header background
- `--header-border` - Header border
- `--footer-bg` - Footer background
- `--overlay` - Modal overlay

#### Shadows
- `--shadow-sm` - Small shadow
- `--shadow-md` - Medium shadow
- `--shadow-lg` - Large shadow
- `--shadow-xl` - Extra large shadow

## Using Theme Variables in HTML

### Inline Styles
```html
<div style="background-color: var(--card-bg); color: var(--text-primary);">
  Content here
</div>
```

### Pre-built Classes
```html
<!-- Text Colors -->
<p class="text-primary">Primary text</p>
<p class="text-secondary">Secondary text</p>
<p class="text-muted">Muted text</p>
<p class="text-brand">Brand colored text</p>

<!-- Buttons -->
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-secondary">Secondary Button</button>
<button class="btn btn-outline">Outline Button</button>

<!-- Cards -->
<div class="card">Card content</div>

<!-- Alerts -->
<div class="alert alert-success">Success message</div>
<div class="alert alert-error">Error message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-info">Info message</div>
```

## Theme Toggle

### Button Location
- Fixed position: bottom-right corner
- Floats above content (z-index: 1000)
- Always accessible on all pages

### JavaScript API
```javascript
// Toggle theme programmatically
window.toggleTheme();

// Get current theme
localStorage.getItem('happyness-theme'); // Returns 'light' or 'dark'
```

### Manual Theme Setting
```javascript
// Set theme directly
document.documentElement.setAttribute('data-theme', 'dark');
localStorage.setItem('happyness-theme', 'dark');
```

## Adding Theme Support to New Components

### 1. Use CSS Variables
```css
.my-new-component {
  background-color: var(--card-bg);
  color: var(--text-primary);
  border: 1px solid var(--card-border);
  box-shadow: var(--shadow-md);
}

.my-new-component:hover {
  background-color: var(--button-primary-hover);
}
```

### 2. Use Pre-built Classes
```html
<div class="card">
  <h2 class="text-primary">Title</h2>
  <p class="text-secondary">Description</p>
  <button class="btn btn-primary">Action</button>
</div>
```

### 3. Test Both Modes
Always test your components in both light and dark modes to ensure proper contrast and readability.

## Best Practices

### ✅ DO:
- Use CSS variables for all colors
- Use pre-built classes when available
- Test components in both light and dark modes
- Ensure adequate contrast ratios (WCAG AA)
- Use semantic color names (success, error, etc.)

### ❌ DON'T:
- Hardcode colors (e.g., `color: #ffffff`)
- Use opacity for text (use muted colors instead)
- Assume background colors
- Override theme variables without good reason

## Accessibility

### Contrast Ratios
- **Light Mode**: Minimum 4.5:1 for normal text
- **Dark Mode**: Minimum 4.5:1 for normal text
- **Focus States**: Clear visual indicators
- **Color Blind Safe**: Don't rely on color alone

### Keyboard Navigation
- Theme toggle accessible via keyboard
- Tab navigation supported
- Focus states clearly visible

## Browser Support
- ✅ Chrome/Edge 88+
- ✅ Firefox 85+
- ✅ Safari 14+
- ✅ Opera 74+

## Performance
- **CSS Variables**: Faster than class switching
- **localStorage**: Minimal overhead
- **No FOUC**: Theme loaded before render
- **Smooth Transitions**: Hardware accelerated

## Customization

### Changing Colors
Edit `static/css/theme.css` and update the CSS variables:

```css
:root {
  --brand-primary: #your-color;
  --brand-secondary: #your-color;
}

[data-theme="dark"] {
  --brand-primary: #your-dark-color;
  --brand-secondary: #your-dark-color;
}
```

### Adding New Variables
```css
:root {
  --my-custom-color: #123456;
}

[data-theme="dark"] {
  --my-custom-color: #654321;
}
```

### Adjusting Transition Speed
```css
html, body {
  transition: background-color 0.5s ease, color 0.5s ease;
}
```

## Troubleshooting

### Theme Not Persisting
- Check browser localStorage is enabled
- Clear cache and reload

### Colors Not Changing
- Ensure CSS variables are used, not hardcoded colors
- Check for CSS specificity issues

### Flash of Unstyled Content
- Ensure `theme.js` loads in `<head>`
- Check console for JavaScript errors

## Future Enhancements
- [ ] System preference detection (prefers-color-scheme)
- [ ] Additional theme options (high contrast, custom)
- [ ] Theme preview before switching
- [ ] Per-section theme overrides
