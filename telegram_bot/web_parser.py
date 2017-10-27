"""Parses given web page and returns all text files found"""

from urllib.request import urlopen
import re


def is_text_file(href):
    pattern = ".*\.(txt)\s?"
    return re.match(pattern, href)


def _get_href(link):
    pattern = "href\s*=\s*(\"([^\"]*\")|'[^']*'|([^'\">\s]+))"
    s = re.search(pattern, link, re.IGNORECASE)
    href = None
    if s is not None:
        href = s.group(1)
        brakets_pattern = "('|\")([^'\"]*)('|\")"
        m = re.match(brakets_pattern, href)
        if m:
            href = m.group(2)
    return href


def _get_text_links(line):
    text_links = []
    link_pattern = "<a([^>]+)>(.+?)</a>"
    links = re.findall(link_pattern, line, re.IGNORECASE)
    for link_params, title in links:
        href = _get_href(link_params)
        if href and is_text_file(href):
            text_links.append(href)
    return text_links


def get_links_to_text_files(web_address):
    response = urlopen(web_address)

    website_html = response.readlines()
    text_links = []

    for line in website_html:
        line = line.decode("utf-8")
        text_links.extend(_get_text_links(line))
    return text_links
