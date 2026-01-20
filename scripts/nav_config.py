#!/usr/bin/env python3
"""
Navigation configuration for Fractional Pulse.
Single source of truth for all navigation elements.
"""

# Site information
SITE_NAME = "Fractional Pulse"
SITE_TAGLINE = "Jobs & Market Intelligence for Fractional Executives"
BASE_URL = "https://fractionalpulse.com"
LOGO_TEXT = "FP"

# Main navigation items
NAV_ITEMS = [
    {"label": "Jobs", "href": "/jobs/"},
    {"label": "Salaries", "href": "/salaries/"},
    {"label": "Companies", "href": "/companies/"},
    {"label": "Insights", "href": "/insights/"},
    {"label": "About", "href": "/about/"},
]

# Header CTA button
HEADER_CTA = {
    "label": "Browse Jobs",
    "href": "/jobs/",
}

# Footer configuration
FOOTER_COLUMNS = [
    {
        "title": "Jobs",
        "links": [
            {"label": "All Jobs", "href": "/jobs/"},
            {"label": "Fractional CFO", "href": "/jobs/?role=cfo"},
            {"label": "Fractional CMO", "href": "/jobs/?role=cmo"},
            {"label": "Fractional CTO", "href": "/jobs/?role=cto"},
            {"label": "Fractional COO", "href": "/jobs/?role=coo"},
        ]
    },
    {
        "title": "Resources",
        "links": [
            {"label": "Salary Data", "href": "/salaries/"},
            {"label": "Companies", "href": "/companies/"},
            {"label": "Market Insights", "href": "/insights/"},
        ]
    },
    {
        "title": "Company",
        "links": [
            {"label": "About", "href": "/about/"},
            {"label": "Newsletter", "href": "/newsletter/"},
            {"label": "Contact", "href": "mailto:hello@fractionalpulse.com"},
        ]
    },
]

# Role categories for browse section
ROLE_CATEGORIES = [
    {
        "id": "cfo",
        "title": "Fractional CFO",
        "icon": "$",
        "slug": "fractional-cfo",
    },
    {
        "id": "cmo",
        "title": "Fractional CMO",
        "icon": "M",
        "slug": "fractional-cmo",
    },
    {
        "id": "cto",
        "title": "Fractional CTO",
        "icon": "</>",
        "slug": "fractional-cto",
    },
    {
        "id": "coo",
        "title": "Fractional COO",
        "icon": "O",
        "slug": "fractional-coo",
    },
    {
        "id": "chro",
        "title": "Fractional CHRO",
        "icon": "H",
        "slug": "fractional-chro",
    },
    {
        "id": "cro",
        "title": "Fractional CRO",
        "icon": "R",
        "slug": "fractional-cro",
    },
    {
        "id": "cpo",
        "title": "Fractional CPO",
        "icon": "P",
        "slug": "fractional-cpo",
    },
    {
        "id": "other",
        "title": "Other Roles",
        "icon": "+",
        "slug": "other",
    },
]

# Social links (if any)
SOCIAL_LINKS = [
    # {"platform": "linkedin", "url": "https://linkedin.com/company/fractionalpulse"},
    # {"platform": "twitter", "url": "https://twitter.com/fractionalpulse"},
]

# Copyright text
COPYRIGHT_TEXT = f"© 2025 {SITE_NAME}. All rights reserved."
