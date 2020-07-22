import re
from utils import bed_normalize, bath_normalize, feet_normalize, rent_normalize, normalize_combined_bed_bath, is_name_header
from soup_utils import combines_bed_bath


# COLLAPSING LIST

def collapsinglist_card(soup):
    bb_combined = combines_bed_bath(soup)

    floorplan_container = soup.find_all('div', {'class': re.compile('accordion')})
    for fc in floorplan_container:
        rows = fc.find_all('tr', {'scope': 'row'})
        for row in rows:
            unitName = None
            unitBeds = None
            unitBaths = None
            unitFootage = None
            unitRent = None

            # get name
            name_container = row.find('td', {'data-selenium-id': re.compile('name', re.IGNORECASE)})
            name_child_span = name_container.next_element
            if name_child_span and name_child_span.next_element.next_element:
                unitName = str(name_child_span.next_element.next_element)

            # get bed and bath
            if bb_combined:
                bed_bath_container = row.find('td', {'data-selenium-id': re.compile('bed', re.IGNORECASE)})
                bb_child_span = bed_bath_container.next_element
                if bb_child_span:
                    bb_text = str(bb_child_span.next_element.next_element)
                    bb_text = bb_text.replace('Studio', '0')
                    (beds, baths) = normalize_combined_bed_bath(bb_text)
                    unitBeds = beds
                    unitBaths = baths

            # get square footage
            feet_container = row.find('td', {'data-label': re.compile('ft', re.IGNORECASE)})
            if feet_container:
                unitFootage = feet_normalize(str(feet_container.text))

            # get rent
            rent_container = row.find('td', {'data-label': re.compile('rent', re.IGNORECASE)})
            if rent_container:
                unitRent = rent_normalize(str(rent_container.text))

            if unitBeds and unitBaths:
                result = dict()
                result['name'] = unitName
                result['beds'] = unitBeds
                result['baths'] = unitBaths
                result['footage'] = unitFootage
                result['rent'] = unitRent

                yield result

def collapsinglist_table(soup):
    rows = soup.find_all('tr', {'data-selenium-id': re.compile('Row')})
    for row in rows:
        unitRent = None
        unitBeds = None
        unitBaths = None
        unitAvailability = None
        unitFootage = None
        unitName = None

        # get floor plan name
        nameContainer = row.find('td', {'data-selenium-id': re.compile('Name')})
        if nameContainer:
            nameText = str(nameContainer.text)
            nameText = nameText.replace('Floor Plan', '')
            unitName = nameText

        # get footage
        feetContainer = row.find('td', {'data-label': re.compile('ft', re.IGNORECASE)})
        if feetContainer:
            feetText = str(feetContainer.text)
            feetNumber = feet_normalize(feetText)
            unitFootage = feetNumber

        if combines_bed_bath(soup):
            bed_bath_container = row.find('td', {'data-selenium-id': re.compile('Bed')})
            if bed_bath_container:
                bed_bath_text = str(bed_bath_container.text)
                bed_bath_text = bed_bath_text.replace('Bed/Bath', '')
                (beds, baths) = normalize_combined_bed_bath(bed_bath_text)
                unitBeds = beds
                unitBaths = baths

        # get rent
        rentContainer = row.find('td', {'data-label': 'Rent'})
        if rentContainer:
            try:
                rentText = str(rentContainer.text)
                rentText = rentText.replace('Monthly Rent', '')
                rentNum = rent_normalize(rentText)
                unitRent = rentNum
            except:
                unitRent = None

        if unitName and unitBeds and unitBaths:
            result = dict()
            result['name'] = unitName
            result['beds'] = unitBeds
            result['baths'] = unitBaths
            result['footage'] = unitFootage
            result['rent'] = unitRent
            result['availability'] = unitAvailability

            yield result

# GRID

def grid_card(soup):

    card_containers = soup.find_all('div', {'class': 'fp-card'})
    for card in card_containers:
        unitName = None
        unitBeds = None
        unitBaths = None
        unitFootage = None
        unitRent = None

        # get unit name
        name_container = card.find('h2', {'class': re.compile('name', re.IGNORECASE)})
        if name_container:
            unitName = str(name_container.text)

        # get beds / baths
        # check if studio
        bed_bath_container = card.find('span', {'class': re.compile('type')})
        if 'tudio' in bed_bath_container.text:
            unitBeds = 0
            unitBaths = 1
        else:
            # assumption: combined
            bbtext = str(bed_bath_container.text)
            bbmatch = re.search('([0-9]) bed[s]?.*([0-9]) bath[s]?', bbtext, re.IGNORECASE)
            if bbmatch:
                unitBeds = int(bbmatch.group(1))
                unitBaths = int(bbmatch.group(2))

        # get square footage
        feetContainer = card.find('span', {'class': re.compile('ft', re.IGNORECASE)})
        if feetContainer:
            feetParent = feetContainer.parent
            feetSuspect = feet_normalize(feetParent.text)
            if feetSuspect > 100:
                unitFootage = feetSuspect

        # get rent
        rentContainer = card.find('div', {'class': re.compile('price', re.IGNORECASE)})
        if rentContainer:
            if '$' in rentContainer.text:
                unitRent = rent_normalize(str(rentContainer.text))

        result = dict()
        result['name'] = unitName
        result['beds'] = unitBeds
        result['baths'] = unitBaths
        result['footage'] = unitFootage
        result['rent'] = unitRent

        yield result

def grid_list(soup):

    list_container = soup.find('ul', {'class': re.compile('plan')})
    list_items = list_container.find_all('li')
    for li in list_items:
        unitName = None
        unitBeds = None
        unitBaths = None
        unitFootage = None
        unitRent = None
        unitAvailability = None

        # get name
        nameContainer = li.find('h2', {'class': re.compile('title')})
        if nameContainer:
            unitName = str(nameContainer.text).strip()

        # contains bed bath and footage
        bbft_container = li.find('p', {'class': re.compile('plan')})
        bbft_text = str(bbft_container.text).strip()
        bbft_text = bbft_text.replace('Studio', '0 bed')
        bbft_list = bbft_text.split('|')
        bb_text = bbft_list[0] + bbft_list[1]

        # get bed and bath
        bbmatch = re.search('([0-9]) bed[s]?.*([0-9]) bath[s]?', bb_text, re.IGNORECASE)
        if bbmatch:
            unitBeds = int(bbmatch.group(1))
            unitBaths = int(bbmatch.group(2))

        # get square footage
        if len(bbft_list) > 2:
            ft_text = bbft_list[2]
            unitFootage = feet_normalize(ft_text)

        # get rent
        rentContainer = li.find('p', string=re.compile('$'))
        if rentContainer:
            unitRent = rent_normalize(str(rentContainer.text))

        result = dict()
        result['name'] = unitName
        result['beds'] = unitBeds
        result['baths'] = unitBaths
        result['footage'] = unitFootage
        result['rent'] = unitRent

        yield result

def grid_table(soup):

    list_container = soup.find('ul', {'class': re.compile('plan')})
    list_items = list_container.find_all('li')
    for li in list_items:
        unitName = None
        unitBeds = None
        unitBaths = None
        unitFootage = None
        unitRent = None
        unitAvailability = None

        # get name
        nameContainer = li.find('h2', {'class': re.compile('title')})
        if nameContainer:
            unitName = str(nameContainer.text).strip()

        # contains bed bath and footage
        bbft_container = li.find('p', {'class': re.compile('info')})
        bbft_text = str(bbft_container.text).strip()
        bbft_text = bbft_text.replace('Studio', '0 bed')
        bbft_list = bbft_text.split('|')
        bb_text = bbft_list[0] + bbft_list[1]

        # get bed and bath
        bbmatch = re.search('([0-9]) bed[s]?.*([0-9]) bath[s]?', bb_text, re.IGNORECASE)
        if bbmatch:
            unitBeds = int(bbmatch.group(1))
            unitBaths = int(bbmatch.group(2))

        # get square footage
        if len(bbft_list) > 2:
            ft_text = bbft_list[2]
            unitFootage = feet_normalize(ft_text)

        # get rent
        rentContainer = li.find('p', string=re.compile('$'))
        if rentContainer:
            unitRent = rent_normalize(str(rentContainer.text))

        result = dict()
        result['name'] = unitName
        result['beds'] = unitBeds
        result['baths'] = unitBaths
        result['footage'] = unitFootage
        result['rent'] = unitRent

        yield result

# TABLE

def table_default(soup):

    nameColNum = None
    bathColNum = None
    bedColNum = None
    feetColNum = None
    rentColNum = None

    # attempt to infer bed count from name
    #   i.e. 'studio' = 0
    INFER_BED = False

    headerContainer = soup.find('thead')
    headers = headerContainer.find_all('th')
    for index, th in enumerate(headers):
        th_text = str(th.text).lower()

        if is_name_header(th_text):
            nameColNum = index

        elif 'bed' in th_text:
            bedColNum = index

        elif 'bath' in th_text:
            bathColNum = index

        elif 'ft' in th_text:
            feetColNum = index

        elif 'rent' in th_text or 'price' in th_text:
            rentColNum = index

    if bedColNum == None:
        INFER_BED = True

    tableContainer = soup.find('tbody')
    rows = tableContainer.find_all('tr')

    for row in rows:
        unitName = None
        unitBeds = None
        unitBaths = None
        unitFootage = None
        unitRent = None
        unitAvailability = None

        cells = row.find_all('td')
        cells_data = [str(x.text).lower() for x in cells]

        if bathColNum:
            bath_string = cells_data[bathColNum]
            unitBaths = bath_normalize(bath_string)

        if bedColNum:
            bed_string = cells_data[bedColNum]
            unitBeds = bed_normalize(bed_string)

        if nameColNum:
            unitName = cells_data[nameColNum]
            if INFER_BED:
                unitBeds = bed_normalize(cells_data[nameColNum])

        if feetColNum:
            unitFootage = feet_normalize(cells_data[feetColNum])

        if rentColNum:
            unitRent = rent_normalize(cells_data[rentColNum])

        result = dict()
        result['name'] = unitName
        result['beds'] = unitBeds
        result['baths'] = unitBaths
        result['footage'] = unitFootage
        result['rent'] = unitRent

        yield result

# TABLIST

def tablist_default(soup):

    # find container for each floorplan tab

    def is_tablist(role):
        return role and re.compile("tablist").search(role)

    tablist = soup.find(role=is_tablist)
    parent_container = tablist.parent
    content_container = parent_container.find("div", {"class": re.compile("content")})
    tabs = content_container.find_all('div')

    # select a floorplan
    for tab in tabs:
        # intitalize default datapoints
        planName = None
        planAvailability = None
        planBeds = None
        planBaths = None
        planRent = None
        planFootage = None

        # find name
        plan_name_container = tab.find('h2', {"class": re.compile("name")})
        if plan_name_container:
            planName = str(plan_name_container.text).strip()

        # find availability
        availability_container = tab.find('div', {"class": re.compile("avail")})
        if availability_container:
            availavility_text = str(availability_container.text).strip()
            if ("Call" in availavility_text) or ("Contact" in availavility_text):
                planAvailability = False
            else:
                planAvailability = True

        # find table data (beds, baths, rent, footage)
        table_data_container = tab.find('table')
        if table_data_container:
            # find bed container
            bed_td = table_data_container.find("td", string=re.compile("Bed"))
            if bed_td:
                bed_container = bed_td.parent
                container_tds = bed_container.find_all("td")
                bed_value = str(container_tds.pop().text)
                planBeds = bed_normalize(bed_value)

            # find bath container
            bath_td = table_data_container.find("td", string=re.compile("Bath"))
            if bath_td:
                bath_container = bath_td.parent
                container_tds = bath_container.find_all("td")
                bath_value = str(container_tds.pop().text)
                planBaths = bath_normalize(bath_value)

            # find rent container
            rent_td = table_data_container.find('td', {'data-selenium-id': re.compile('rent', re.IGNORECASE)})
            if rent_td:
                planRent = rent_normalize(str(rent_td.text))

            # find footage container
            feet_td = table_data_container.find('td', {'data-selenium-id': re.compile('ft', re.IGNORECASE)})
            if feet_td:
                planFootage = feet_normalize(str(feet_td.text))


        if planName or planAvailability:
            result = dict()
            result['name'] = planName
            result['beds'] = planBeds
            result['baths'] = planBaths
            result['footage'] = planFootage
            result['rent'] = planRent
            result['availability'] = planAvailability

            yield result