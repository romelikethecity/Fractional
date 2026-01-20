#!/usr/bin/env python3
"""
Generate homepage for Fractional Pulse.
Creates site/index.html with market stats, featured jobs, and role categories.
"""

import os
import sys
from datetime import datetime

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import SITE_NAME, BASE_URL, ROLE_CATEGORIES
from templates import get_full_page

# Paths
SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')

# Sample stats (will be dynamic once job data is loaded)
STATS = {
    'total_jobs': 247,
    'avg_salary': '$185K',
    'remote_pct': '68%',
    'companies': 142,
}

# Sample featured jobs (will be dynamic once job data is loaded)
FEATURED_JOBS = [
    {
        'company': 'TechScale Ventures',
        'title': 'Fractional CFO',
        'salary': '$15-20K/mo',
        'location': 'Remote',
        'hours': '20 hrs/week',
        'stage': 'Series A-B',
        'is_remote': True,
    },
    {
        'company': 'Growth Partners LLC',
        'title': 'Fractional CMO',
        'salary': '$12-18K/mo',
        'location': 'San Francisco, CA',
        'hours': '15 hrs/week',
        'stage': 'Seed',
        'is_remote': False,
    },
    {
        'company': 'DataFlow Systems',
        'title': 'Fractional CTO',
        'salary': '$18-25K/mo',
        'location': 'Remote',
        'hours': '25 hrs/week',
        'stage': 'Series B',
        'is_remote': True,
    },
    {
        'company': 'Horizon Health',
        'title': 'Fractional COO',
        'salary': '$14-20K/mo',
        'location': 'New York, NY',
        'hours': '20 hrs/week',
        'stage': 'Series A',
        'is_remote': False,
    },
]


def generate_hero_section():
    """Generate hero section HTML."""
    return '''
        <section class="hero">
            <div class="hero__badge">
                <span class="hero__badge-dot"></span>
                Updated weekly with new opportunities
            </div>
            <h1 class="hero__title">
                Find Your Next <span class="hero__title-accent">Fractional</span> Executive Role
            </h1>
            <p class="hero__subtitle">
                The leading job board and market intelligence platform for fractional CFOs, CMOs, CTOs, COOs and other C-suite executives.
            </p>
            <div class="hero__buttons">
                <a href="/jobs/" class="btn btn--primary">Browse All Jobs</a>
                <a href="/salaries/" class="btn btn--secondary">Salary Data</a>
            </div>
        </section>
'''


def generate_stats_section(stats):
    """Generate stats section HTML."""
    return f'''
        <section class="stats">
            <div class="stats__inner">
                <div class="stat">
                    <div class="stat__value">{stats['total_jobs']}</div>
                    <div class="stat__label">Open Positions</div>
                </div>
                <div class="stat">
                    <div class="stat__value">{stats['avg_salary']}</div>
                    <div class="stat__label">Avg. Annual Equivalent</div>
                </div>
                <div class="stat">
                    <div class="stat__value">{stats['remote_pct']}</div>
                    <div class="stat__label">Remote Friendly</div>
                </div>
                <div class="stat">
                    <div class="stat__value">{stats['companies']}</div>
                    <div class="stat__label">Companies Hiring</div>
                </div>
            </div>
        </section>
'''


def generate_roles_section(role_categories):
    """Generate browse by role section HTML."""
    role_cards = ""
    for role in role_categories:
        # Placeholder job counts - will be dynamic
        job_count = {
            'cfo': 64, 'cmo': 52, 'cto': 48, 'coo': 38,
            'chro': 21, 'cro': 18, 'cpo': 12, 'other': 24
        }.get(role['id'], 0)

        role_cards += f'''
                <a href="/jobs/?role={role['id']}" class="card role-card">
                    <div class="role-card__icon">{role['icon']}</div>
                    <div class="role-card__title">{role['title']}</div>
                    <div class="role-card__count">{job_count} jobs</div>
                </a>'''

    return f'''
        <section class="section" style="max-width: 1200px; margin: 0 auto;">
            <div class="section__header">
                <h2 class="section__title">Browse by Role</h2>
                <p class="section__subtitle">Find fractional opportunities by executive function</p>
            </div>
            <div class="roles-grid">
{role_cards}
            </div>
        </section>
'''


def generate_featured_jobs_section(jobs):
    """Generate featured jobs section HTML."""
    job_cards = ""
    for job in jobs:
        remote_class = 'job-card__tag--remote' if job['is_remote'] else ''
        location_text = 'Remote' if job['is_remote'] else job['location']

        job_cards += f'''
                <div class="card job-card">
                    <div class="job-card__header">
                        <div>
                            <div class="job-card__company">{job['company']}</div>
                            <div class="job-card__title">{job['title']}</div>
                        </div>
                        <div class="job-card__salary">{job['salary']}</div>
                    </div>
                    <div class="job-card__meta">
                        <span class="job-card__tag {remote_class}">{location_text}</span>
                        <span class="job-card__tag">{job['hours']}</span>
                        <span class="job-card__tag">{job['stage']}</span>
                    </div>
                </div>'''

    return f'''
        <section class="section" style="max-width: 1200px; margin: 0 auto;">
            <div class="section__header">
                <h2 class="section__title">Featured Opportunities</h2>
                <p class="section__subtitle">Hand-picked fractional executive positions</p>
            </div>
            <div class="jobs-grid">
{job_cards}
            </div>
        </section>
'''


def generate_cta_section():
    """Generate newsletter CTA section HTML."""
    return '''
        <div class="cta" style="margin-left: var(--space-lg); margin-right: var(--space-lg);">
            <h2 class="cta__title">Get Weekly Fractional Opportunities</h2>
            <p class="cta__text">Join 2,500+ fractional executives receiving curated job listings and market insights.</p>
            <a href="/newsletter/" class="btn btn--primary">Subscribe to Newsletter</a>
        </div>
'''


def generate_homepage():
    """Generate the complete homepage."""
    print("=" * 70)
    print("  FRACTIONAL PULSE - GENERATING HOMEPAGE")
    print("=" * 70)

    # Build body content
    body_content = (
        generate_hero_section() +
        generate_stats_section(STATS) +
        generate_roles_section(ROLE_CATEGORIES) +
        generate_featured_jobs_section(FEATURED_JOBS) +
        generate_cta_section()
    )

    # Generate full page
    html = get_full_page(
        title="Fractional Executive Jobs & Salary Data",
        description="Find fractional CFO, CMO, CTO, COO and other C-suite executive opportunities. Browse 247+ jobs with salary data and market insights.",
        body_content=body_content,
        canonical_path="/"
    )

    # Ensure output directory exists
    os.makedirs(SITE_DIR, exist_ok=True)

    # Write homepage
    output_path = os.path.join(SITE_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✓ Homepage generated: {output_path}")
    print(f"  - Stats: {STATS['total_jobs']} jobs, {STATS['avg_salary']} avg salary")
    print(f"  - Featured jobs: {len(FEATURED_JOBS)}")
    print(f"  - Role categories: {len(ROLE_CATEGORIES)}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    generate_homepage()
