from scrapers import *
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def unit_generator(floorplan_link):
    html = get_raw_html(floorplan_link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        yield from router(soup, debug=False)
    else:
        print(f"ERROR AT {floorplan_link}")

def get_raw_html(floorplan_link):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options, executable_path="/usr/local/bin/chromedriver")
        driver.get(floorplan_link)
        html = driver.page_source
        driver.close()

        return html
    except:
        return None

def router(soup, debug=False):
    # TABLIST: DEFAULT

    def is_tablist(role):
        return role and re.compile("tablist").search(role)

    # COLLAPSING LIST : CARD
    test1 = soup.find('div', {'class': re.compile('accordion', re.IGNORECASE)})
    rows = []
    if test1:
        rows = test1.find_all('tr', {'scope': 'row'})

    if test1 and len(rows) > 0:
        if debug:
            print("COLLAPSING LIST CARD")
        yield from collapsinglist_card(soup)

    elif soup.find(role=is_tablist):
        if debug:
            print("TABLIST")
        yield from tablist_default(soup)

    # GRID : CARD
    elif soup.find_all('div', {'class': 'fp-card'}):
        if debug:
            print("GRID CARD")
        yield from grid_card(soup)

    # COLLAPSING LIST : TABLE
    elif soup.find_all('tr', {'data-selenium-id': re.compile('row', re.IGNORECASE)}):
        if debug:
            print("COLLAPSING LIST TABLE")
        yield from collapsinglist_table(soup)

    # GRID: LIST / TABLE
    elif soup.find('ul', {'class': re.compile('plan')}):
        if debug:
            print("GRID LIST / TABLE")
        yield from grid_table(soup)

    # TABLE : DEFAULT
    elif soup.find('thead'):
        if debug:
            print("TABLE")
        yield from table_default(soup)

    else:
        print("NO MATCH")



