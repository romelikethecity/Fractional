#!/usr/bin/env python3
"""
Shared HTML/CSS templates for Fractional Pulse.
Contains all styling and reusable HTML components.
"""

from nav_config import (
    SITE_NAME, BASE_URL, LOGO_TEXT, NAV_ITEMS, HEADER_CTA,
    FOOTER_COLUMNS, COPYRIGHT_TEXT
)

# =============================================================================
# CSS VARIABLES
# =============================================================================

CSS_VARIABLES = """
:root {
    /* Backgrounds */
    --bg-primary: #0d1b2a;
    --bg-secondary: #081420;
    --bg-card: #152535;
    --bg-card-hover: #1d3045;

    /* Brand Colors (from logo) */
    --teal: #1a9a8a;
    --teal-light: #22b8a5;
    --teal-dark: #158577;
    --teal-glow: rgba(26, 154, 138, 0.2);

    /* Text */
    --text-primary: #ffffff;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;

    /* Borders */
    --border: rgba(255, 255, 255, 0.1);
    --border-light: rgba(255, 255, 255, 0.05);

    /* Status */
    --success: #4ade80;
    --warning: #fbbf24;
    --error: #f87171;

    /* Spacing */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;
    --space-3xl: 4rem;

    /* Border Radius */
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-full: 9999px;

    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 0 20px var(--teal-glow);

    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-base: 250ms ease;
}
"""

# =============================================================================
# CSS RESET & BASE
# =============================================================================

CSS_BASE = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
}

a {
    color: inherit;
    text-decoration: none;
}

img {
    max-width: 100%;
    height: auto;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif;
    line-height: 1.2;
}
"""

# =============================================================================
# CSS LAYOUT
# =============================================================================

CSS_LAYOUT = """
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}

.container--narrow {
    max-width: 800px;
}

.section {
    padding: var(--space-3xl) var(--space-lg);
}

.section__header {
    text-align: center;
    margin-bottom: var(--space-2xl);
}

.section__title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: var(--space-sm);
}

.section__subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
}
"""

# =============================================================================
# CSS HEADER
# =============================================================================

CSS_HEADER = """
.header {
    background: rgba(13, 27, 42, 0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
}

.header__inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
    height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.logo {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.logo__icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--teal), var(--teal-dark));
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 14px;
    box-shadow: var(--shadow-glow);
}

.logo__text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

.nav {
    display: flex;
    align-items: center;
    gap: var(--space-xl);
}

.nav__link {
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.95rem;
    transition: color var(--transition-fast);
}

.nav__link:hover {
    color: var(--teal-light);
}

/* Mobile menu button */
.menu-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: var(--space-sm);
}

.menu-toggle span {
    display: block;
    width: 24px;
    height: 2px;
    background: var(--text-primary);
    margin: 5px 0;
    transition: var(--transition-fast);
}

/* Mobile nav */
.mobile-nav {
    display: none;
    position: fixed;
    top: 0;
    right: -100%;
    width: 280px;
    height: 100vh;
    background: var(--bg-card);
    z-index: 200;
    padding: var(--space-xl);
    transition: right var(--transition-base);
}

.mobile-nav.active {
    right: 0;
}

.mobile-nav__overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 150;
    opacity: 0;
    transition: opacity var(--transition-base);
}

.mobile-nav__overlay.active {
    display: block;
    opacity: 1;
}

.mobile-nav__close {
    position: absolute;
    top: var(--space-lg);
    right: var(--space-lg);
    background: none;
    border: none;
    color: var(--text-primary);
    font-size: 1.5rem;
    cursor: pointer;
}

.mobile-nav__links {
    list-style: none;
    margin-top: var(--space-3xl);
}

.mobile-nav__link {
    display: block;
    padding: var(--space-md) 0;
    color: var(--text-primary);
    font-size: 1.1rem;
    font-weight: 500;
    border-bottom: 1px solid var(--border);
}

@media (max-width: 768px) {
    .nav {
        display: none;
    }

    .menu-toggle {
        display: block;
    }

    .mobile-nav {
        display: block;
    }
}
"""

# =============================================================================
# CSS BUTTONS
# =============================================================================

CSS_BUTTONS = """
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    font-size: 0.95rem;
    transition: all var(--transition-fast);
    cursor: pointer;
    border: none;
    text-decoration: none;
}

.btn--primary {
    background: var(--teal);
    color: white;
    box-shadow: var(--shadow-glow);
}

.btn--primary:hover {
    background: var(--teal-light);
    transform: translateY(-1px);
    box-shadow: 0 0 30px var(--teal-glow);
}

.btn--secondary {
    background: transparent;
    color: var(--teal-light);
    border: 2px solid var(--teal);
}

.btn--secondary:hover {
    background: var(--teal);
    color: white;
}

.btn--sm {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
}

.btn--lg {
    padding: 1rem 2rem;
    font-size: 1rem;
}
"""

# =============================================================================
# CSS CARDS
# =============================================================================

CSS_CARDS = """
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    transition: all var(--transition-base);
}

.card:hover {
    border-color: var(--teal);
    box-shadow: var(--shadow-glow);
}

/* Role cards */
.role-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    text-decoration: none;
}

.role-card:hover {
    transform: translateY(-2px);
}

.role-card__icon {
    width: 48px;
    height: 48px;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--space-md);
    font-size: 1.5rem;
    color: var(--teal-light);
}

.role-card__title {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--space-xs);
}

.role-card__count {
    font-size: 0.875rem;
    color: var(--text-muted);
}

/* Job cards */
.job-card__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-md);
}

.job-card__company {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-xs);
}

.job-card__title {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 1.1rem;
}

.job-card__salary {
    background: var(--bg-secondary);
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--teal-light);
    white-space: nowrap;
}

.job-card__meta {
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
}

.job-card__tag {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    font-size: 0.8rem;
    color: var(--text-muted);
}

.job-card__tag--remote {
    color: var(--success);
    font-weight: 500;
}
"""

# =============================================================================
# CSS HERO
# =============================================================================

CSS_HERO = """
.hero {
    padding: 10rem var(--space-lg) var(--space-3xl);
    text-align: center;
    max-width: 900px;
    margin: 0 auto;
    position: relative;
}

.hero::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--teal-glow) 0%, transparent 70%);
    pointer-events: none;
    z-index: -1;
}

.hero__badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-sm);
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-full);
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-xl);
}

.hero__badge-dot {
    width: 8px;
    height: 8px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.hero__title {
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: var(--space-lg);
}

.hero__title-accent {
    color: var(--teal-light);
}

.hero__subtitle {
    font-size: 1.25rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-2xl);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.hero__buttons {
    display: flex;
    gap: var(--space-md);
    justify-content: center;
    flex-wrap: wrap;
}

@media (max-width: 768px) {
    .hero {
        padding-top: 8rem;
    }

    .hero__title {
        font-size: 2.5rem;
    }
}
"""

# =============================================================================
# CSS STATS
# =============================================================================

CSS_STATS = """
.stats {
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: var(--space-2xl) var(--space-lg);
}

.stats__inner {
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-xl);
}

.stat {
    text-align: center;
}

.stat__value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--teal-light);
    line-height: 1;
    margin-bottom: var(--space-xs);
}

.stat__label {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}

@media (max-width: 768px) {
    .stats__inner {
        grid-template-columns: repeat(2, 1fr);
    }
}
"""

# =============================================================================
# CSS GRIDS
# =============================================================================

CSS_GRIDS = """
.roles-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
}

.jobs-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-lg);
}

@media (max-width: 768px) {
    .roles-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .jobs-grid {
        grid-template-columns: 1fr;
    }
}
"""

# =============================================================================
# CSS CTA
# =============================================================================

CSS_CTA = """
.cta {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-3xl);
    text-align: center;
    margin: var(--space-2xl) auto;
    max-width: 1200px;
    position: relative;
    overflow: hidden;
}

.cta::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--teal), transparent);
}

.cta__title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--space-md);
}

.cta__text {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-bottom: var(--space-xl);
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}
"""

# =============================================================================
# CSS FOOTER
# =============================================================================

CSS_FOOTER = """
.footer {
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    padding: var(--space-3xl) var(--space-lg) var(--space-xl);
}

.footer__inner {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: var(--space-2xl);
}

.footer__brand {
    max-width: 280px;
}

.footer__logo {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
}

.footer__logo-icon {
    width: 36px;
    height: 36px;
    background: var(--teal);
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 12px;
}

.footer__logo-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
}

.footer__desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.7;
}

.footer__col-title {
    font-weight: 600;
    margin-bottom: var(--space-md);
    font-size: 0.95rem;
}

.footer__links {
    list-style: none;
}

.footer__link {
    color: var(--text-secondary);
    font-size: 0.9rem;
    display: block;
    padding: var(--space-xs) 0;
    transition: color var(--transition-fast);
}

.footer__link:hover {
    color: var(--teal-light);
}

.footer__bottom {
    max-width: 1200px;
    margin: var(--space-2xl) auto 0;
    padding-top: var(--space-xl);
    border-top: 1px solid var(--border);
    font-size: 0.875rem;
    color: var(--text-muted);
}

@media (max-width: 768px) {
    .footer__inner {
        grid-template-columns: 1fr 1fr;
    }

    .footer__brand {
        grid-column: 1 / -1;
    }
}
"""

# =============================================================================
# COMBINED CSS
# =============================================================================

def get_all_css():
    """Return all CSS combined."""
    return (
        CSS_VARIABLES +
        CSS_BASE +
        CSS_LAYOUT +
        CSS_HEADER +
        CSS_BUTTONS +
        CSS_CARDS +
        CSS_HERO +
        CSS_STATS +
        CSS_GRIDS +
        CSS_CTA +
        CSS_FOOTER
    )

# =============================================================================
# HTML COMPONENTS
# =============================================================================

def get_html_head(title, description, canonical_path="/", extra_head=""):
    """Generate HTML head section with SEO meta tags."""
    canonical_url = f"{BASE_URL}{canonical_path}"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {SITE_NAME}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title} | {SITE_NAME}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{BASE_URL}/assets/social-preview.png">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} | {SITE_NAME}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{BASE_URL}/assets/social-preview.png">

    <!-- Favicon -->
    <link rel="icon" href="/assets/logo.png" type="image/png">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">

    <style>
{get_all_css()}
    </style>
    {extra_head}
</head>'''


def get_header_html():
    """Generate header HTML."""
    nav_links = "\n".join([
        f'                <a href="{item["href"]}" class="nav__link">{item["label"]}</a>'
        for item in NAV_ITEMS
    ])

    mobile_links = "\n".join([
        f'                    <li><a href="{item["href"]}" class="mobile-nav__link">{item["label"]}</a></li>'
        for item in NAV_ITEMS
    ])

    return f'''
    <header class="header">
        <div class="header__inner">
            <a href="/" class="logo">
                <div class="logo__icon">{LOGO_TEXT}</div>
                <span class="logo__text">{SITE_NAME}</span>
            </a>
            <nav class="nav">
{nav_links}
            </nav>
            <a href="{HEADER_CTA["href"]}" class="btn btn--primary">{HEADER_CTA["label"]}</a>
            <button class="menu-toggle" aria-label="Menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>

    <!-- Mobile Navigation -->
    <div class="mobile-nav__overlay"></div>
    <nav class="mobile-nav">
        <button class="mobile-nav__close" aria-label="Close">&times;</button>
        <ul class="mobile-nav__links">
{mobile_links}
        </ul>
    </nav>
'''


def get_footer_html():
    """Generate footer HTML."""
    columns_html = ""
    for col in FOOTER_COLUMNS:
        links = "\n".join([
            f'                    <li><a href="{link["href"]}" class="footer__link">{link["label"]}</a></li>'
            for link in col["links"]
        ])
        columns_html += f'''
            <div class="footer__col">
                <h4 class="footer__col-title">{col["title"]}</h4>
                <ul class="footer__links">
{links}
                </ul>
            </div>'''

    return f'''
    <footer class="footer">
        <div class="footer__inner">
            <div class="footer__brand">
                <div class="footer__logo">
                    <div class="footer__logo-icon">{LOGO_TEXT}</div>
                    <span class="footer__logo-text">{SITE_NAME}</span>
                </div>
                <p class="footer__desc">The leading job board and market intelligence platform for fractional executives.</p>
            </div>
{columns_html}
        </div>
        <div class="footer__bottom">
            {COPYRIGHT_TEXT}
        </div>
    </footer>
'''


def get_mobile_nav_js():
    """Generate mobile navigation JavaScript."""
    return '''
    <script>
    (function() {
        const menuToggle = document.querySelector('.menu-toggle');
        const mobileNav = document.querySelector('.mobile-nav');
        const overlay = document.querySelector('.mobile-nav__overlay');
        const closeBtn = document.querySelector('.mobile-nav__close');
        const mobileLinks = document.querySelectorAll('.mobile-nav__link');

        function openMenu() {
            mobileNav.classList.add('active');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeMenu() {
            mobileNav.classList.remove('active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        if (menuToggle) menuToggle.addEventListener('click', openMenu);
        if (closeBtn) closeBtn.addEventListener('click', closeMenu);
        if (overlay) overlay.addEventListener('click', closeMenu);

        mobileLinks.forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    })();
    </script>
'''


def get_full_page(title, description, body_content, canonical_path="/", extra_head=""):
    """Generate a complete HTML page."""
    return f'''{get_html_head(title, description, canonical_path, extra_head)}
<body>
{get_header_html()}
    <main>
{body_content}
    </main>
{get_footer_html()}
{get_mobile_nav_js()}
</body>
</html>'''
