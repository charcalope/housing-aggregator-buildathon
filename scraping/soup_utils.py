def has_selenium_id(tag):
    return tag and tag.has_attr('data-selenium-id')

def combines_bed_bath(soup):
    headers = soup.find_all('th')
    for header in headers:
        text = str(header.text)
        text = text.lower()
        if ('bed' in text) and ('bath' in text):
            return True
    return False