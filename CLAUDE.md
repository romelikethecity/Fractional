# Fractional Pulse - Project Guidelines

## Overview
Fractional Pulse (fractionalpulse.com) is a job board and market intelligence platform for fractional executives (CFO, CMO, CTO, COO, CHRO, CPO, CRO, etc.). Built as a static site for GitHub Pages deployment.

## Tech Stack
- **Static Site Generator**: Python scripts in `/scripts/`
- **Hosting**: GitHub Pages
- **Domain**: fractionalpulse.com
- **Analytics**: Google Analytics 4 + Microsoft Clarity

## Directory Structure
```
/Fractional/
├── .github/workflows/     # CI/CD pipeline
├── data/                  # Job CSV files and JSON data
├── scripts/               # Python generators
├── site/                  # Generated static site (output)
├── mockups/               # Design mockups
├── CLAUDE.md              # This file
└── README.md
```

## Design System

### Theme: Dark
Selected dark theme matching other sites in the network (croreport, aimarketpulse).

### Color Palette
```css
/* Backgrounds */
--bg-primary: #0d1b2a;      /* Main background */
--bg-secondary: #081420;    /* Darker sections */
--bg-card: #152535;         /* Card backgrounds */
--bg-card-hover: #1d3045;   /* Card hover state */

/* Brand Colors (from logo) */
--teal: #1a9a8a;            /* Primary accent */
--teal-light: #22b8a5;      /* Hover/highlight */
--teal-dark: #158577;       /* Pressed state */
--teal-glow: rgba(26, 154, 138, 0.2);  /* Glow effect */

/* Text */
--text-primary: #ffffff;
--text-secondary: #94a3b8;
--text-muted: #64748b;

/* Borders */
--border: rgba(255, 255, 255, 0.1);
--border-light: rgba(255, 255, 255, 0.05);

/* Status */
--success: #4ade80;         /* Remote badges, positive */
--warning: #fbbf24;         /* Warnings */
--error: #f87171;           /* Errors, expired */
```

### Typography
- **Display Font**: Space Grotesk (headings, stats, logo)
- **Body Font**: DM Sans (paragraphs, UI text)
- Google Fonts with preconnect for performance

### Spacing Scale
```css
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
--space-3xl: 4rem;     /* 64px */
```

### Border Radius
```css
--radius-sm: 6px;
--radius-md: 10px;
--radius-lg: 16px;
--radius-full: 9999px;
```

## URL Patterns

| Page Type | URL Pattern | Example |
|-----------|-------------|---------|
| Homepage | `/` | fractionalpulse.com |
| Job Board | `/jobs/` | /jobs/ |
| Individual Job | `/jobs/{company}-{role}-{hash}/` | /jobs/acme-fractional-cfo-a1b2c3/ |
| Salary Hub | `/salaries/` | /salaries/ |
| Salary by Role | `/salaries/fractional-{role}/` | /salaries/fractional-cfo/ |
| Company Profile | `/companies/{slug}/` | /companies/acme-corp/ |
| Insights | `/insights/` | /insights/ |
| About | `/about/` | /about/ |

## Fractional Executive Roles

### Primary Roles (highest volume)
- Fractional CFO (Chief Financial Officer)
- Fractional CMO (Chief Marketing Officer)
- Fractional CTO (Chief Technology Officer)
- Fractional COO (Chief Operations Officer)

### Secondary Roles
- Fractional CHRO (Chief Human Resources Officer)
- Fractional CPO (Chief Product Officer)
- Fractional CRO (Chief Revenue Officer)
- Fractional CSO (Chief Strategy Officer)
- Fractional CIO (Chief Information Officer)
- Fractional CISO (Chief Information Security Officer)

### VP Level
- Fractional VP Sales
- Fractional VP Marketing
- Fractional VP Engineering
- Fractional VP Finance

## SEO Requirements

### Meta Tags (every page)
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Page Title} | Fractional Pulse</title>
<meta name="description" content="{150-160 char description}">
<link rel="canonical" href="https://fractionalpulse.com/{path}/">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://fractionalpulse.com/{path}/">
<meta property="og:title" content="{Title}">
<meta property="og:description" content="{Description}">
<meta property="og:site_name" content="Fractional Pulse">
<meta property="og:image" content="https://fractionalpulse.com/assets/social-preview.png">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{Title}">
<meta name="twitter:description" content="{Description}">
<meta name="twitter:image" content="https://fractionalpulse.com/assets/social-preview.png">
```

### Structured Data (JSON-LD)
- **Homepage**: Organization + WebSite schemas
- **Job Pages**: JobPosting + BreadcrumbList schemas
- **Salary Pages**: Dataset + FAQPage + BreadcrumbList schemas
- **Company Pages**: Organization + BreadcrumbList schemas

### Sitemap Strategy
- `sitemap_index.xml` - Index pointing to category sitemaps
- `sitemaps/sitemap-main.xml` - Homepage, about, core pages
- `sitemaps/sitemap-jobs.xml` - Individual job pages
- `sitemaps/sitemap-salaries.xml` - Salary benchmark pages
- `sitemaps/sitemap-companies.xml` - Company profiles

## Job Data Schema (CSV)

Required columns:
```
id,title,company,location,salary_min,salary_max,salary_type,job_category,
experience_level,remote_type,job_url,posted_date,engagement_type,hours_per_week,
company_size,industry,description
```

### Key Fields
- `job_category`: fractional-cfo, fractional-cmo, fractional-cto, etc.
- `remote_type`: remote, hybrid, onsite
- `engagement_type`: retainer, project, interim
- `hours_per_week`: 10-20, 20-30, 30+
- `salary_type`: monthly, hourly, annual

## Scripts

### Core Scripts
- `nav_config.py` - Navigation structure (single source of truth)
- `templates.py` - HTML/CSS templates and utilities
- `seo_core.py` - Schema generators, SEO utilities
- `tracking_config.py` - Analytics IDs

### Generators
- `generate_homepage.py` - Homepage with stats and featured jobs
- `generate_job_board.py` - Main job listing page
- `generate_job_pages.py` - Individual job pages
- `generate_salary_pages.py` - Salary benchmark pages
- `generate_company_pages.py` - Company profile pages
- `generate_sitemap.py` - XML sitemaps

## Running Generators

From project root:
```bash
cd /Users/rome/Documents/Fractional
python scripts/generate_homepage.py
python scripts/generate_job_board.py
python scripts/generate_job_pages.py
# etc.
```

## Stale Job Handling

When a job is no longer in the current data:
1. Add `<meta name="robots" content="noindex, follow">`
2. Show "Position Filled" badge
3. Display similar active opportunities
4. Keep page accessible for users landing from old links

## Writing Style

- Professional but approachable
- Data-driven (use specific numbers)
- No jargon or buzzwords
- Clear value proposition
- Action-oriented CTAs

## Deployment

1. Push changes to GitHub
2. GitHub Actions runs build scripts
3. Generated `site/` deployed to GitHub Pages
4. Custom domain: fractionalpulse.com

## Data Pipeline

### Scraper Location
Job scrapers are located at: `/Users/rome/Documents/projects/scrapers/fractional`

### Data Sources
1. **Indeed** - Via JobSpy library with fractional executive search terms
2. **FractionalJobs.io** - Direct scraping of specialized job board
3. **The Free Agent** - PE/VC portfolio company fractional roles

### Export Script
Run from Fractional directory:
```bash
# Export from CSV (for initial data)
python3 scripts/export_jobs.py --csv /path/to/scraped_jobs.csv

# Export from database (after scraper populates it)
python3 scripts/export_jobs.py
```

### Output Files
- `data/jobs.json` - All job listings with metadata
- `data/market_stats.json` - Aggregate statistics for homepage

### Job Data Structure (jobs.json)
```json
{
  "last_updated": "2026-01-20",
  "total_jobs": 28,
  "stats": {
    "by_role_type": {"cfo": 12, "cmo": 3, "cto": 4},
    "by_location_type": {"remote": 16, "onsite": 12},
    "with_salary": 15,
    "c_level": 20
  },
  "jobs": [
    {
      "job_id": "in-7edf0c0c3e04",
      "slug": "company-title-hash",
      "title": "Fractional CFO",
      "company": "Company Name",
      "location": "Remote, US",
      "location_type": "remote",
      "is_remote": true,
      "compensation": {
        "type": "hourly",
        "display": "$150-200/hr",
        "min": 150,
        "max": 200,
        "hourly_min": 150,
        "hourly_max": 200
      },
      "has_salary": true,
      "hours": {
        "min": 10,
        "max": 20,
        "display": "10-20 hrs/week"
      },
      "role_type": "cfo",
      "function_category": "finance",
      "is_c_level": true,
      "date_posted": "2026-01-15",
      "description": "...",
      "source": "indeed",
      "source_url": "https://..."
    }
  ]
}
```

## Current Progress

### Completed
- [x] Directory structure created
- [x] Design system (dark theme matching logo colors)
- [x] `scripts/nav_config.py` - Navigation configuration
- [x] `scripts/templates.py` - CSS/HTML templates
- [x] `scripts/tracking_config.py` - Analytics placeholders
- [x] `scripts/generate_homepage.py` - Homepage generator
- [x] `scripts/export_jobs.py` - Job data export utility
- [x] `site/index.html` - Generated homepage
- [x] `site/about/index.html` - About page
- [x] `site/robots.txt` and `site/CNAME`
- [x] `data/jobs.json` - 28 fractional exec jobs exported
- [x] `data/market_stats.json` - Market statistics

### Scraper Improvements Completed
- [x] Centralized `job_to_db_dict` functions in `utils/parsers.py`
- [x] Structured logging in `utils/logger.py`
- [x] Safe parsing methods in `fractionaljobs_scraper.py`
- [x] New `thefreeagent_scraper.py` scraper
- [x] Updated `main.py` with 4-source daily workflow

### Pending
- [ ] `scripts/generate_job_board.py` - Job listing page
- [ ] `scripts/generate_job_pages.py` - Individual job pages
- [ ] `scripts/generate_salary_pages.py` - Salary benchmarks
- [ ] `scripts/generate_company_pages.py` - Company profiles
- [ ] `scripts/generate_sitemap.py` - XML sitemaps
- [ ] `.github/workflows/build-site.yml` - CI/CD pipeline
- [ ] GitHub Pages deployment setup

## Reference Sites
Pattern sources for SEO and content structure:
- `/Users/rome/Documents/croreport` - Job board patterns
- `/Users/rome/Documents/aimarketpulse` - Job data structure, templates
- `/Users/rome/Documents/projects/verum-website` - GitHub Pages deployment
