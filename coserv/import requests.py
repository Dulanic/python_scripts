import requests
import pandas as pd

url =  'https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]

new = df[[2]].copy()
print(df)
print(new)