#!/usr/bin/env python3
"""
Generate XML sitemaps for Fractional Pulse.
"""

import json
import os
import sys
from datetime import datetime

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import BASE_URL

DATA_DIR = 'data'
SITE_DIR = 'site'

TODAY = datetime.now().strftime('%Y-%m-%d')


def generate_sitemap_xml(urls):
    """Generate sitemap XML from URL list."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        loc = url.get('loc', '')
        lastmod = url.get('lastmod', TODAY)
        changefreq = url.get('changefreq', 'weekly')
        priority = url.get('priority', '0.5')

        xml += '  <url>\n'
        xml += f'    <loc>{loc}</loc>\n'
        xml += f'    <lastmod>{lastmod}</lastmod>\n'
        xml += f'    <changefreq>{changefreq}</changefreq>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += '  </url>\n'

    xml += '</urlset>'
    return xml


def generate_sitemap_index(sitemaps):
    """Generate sitemap index XML."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for sitemap in sitemaps:
        xml += '  <sitemap>\n'
        xml += f'    <loc>{sitemap["loc"]}</loc>\n'
        xml += f'    <lastmod>{sitemap.get("lastmod", TODAY)}</lastmod>\n'
        xml += '  </sitemap>\n'

    xml += '</sitemapindex>'
    return xml


def main():
    print("=" * 60)
    print("  FRACTIONAL PULSE - GENERATING SITEMAPS")
    print("=" * 60)

    os.makedirs(f"{SITE_DIR}/sitemaps", exist_ok=True)

    # Load job data
    jobs_file = f"{DATA_DIR}/jobs.json"
    jobs = []
    if os.path.exists(jobs_file):
        with open(jobs_file) as f:
            data = json.load(f)
        jobs = data.get('jobs', [])

    print(f"  Loaded {len(jobs)} jobs")

    # Main sitemap (core pages)
    main_urls = [
        {'loc': f'{BASE_URL}/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': f'{BASE_URL}/jobs/', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': f'{BASE_URL}/about/', 'priority': '0.6', 'changefreq': 'monthly'},
    ]

    main_xml = generate_sitemap_xml(main_urls)
    with open(f'{SITE_DIR}/sitemaps/sitemap-main.xml', 'w') as f:
        f.write(main_xml)
    print(f"  Generated: sitemaps/sitemap-main.xml ({len(main_urls)} URLs)")

    # Jobs sitemap
    job_urls = []
    for job in jobs:
        slug = job.get('slug')
        if slug:
            job_urls.append({
                'loc': f'{BASE_URL}/jobs/{slug}/',
                'lastmod': job.get('date_posted', TODAY)[:10] if job.get('date_posted') else TODAY,
                'priority': '0.7',
                'changefreq': 'weekly'
            })

    if job_urls:
        jobs_xml = generate_sitemap_xml(job_urls)
        with open(f'{SITE_DIR}/sitemaps/sitemap-jobs.xml', 'w') as f:
            f.write(jobs_xml)
        print(f"  Generated: sitemaps/sitemap-jobs.xml ({len(job_urls)} URLs)")

    # Sitemap index
    sitemaps = [
        {'loc': f'{BASE_URL}/sitemaps/sitemap-main.xml', 'lastmod': TODAY},
    ]
    if job_urls:
        sitemaps.append({'loc': f'{BASE_URL}/sitemaps/sitemap-jobs.xml', 'lastmod': TODAY})

    index_xml = generate_sitemap_index(sitemaps)
    with open(f'{SITE_DIR}/sitemap_index.xml', 'w') as f:
        f.write(index_xml)
    print(f"  Generated: sitemap_index.xml")

    # Also create a simple sitemap.xml at root for compatibility
    all_urls = main_urls + job_urls
    all_xml = generate_sitemap_xml(all_urls)
    with open(f'{SITE_DIR}/sitemap.xml', 'w') as f:
        f.write(all_xml)
    print(f"  Generated: sitemap.xml ({len(all_urls)} total URLs)")

    # Update robots.txt with sitemap reference
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap_index.xml
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(f'{SITE_DIR}/robots.txt', 'w') as f:
        f.write(robots_content)
    print(f"  Updated: robots.txt")

    print("=" * 60)


if __name__ == "__main__":
    main()
