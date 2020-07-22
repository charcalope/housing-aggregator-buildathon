import requests, csv

response = requests.get('https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Zoned_Development_Capacity_Layers_2016/FeatureServer/2/query?where=MF_UNITS%20%3E%3D%2010%20AND%20MF_UNITS%20%3C%3D%20999&outFields=*&returnGeometry=false&outSR=4326&f=json')
data = response.json()
units = [x['attributes'] for x in data['features']]

# building name = PROP_NAME
# neighborhood = UV_NAME

addresses = [x['ADDRESS'] for x in units]
adds2 = []
for addy in addresses:
    if addy:
        addy = addy.lower()
        add_words = addy.split()
        addy2 = ' '.join(add_words)
        adds2.append(addy2)
    else:
        adds2.append(None)

addresses = adds2

neighborhoods = [x['UV_NAME'] for x in units]
building_names = [x['PROP_NAME'] for x in units]

print(units[125])

apt_data = list(zip(addresses, neighborhoods, building_names))

with open('../data/misc_apt_data.csv', 'w') as csvfile:
    fieldnames = ['address', 'neighborhood', 'building_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for apt_dp in apt_data:
        writer.writerow({'address': apt_dp[0],
                         'neighborhood': apt_dp[1],
                         'building_name': apt_dp[2]})

