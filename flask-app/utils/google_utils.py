from googleapiclient.discovery import build

def search_zillow(building_name):
    API_KEY = "API_KEY"
    CSE_ID = "CSE_ID"

    query = building_name + " seattle"
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CSE_ID).execute()
    if res and 'items' in res.keys():
        return res['items']
    else:
        return None

def fetch_zillow_link(building_name):
    links = search_zillow(building_name)
    if links and len(links) > 0:
        link = links[0]['link']
        return link
    else:
        return None


