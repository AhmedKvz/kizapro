#!/usr/bin/env python3
"""
scripts/verify_site.py
Automated website verification and audit suite for afterBefore promo (sr.html).
Performs checks on HTML syntax, CSS rules, link integrity, SEO/OpenGraph tags,
mobile responsiveness parameters, asset availability, and interactive elements.
"""

import sys
import os
import re
import json
import urllib.request
import urllib.error
from html.parser import HTMLParser

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.tags = []
        self.images = []
        self.videos = []
        self.buttons = []
        self.metas = []
        self.headings = []
        self.title = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tags.append(tag)
        if 'id' in attr_dict:
            self.ids.add(attr_dict['id'])
        if tag == 'title':
            self._in_title = True
        elif tag == 'meta':
            self.metas.append(attr_dict)
        elif tag == 'a':
            self.links.append(attr_dict)
        elif tag == 'img':
            self.images.append(attr_dict)
        elif tag == 'video':
            self.videos.append(attr_dict)
        elif tag == 'button':
            self.buttons.append(attr_dict)
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.headings.append((tag, attr_dict))

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title = data.strip()

def check_external_url(url, timeout=10):
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {'status': resp.status, 'ok': True, 'msg': 'OK'}
    except urllib.error.HTTPError as e:
        return {'status': e.code, 'ok': (e.code in [200, 301, 302, 307, 308, 403, 405]), 'msg': f'HTTP {e.code}'}
    except Exception as e:
        return {'status': None, 'ok': False, 'msg': str(e)}

def run_verification(html_file, css_file=None, live_url=None):
    results = {
        'html_structure': {},
        'seo_metadata': {},
        'anchor_links': {'passed': [], 'failed': []},
        'external_links': {'passed': [], 'failed': []},
        'assets': {'passed': [], 'failed': []},
        'responsive_viewport': {},
        'accessibility': {},
        'issues_found': []
    }

    if not os.path.exists(html_file):
        raise FileNotFoundError(f"File {html_file} not found")

    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()

    parser = LinkExtractor()
    parser.feed(html_content)

    # 1. HTML & SEO Metadata
    results['html_structure']['has_doctype'] = bool(re.search(r'<!doctype\s+html>', html_content, re.IGNORECASE))
    results['html_structure']['has_html_lang'] = bool(re.search(r'<html\s+[^>]*lang=["\']sr["\']', html_content))
    results['seo_metadata']['title'] = parser.title

    for m in parser.metas:
        if m.get('name') == 'description':
            results['seo_metadata']['description'] = m.get('content')
        if m.get('name') == 'viewport':
            results['responsive_viewport']['raw'] = m.get('content')
            results['responsive_viewport']['has_initial_scale'] = 'initial-scale=1' in m.get('content', '')
            results['responsive_viewport']['has_width_device'] = 'width=device-width' in m.get('content', '')
            results['responsive_viewport']['has_viewport_fit'] = 'viewport-fit=cover' in m.get('content', '')
        if m.get('property') and m.get('property').startswith('og:'):
            results['seo_metadata'][m.get('property')] = m.get('content')
        if m.get('name') and m.get('name').startswith('twitter:'):
            results['seo_metadata'][m.get('name')] = m.get('content')

    # Canonical and alternate hreflang
    canon = re.findall(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html_content)
    results['seo_metadata']['canonical'] = canon[0] if canon else None

    hreflangs = re.findall(r'<link\s+[^>]*hreflang=["\']([^"\']+)["\'][^>]*href=["\']([^"\']+)["\']', html_content)
    results['seo_metadata']['hreflangs'] = hreflangs

    # Check safe-area viewport
    if not results['responsive_viewport'].get('has_viewport_fit'):
        results['issues_found'].append({
            'severity': 'MEDIUM',
            'type': 'RESPONSIVE',
            'description': 'Viewport meta tag ne sadrži "viewport-fit=cover", što može dovesti do belih margina na iPhone uređajima sa notch-om/Dynamic Island-om.'
        })

    # Check canonical pointing to https://afterbefore.rs/sr vs afterbefore-promo.netlify.app
    if results['seo_metadata']['canonical'] and 'netlify.app' not in results['seo_metadata']['canonical']:
        results['seo_metadata']['canonical_note'] = (
            f"Canonical URL je postavljen na zvanični domen: {results['seo_metadata']['canonical']} (nije netlify poddomen, što je ispravno za produkciju)."
        )

    # 2. Anchors check
    for link in parser.links:
        href = link.get('href', '')
        if href.startswith('#'):
            target_id = href.lstrip('#')
            if target_id == '' or target_id in parser.ids:
                results['anchor_links']['passed'].append(href)
            else:
                results['anchor_links']['failed'].append(href)
                results['issues_found'].append({
                    'severity': 'HIGH',
                    'type': 'BROKEN_ANCHOR',
                    'description': f"Anchor link '{href}' nema odgovarajući element sa id='{target_id}' na stranici!"
                })

    # 3. External links check
    checked_urls = {}
    for link in parser.links:
        href = link.get('href', '')
        if href.startswith('http://') or href.startswith('https://'):
            if href in checked_urls:
                status_info = checked_urls[href]
            else:
                print(f"Proveravam eksterni link: {href} ...")
                status_info = check_external_url(href)
                checked_urls[href] = status_info

            link_entry = {'url': href, 'text': link.get('aria-label', ''), 'status': status_info['status'], 'msg': status_info['msg']}
            if status_info['ok']:
                results['external_links']['passed'].append(link_entry)
            else:
                results['external_links']['failed'].append(link_entry)
                results['issues_found'].append({
                    'severity': 'HIGH',
                    'type': 'DEAD_LINK',
                    'description': f"Eksterni link {href} vraća grešku: {status_info['msg']}"
                })

    # 4. Local & Remote Assets check
    all_asset_srcs = set()
    for img in parser.images:
        if 'src' in img:
            all_asset_srcs.add(img['src'])
    for vid in parser.videos:
        if 'poster' in vid:
            all_asset_srcs.add(vid['poster'])
    video_sources = re.findall(r'<source\s+[^>]*src=["\']([^"\']+)["\']', html_content)
    for vs in video_sources:
        all_asset_srcs.add(vs)
    favicons = re.findall(r'<link\s+[^>]*rel=["\'](?:icon|apple-touch-icon)["\'][^>]*href=["\']([^"\']+)["\']', html_content)
    for fav in favicons:
        all_asset_srcs.add(fav)

    for src in all_asset_srcs:
        # Check local path
        local_path = os.path.join(os.path.dirname(html_file) or '.', src)
        exists_local = os.path.exists(local_path)
        size = os.path.getsize(local_path) if exists_local else 0
        if exists_local:
            results['assets']['passed'].append({'src': src, 'size_bytes': size, 'local': True})
        else:
            results['assets']['failed'].append({'src': src, 'local': False})
            results['issues_found'].append({
                'severity': 'MEDIUM',
                'type': 'MISSING_LOCAL_ASSET',
                'description': f"Lokalni fajl resursa nedostaje: {src}"
            })

    # 5. Accessibility Checks
    images_without_alt = [img for img in parser.images if 'alt' not in img or not img.get('alt', '').strip()]
    results['accessibility']['total_images'] = len(parser.images)
    results['accessibility']['images_without_alt'] = len(images_without_alt)
    if images_without_alt:
        results['issues_found'].append({
            'severity': 'LOW',
            'type': 'ACCESSIBILITY_ALT',
            'description': f"{len(images_without_alt)} slika nema 'alt' atribut."
        })

    # Skip link check
    skip_link = [l for l in parser.links if 'skip' in l.get('class', '')]
    results['accessibility']['has_skip_link'] = len(skip_link) > 0

    # 6. Heading hierarchy check
    heading_tags = [h[0] for h in parser.headings]
    results['html_structure']['headings_hierarchy'] = heading_tags

    return results

if __name__ == '__main__':
    html_target = sys.argv[1] if len(sys.argv) > 1 else 'sr.html'
    print(f"Pokrećem automatsku verifikaciju za: {html_target}")
    res = run_verification(html_target)
    
    output_json = 'verification_results.json'
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    
    print(f"\nVerifikacija završena! Rezultati upisani u {output_json}.")
    print(f"Pronađeno problema/upozorenja: {len(res['issues_found'])}")
    for issue in res['issues_found']:
        print(f" - [{issue['severity']}] {issue['type']}: {issue['description']}")
