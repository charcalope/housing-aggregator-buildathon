from bs4 import BeautifulSoup
import time, urllib, requests, json
import re

def get_domain(url, debug=False):
    if debug:
        print('executing get_domain...')
    expr = re.compile(r'https?:\/\/([^/]*)')
    pre = expr.match(url)
    return pre.group(1)

def filter_domain_dupes(links, debug=False):
    if debug:
        print('executing filter_domain_dupes...')
    domain_dict = dict()
    for link in links:
        domain = get_domain(link)
        if domain not in domain_dict.keys():
            domain_dict[domain] = link
    return domain_dict.values()

def all_urls(link, debug=False):
    """returns a list of all page links within a given domain"""
    if debug:
        print('Executing all_urls...')
    links = set()
    untraversed = [link]
    domain = get_domain(link)
    if 'www.' in domain:
        domain = domain.replace('www.', '')

    if debug:
        print(f"DOMAIN: {domain}")

    def in_domain(href):
        if debug:
            print(f"TESTING IN DOMAIN {href}")
        # to be passed into the beatiful soup filter
        def wonky():
            # don't explore images for links
            img_suffs = ['png', 'jpeg', 'jpg', 'pdf', 'xml', '.mp4']
            return any([x in href for x in img_suffs])

        return href and (domain in href or '.aspx' in href) and (href not in links) and (not wonky())

    while len(untraversed) > 0:
        if len(links) > 35:
            return [link]

        current_link = untraversed.pop()


        if debug:
            print(f'Now traversing {current_link}')
        try:
            page = requests.get(current_link)
            data = page.text
        except:
            if debug:
                print(f"ERROR: BROKEN AT {current_link}")
            break
        soup = BeautifulSoup(data, 'html.parser')

        for soup_result in soup.find_all("a", href=in_domain):
            link_found = soup_result.get('href')

            if 'aspx' in link_found:
                link_found = str(f"www.{domain}/{link_found}")
                if debug:
                    print(f"    EDITED ASPX TO {link_found}")

            if debug:
                print(link_found)
            if link_found in links:
                continue
            links.add(link_found)
            untraversed.append(link_found)

    return links