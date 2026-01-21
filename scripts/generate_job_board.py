#!/usr/bin/env python3
"""
Generate the main job board listing page at /jobs/index.html
"""

import json
import os
import sys
import hashlib
import re
from datetime import datetime

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from templates import get_full_page, get_all_css
from nav_config import BASE_URL, SITE_NAME

DATA_DIR = 'data'
SITE_DIR = 'site'
JOBS_DIR = f'{SITE_DIR}/jobs'


def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def format_date(date_str):
    """Format date for display."""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str[:10], '%Y-%m-%d')
        return dt.strftime('%b %d, %Y')
    except:
        return date_str


def get_role_display(role_type):
    """Get display name for role type."""
    role_map = {
        'cfo': 'CFO',
        'cmo': 'CMO',
        'cto': 'CTO',
        'coo': 'COO',
        'chro': 'CHRO',
        'cpo': 'CPO',
        'cro': 'CRO',
        'ciso': 'CISO',
        'cio': 'CIO',
        'vp': 'VP',
        'director': 'Director',
        'head_of': 'Head of',
    }
    return role_map.get(role_type, role_type.upper() if role_type else 'Other')


# Additional CSS for job board page
JOB_BOARD_CSS = """
/* Job Board Specific Styles */
.page-header {
    padding: 8rem 0 3rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
}

.page-header__inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}

.page-header__title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: var(--space-sm);
}

.page-header__subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
}

/* Filters */
.filters {
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border);
    padding: var(--space-lg);
    position: sticky;
    top: 72px;
    z-index: 50;
}

.filters__inner {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
    align-items: center;
}

.filter-search {
    flex: 1;
    min-width: 250px;
    position: relative;
}

.filter-search__input {
    width: 100%;
    padding: var(--space-md) var(--space-lg);
    padding-left: 3rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 1rem;
    outline: none;
    transition: border-color var(--transition-fast);
}

.filter-search__input:focus {
    border-color: var(--teal);
}

.filter-search__input::placeholder {
    color: var(--text-muted);
}

.filter-search__icon {
    position: absolute;
    left: var(--space-md);
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
}

.filter-btn {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    padding: var(--space-sm) var(--space-md);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-full);
    color: var(--text-secondary);
    font-size: 0.9rem;
    cursor: pointer;
    transition: all var(--transition-fast);
}

.filter-btn:hover, .filter-btn.active {
    background: var(--teal);
    border-color: var(--teal);
    color: white;
}

/* Job List */
.jobs-list {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--space-xl) var(--space-lg);
}

.jobs-list__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-lg);
}

.jobs-list__count {
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.jobs-list__sort {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.jobs-list__sort select {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    padding: var(--space-sm) var(--space-md);
    font-size: 0.9rem;
    cursor: pointer;
}

/* Job Card (list view) */
.job-item {
    display: block;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
    transition: all var(--transition-fast);
}

.job-item:hover {
    background: var(--bg-card-hover);
    border-color: var(--teal);
    transform: translateY(-2px);
}

.job-item__header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-md);
}

.job-item__company {
    font-size: 0.9rem;
    color: var(--teal-light);
    font-weight: 500;
    margin-bottom: var(--space-xs);
}

.job-item__title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}

.job-item__salary {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--success);
    text-align: right;
}

.job-item__meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
}

.job-item__tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.job-item__tag--remote {
    background: rgba(74, 222, 128, 0.15);
    color: var(--success);
}

.job-item__tag--role {
    background: rgba(26, 154, 138, 0.15);
    color: var(--teal-light);
}

.job-item__date {
    margin-left: auto;
    font-size: 0.8rem;
    color: var(--text-muted);
}

/* No results */
.no-results {
    text-align: center;
    padding: var(--space-3xl);
    color: var(--text-secondary);
}

.no-results__title {
    font-size: 1.5rem;
    margin-bottom: var(--space-md);
    color: var(--text-primary);
}

@media (max-width: 768px) {
    .page-header {
        padding: 6rem 0 2rem;
    }

    .page-header__title {
        font-size: 2rem;
    }

    .filters__inner {
        flex-direction: column;
    }

    .filter-search {
        width: 100%;
    }

    .job-item__header {
        flex-direction: column;
        gap: var(--space-sm);
    }

    .job-item__salary {
        text-align: left;
    }
}
"""


def main():
    print("=" * 60)
    print("  FRACTIONAL PULSE - GENERATING JOB BOARD")
    print("=" * 60)

    os.makedirs(JOBS_DIR, exist_ok=True)

    # Load job data
    jobs_file = f"{DATA_DIR}/jobs.json"
    if not os.path.exists(jobs_file):
        print(f"  ERROR: {jobs_file} not found")
        sys.exit(1)

    with open(jobs_file) as f:
        data = json.load(f)

    jobs = data.get('jobs', [])
    stats = data.get('stats', {})
    print(f"  Loaded {len(jobs)} jobs from jobs.json")

    # Calculate stats
    total_jobs = len(jobs)
    remote_jobs = sum(1 for j in jobs if j.get('is_remote'))
    with_salary = sum(1 for j in jobs if j.get('has_salary'))
    c_level = sum(1 for j in jobs if j.get('is_c_level'))

    # Role type counts for filters
    role_counts = {}
    for job in jobs:
        role = job.get('role_type') or 'other'
        role_counts[role] = role_counts.get(role, 0) + 1

    # Generate filter buttons
    filter_buttons = '<button class="filter-btn active" data-filter="all">All Roles</button>\n'
    for role, count in sorted(role_counts.items(), key=lambda x: -x[1]):
        display = get_role_display(role)
        filter_buttons += f'<button class="filter-btn" data-filter="{role}">{display} ({count})</button>\n'

    # Generate job cards HTML
    job_cards_html = ""
    for job in jobs:
        company = escape_html(job.get('company', 'Confidential'))
        title = escape_html(job.get('title', 'Fractional Executive'))
        location = escape_html(job.get('location', ''))
        comp_display = job.get('compensation', {}).get('display', 'Not disclosed')
        role_type = job.get('role_type') or 'other'
        is_remote = job.get('is_remote', False)
        slug = job.get('slug', '')
        date_posted = format_date(job.get('date_posted'))

        # Tags
        tags_html = ""
        if is_remote:
            tags_html += '<span class="job-item__tag job-item__tag--remote">Remote</span>'
        elif location:
            tags_html += f'<span class="job-item__tag">{location}</span>'

        if role_type and role_type != 'other':
            tags_html += f'<span class="job-item__tag job-item__tag--role">{get_role_display(role_type)}</span>'

        if date_posted:
            tags_html += f'<span class="job-item__date">{date_posted}</span>'

        job_cards_html += f'''
        <a href="/jobs/{slug}/" class="job-item"
           data-role="{role_type}"
           data-remote="{str(is_remote).lower()}"
           data-company="{company.lower()}"
           data-title="{title.lower()}">
            <div class="job-item__header">
                <div>
                    <div class="job-item__company">{company}</div>
                    <div class="job-item__title">{title}</div>
                </div>
                <div class="job-item__salary">{comp_display}</div>
            </div>
            <div class="job-item__meta">
                {tags_html}
            </div>
        </a>
        '''

    # Search and filter JavaScript
    search_js = '''
    <script>
    (function() {
        const searchInput = document.getElementById('job-search');
        const filterBtns = document.querySelectorAll('.filter-btn');
        const jobItems = document.querySelectorAll('.job-item');
        const countEl = document.getElementById('job-count');
        let activeFilter = 'all';

        function filterJobs() {
            const query = searchInput.value.toLowerCase();
            let visible = 0;

            jobItems.forEach(item => {
                const role = item.dataset.role;
                const company = item.dataset.company;
                const title = item.dataset.title;

                const matchesFilter = activeFilter === 'all' || role === activeFilter;
                const matchesSearch = !query ||
                    company.includes(query) ||
                    title.includes(query);

                if (matchesFilter && matchesSearch) {
                    item.style.display = '';
                    visible++;
                } else {
                    item.style.display = 'none';
                }
            });

            countEl.textContent = visible + ' jobs found';
        }

        searchInput.addEventListener('input', filterJobs);

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeFilter = btn.dataset.filter;
                filterJobs();
            });
        });
    })();
    </script>
    '''

    # Build page content
    body_content = f'''
        <div class="page-header">
            <div class="page-header__inner">
                <h1 class="page-header__title">Fractional Executive Jobs</h1>
                <p class="page-header__subtitle">{total_jobs} opportunities from top companies seeking fractional CFOs, CMOs, CTOs, and more</p>
            </div>
        </div>

        <div class="filters">
            <div class="filters__inner">
                <div class="filter-search">
                    <svg class="filter-search__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <path d="m21 21-4.35-4.35"></path>
                    </svg>
                    <input type="text" id="job-search" class="filter-search__input" placeholder="Search by company or title...">
                </div>
                {filter_buttons}
            </div>
        </div>

        <div class="jobs-list">
            <div class="jobs-list__header">
                <span class="jobs-list__count" id="job-count">{total_jobs} jobs found</span>
            </div>

            <div class="jobs-list__items">
                {job_cards_html}
            </div>
        </div>
        {search_js}
    '''

    # Generate page
    extra_css = f"<style>{JOB_BOARD_CSS}</style>"
    html = get_full_page(
        title=f"Fractional Executive Jobs ({total_jobs} Open Positions)",
        description=f"Browse {total_jobs} fractional executive jobs. Find part-time CFO, CMO, CTO, COO roles with flexible hours and competitive rates.",
        body_content=body_content,
        canonical_path="/jobs/",
        extra_head=extra_css
    )

    # Write file
    output_file = f"{JOBS_DIR}/index.html"
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"  Generated: {output_file}")
    print(f"  Total jobs: {total_jobs}")
    print(f"  Remote jobs: {remote_jobs}")
    print(f"  With salary: {with_salary}")
    print("=" * 60)


if __name__ == "__main__":
    main()
