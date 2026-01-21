#!/usr/bin/env python3
"""
Generate individual job pages at /jobs/{slug}/index.html
"""

import json
import os
import sys
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
        return dt.strftime('%B %d, %Y')
    except:
        return date_str


def markdown_to_html(text):
    """Convert basic markdown to HTML."""
    if not text:
        return ''

    # Escape HTML
    text = escape_html(text)

    # Convert markdown-style formatting
    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # Convert line breaks to paragraphs
    paragraphs = text.split('\n\n')
    html_parts = []

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        # Check if it's a list
        lines = p.split('\n')
        if all(line.strip().startswith(('* ', '- ', '• ')) for line in lines if line.strip()):
            items = [re.sub(r'^[\*\-•]\s*', '', line.strip()) for line in lines if line.strip()]
            html_parts.append('<ul>' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>')
        else:
            # Regular paragraph - convert single newlines to <br>
            p = p.replace('\n', '<br>')
            html_parts.append(f'<p>{p}</p>')

    return '\n'.join(html_parts)


def get_role_display(role_type):
    """Get display name for role type."""
    role_map = {
        'cfo': 'Fractional CFO',
        'cmo': 'Fractional CMO',
        'cto': 'Fractional CTO',
        'coo': 'Fractional COO',
        'chro': 'Fractional CHRO',
        'cpo': 'Fractional CPO',
        'cro': 'Fractional CRO',
        'ciso': 'Fractional CISO',
        'cio': 'Fractional CIO',
        'vp': 'VP Level',
        'director': 'Director Level',
        'head_of': 'Head of Department',
    }
    return role_map.get(role_type, 'Fractional Executive')


# Additional CSS for job detail page
JOB_DETAIL_CSS = """
/* Job Detail Page Styles */
.job-detail {
    padding-top: 72px;
}

.job-header {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: var(--space-2xl) 0;
}

.job-header__inner {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 var(--space-lg);
}

.job-header__breadcrumb {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: var(--space-lg);
}

.job-header__breadcrumb a {
    color: var(--text-secondary);
    transition: color var(--transition-fast);
}

.job-header__breadcrumb a:hover {
    color: var(--teal-light);
}

.job-header__company {
    font-size: 1.1rem;
    color: var(--teal-light);
    font-weight: 500;
    margin-bottom: var(--space-sm);
}

.job-header__title {
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: var(--space-lg);
    line-height: 1.2;
}

.job-header__meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-md);
    margin-bottom: var(--space-xl);
}

.job-header__tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: var(--space-sm) var(--space-md);
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-full);
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.job-header__tag--salary {
    background: rgba(74, 222, 128, 0.1);
    border-color: rgba(74, 222, 128, 0.3);
    color: var(--success);
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
}

.job-header__tag--remote {
    background: rgba(74, 222, 128, 0.1);
    border-color: rgba(74, 222, 128, 0.3);
    color: var(--success);
}

.job-header__actions {
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
}

/* Job Content */
.job-content {
    max-width: 900px;
    margin: 0 auto;
    padding: var(--space-2xl) var(--space-lg);
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: var(--space-2xl);
}

.job-main {
    min-width: 0;
}

.job-sidebar {
    position: sticky;
    top: calc(72px + var(--space-xl));
    height: fit-content;
}

.job-section {
    margin-bottom: var(--space-2xl);
}

.job-section__title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 1px solid var(--border);
}

.job-description {
    color: var(--text-secondary);
    line-height: 1.8;
}

.job-description p {
    margin-bottom: var(--space-md);
}

.job-description ul {
    margin: var(--space-md) 0;
    padding-left: var(--space-xl);
}

.job-description li {
    margin-bottom: var(--space-sm);
}

.job-description strong {
    color: var(--text-primary);
}

/* Sidebar Card */
.sidebar-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-lg);
}

.sidebar-card__title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: var(--space-md);
}

.sidebar-card__item {
    display: flex;
    justify-content: space-between;
    padding: var(--space-sm) 0;
    border-bottom: 1px solid var(--border-light);
    font-size: 0.9rem;
}

.sidebar-card__item:last-child {
    border-bottom: none;
}

.sidebar-card__label {
    color: var(--text-muted);
}

.sidebar-card__value {
    color: var(--text-primary);
    font-weight: 500;
}

.sidebar-card__value--highlight {
    color: var(--teal-light);
}

/* Similar Jobs */
.similar-jobs {
    margin-top: var(--space-2xl);
    padding-top: var(--space-2xl);
    border-top: 1px solid var(--border);
}

.similar-jobs__title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: var(--space-lg);
}

.similar-jobs__grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-md);
}

.similar-job {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    transition: all var(--transition-fast);
}

.similar-job:hover {
    background: var(--bg-card-hover);
    border-color: var(--teal);
}

.similar-job__company {
    font-size: 0.85rem;
    color: var(--teal-light);
    margin-bottom: 4px;
}

.similar-job__title {
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: var(--space-sm);
}

.similar-job__salary {
    font-size: 0.9rem;
    color: var(--success);
    font-family: 'Space Grotesk', sans-serif;
}

@media (max-width: 900px) {
    .job-content {
        grid-template-columns: 1fr;
    }

    .job-sidebar {
        position: static;
        order: -1;
    }

    .similar-jobs__grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 600px) {
    .job-header__title {
        font-size: 1.75rem;
    }

    .job-header__actions {
        flex-direction: column;
    }

    .job-header__actions .btn {
        width: 100%;
        justify-content: center;
    }
}
"""


def generate_job_posting_schema(job):
    """Generate JobPosting JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "title": job.get('title', ''),
        "description": job.get('description_snippet', '')[:500] if job.get('description_snippet') else '',
        "datePosted": job.get('date_posted', ''),
        "hiringOrganization": {
            "@type": "Organization",
            "name": job.get('company', 'Confidential')
        },
        "jobLocation": {
            "@type": "Place",
            "address": job.get('location', 'Remote')
        },
        "employmentType": "CONTRACTOR",
    }

    if job.get('is_remote'):
        schema["jobLocationType"] = "TELECOMMUTE"

    comp = job.get('compensation', {})
    if comp.get('min'):
        schema["baseSalary"] = {
            "@type": "MonetaryAmount",
            "currency": "USD",
            "value": {
                "@type": "QuantitativeValue",
                "minValue": comp.get('min'),
                "maxValue": comp.get('max') or comp.get('min'),
                "unitText": "HOUR" if comp.get('type') == 'hourly' else "YEAR"
            }
        }

    return json.dumps(schema, indent=2)


def main():
    print("=" * 60)
    print("  FRACTIONAL PULSE - GENERATING JOB PAGES")
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
    print(f"  Loaded {len(jobs)} jobs")

    generated = 0

    for job in jobs:
        slug = job.get('slug')
        if not slug:
            continue

        company = escape_html(job.get('company', 'Confidential'))
        title = escape_html(job.get('title', 'Fractional Executive'))
        location = job.get('location', 'Remote')
        comp = job.get('compensation', {})
        comp_display = comp.get('display', 'Not disclosed')
        role_type = job.get('role_type')
        is_remote = job.get('is_remote', False)
        date_posted = format_date(job.get('date_posted'))
        source_url = job.get('source_url', '#')
        description = job.get('description', '')
        hours = job.get('hours', {})

        # Format description
        description_html = markdown_to_html(description) if description else '<p>No description available.</p>'

        # Meta tags
        tags_html = ""
        if comp_display != 'Not disclosed':
            tags_html += f'<span class="job-header__tag job-header__tag--salary">{comp_display}</span>'
        if is_remote:
            tags_html += '<span class="job-header__tag job-header__tag--remote">Remote</span>'
        else:
            tags_html += f'<span class="job-header__tag">{escape_html(location)}</span>'
        if role_type and role_type != 'other':
            tags_html += f'<span class="job-header__tag">{get_role_display(role_type)}</span>'
        if hours.get('display') and hours.get('display') != 'Not specified':
            tags_html += f'<span class="job-header__tag">{hours["display"]}</span>'

        # Sidebar details
        sidebar_items = []
        sidebar_items.append(('Company', company))
        sidebar_items.append(('Location', 'Remote' if is_remote else location))
        if comp_display != 'Not disclosed':
            sidebar_items.append(('Compensation', f'<span class="sidebar-card__value--highlight">{comp_display}</span>'))
        if hours.get('display') and hours.get('display') != 'Not specified':
            sidebar_items.append(('Hours', hours['display']))
        if date_posted:
            sidebar_items.append(('Posted', date_posted))

        sidebar_html = ""
        for label, value in sidebar_items:
            sidebar_html += f'''
            <div class="sidebar-card__item">
                <span class="sidebar-card__label">{label}</span>
                <span class="sidebar-card__value">{value}</span>
            </div>'''

        # Find similar jobs (same role type, different company)
        similar_jobs = [j for j in jobs if j.get('role_type') == role_type and j.get('slug') != slug][:4]
        similar_html = ""
        if similar_jobs:
            similar_cards = ""
            for sj in similar_jobs:
                sj_comp = sj.get('compensation', {}).get('display', '')
                similar_cards += f'''
                <a href="/jobs/{sj.get('slug')}/" class="similar-job">
                    <div class="similar-job__company">{escape_html(sj.get('company', ''))}</div>
                    <div class="similar-job__title">{escape_html(sj.get('title', ''))}</div>
                    {f'<div class="similar-job__salary">{sj_comp}</div>' if sj_comp and sj_comp != 'Not disclosed' else ''}
                </a>'''

            similar_html = f'''
            <div class="similar-jobs">
                <h2 class="similar-jobs__title">Similar Opportunities</h2>
                <div class="similar-jobs__grid">
                    {similar_cards}
                </div>
            </div>'''

        # JSON-LD Schema
        schema_json = generate_job_posting_schema(job)

        # Build page content
        body_content = f'''
        <div class="job-detail">
            <div class="job-header">
                <div class="job-header__inner">
                    <nav class="job-header__breadcrumb">
                        <a href="/">Home</a>
                        <span>/</span>
                        <a href="/jobs/">Jobs</a>
                        <span>/</span>
                        <span>{title[:30]}{'...' if len(title) > 30 else ''}</span>
                    </nav>

                    <div class="job-header__company">{company}</div>
                    <h1 class="job-header__title">{title}</h1>

                    <div class="job-header__meta">
                        {tags_html}
                    </div>

                    <div class="job-header__actions">
                        <a href="{source_url}" target="_blank" rel="noopener" class="btn btn--primary">Apply Now</a>
                        <a href="/jobs/" class="btn btn--secondary">View All Jobs</a>
                    </div>
                </div>
            </div>

            <div class="job-content">
                <div class="job-main">
                    <div class="job-section">
                        <h2 class="job-section__title">About This Role</h2>
                        <div class="job-description">
                            {description_html}
                        </div>
                    </div>
                    {similar_html}
                </div>

                <aside class="job-sidebar">
                    <div class="sidebar-card">
                        <h3 class="sidebar-card__title">Job Details</h3>
                        {sidebar_html}
                    </div>

                    <a href="{source_url}" target="_blank" rel="noopener" class="btn btn--primary" style="width: 100%; justify-content: center;">
                        Apply Now
                    </a>
                </aside>
            </div>
        </div>
        '''

        # Generate page
        extra_head = f'''
    <style>{JOB_DETAIL_CSS}</style>
    <script type="application/ld+json">
{schema_json}
    </script>'''

        html = get_full_page(
            title=f"{title} at {company}",
            description=f"{title} opportunity at {company}. {comp_display}. {location}. Apply now for this fractional executive role.",
            body_content=body_content,
            canonical_path=f"/jobs/{slug}/",
            extra_head=extra_head
        )

        # Write file
        job_dir = f"{JOBS_DIR}/{slug}"
        os.makedirs(job_dir, exist_ok=True)
        output_file = f"{job_dir}/index.html"

        with open(output_file, 'w') as f:
            f.write(html)

        generated += 1

    print(f"  Generated {generated} job pages")
    print("=" * 60)


if __name__ == "__main__":
    main()
