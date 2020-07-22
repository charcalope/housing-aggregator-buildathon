import re

def is_name_header(header_string):
    if ('plan' in header_string) or ('name' in header_string) or ('type' in header_string):
        return True
    return False

def bed_normalize(bed_string):
    if "tudio" in bed_string:
        return 0
    else:
        match = re.search('([0-9])', bed_string)
        if match:
            match = match.group(1)
            return int(match)
        return None

def bath_normalize(bath_string):
    match = re.search('([0-9])', bath_string)
    if match:
        match = match.group(1)
        return int(match)
    return None

def feet_normalize(feet_string):
    feet_string = feet_string.replace(',', '')
    match = re.search('([0-9]+)', feet_string)
    if match:
        match = match.group(1)
        return int(match)
    return None

# return a (bed_num, bath_num) tuple
def normalize_combined_bed_bath(combined_string):
    combined_string = combined_string.strip()
    if 'Studio' in combined_string:
        combined_string = combined_string.replace('Studio', '0')
    char_list = list(combined_string)
    bed_nums = int(char_list[0])
    bath_nums = int(char_list.pop())
    return (bed_nums, bath_nums)

def rent_normalize(rent_string):
    rent_string = rent_string.replace(',', '')
    match = re.search('([0-9]+)', rent_string)
    if match:
        match = match.group(1)
        return int(match)
    return None