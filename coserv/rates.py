
import requests
import lxml.html as lh
import pandas as pd
from dateutil.parser import parse
import re

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

url =  'https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate'

#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

c = 0

i = ['Base rate per kWh', 'First 700 kWh', 'MINUS the PCRF', 'Next 300 kWh', 'Over 1000 kWh']
#monthly_cost = 


#For each row, store each first element (header) and an empty list
for t in tr_elements:
    for row in t:
        a = t.text_content()
        h = re.search("(?:[\£\$\€]{1}[,\d]+\.?\d*)",a)
        j = re.findall("(?:[\£\$\€]{1}[,\d]+\.?\d*)",a)
        if re.findall("(?:[\£\$\€]{1}[,\d]+\.?\d*)",a):
            print(1)

        if is_date(t.text_content()):
            mnth = parse(t.text_content())

        if a:
            lst = a.splitlines()
            for r in lst:
                if r in i:
                    label = r
                else:
                    try:
                        price = float(r.lstrip('$'))
                        if pcrf is not None and price is not None:
                            c = 1
                    except Exception:
                        pass
                    try:
                        if 'PCRF' in label:
                            try:
                                pcrf = float(r.lstrip('$'))
#                                if pcrf is not None:

                            except Exception:
                                pass
                        if pcrf is not None and price is not None:
                            c = 1
                    except Exception:
                        pass
        if c == 1:
            price = price - pcrf
            print(f'need to add insert...month {mnth} label {label} and price {price} ')
            c = 0
            pcrf = None
            price = None
