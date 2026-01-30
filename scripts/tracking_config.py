#!/usr/bin/env python3
"""
Analytics and tracking configuration for Fractional Pulse.
Update these IDs when analytics accounts are set up.
"""

# Google Analytics 4
GA4_ID = "G-4XJB2YNHFC"

# Microsoft Clarity
CLARITY_ID = ""  # e.g., "abcdefghij"


def get_analytics_scripts():
    """
    Return analytics script tags.
    Only returns scripts if IDs are configured.
    """
    scripts = ""

    if GA4_ID:
        scripts += f'''
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA4_ID}');
    </script>
'''

    if CLARITY_ID:
        scripts += f'''
    <!-- Microsoft Clarity -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/{CLARITY_ID}";
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{CLARITY_ID}");
    </script>
'''

    return scripts
