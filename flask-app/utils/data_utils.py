import pandas as pd
import random

def load_units():
    df = pd.read_csv('data/unit_db_init.csv')
    # filter by has rent and footage
    df = df.dropna(subset=['footage', 'rent'])
    dicts = df.to_dict('records')
    return dicts

def load_10():
    dict_pop = load_units()
    sample = random.sample(dict_pop, 10)
    return sample

def fetch_misc_data(building_id):
    address = fetch_address(building_id)

    if address:
        try:
            # preprocess to match existing address formatting
            address = address.lower()
            add_words = address.split()
            address = ' '.join(add_words)

            # load misc data
            df = pd.read_csv('data/misc_apt_data.csv')
            # convert data to dicts
            dicts = df.to_dict('records')
            # find index of given address
            addresses = list(df['address'])
            index = addresses.index(address)
            data = dicts[index]

            return (data['neighborhood'], data['building_name'])
        except:
            return None
    else:
        return None

def fetch_address(building_id):
    df = pd.read_csv('data/address_db_init_UPDATED.csv', header=None)
    addresses = list(df[1])
    # find index of desired address
    ids = list(df[0])
    try:
        index = ids.index(building_id)
        address = addresses[index]
        return address
    except:
        return None