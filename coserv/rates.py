from datetime import datetime
from chrome import driver
from db import cur, conn
import datetime
import pandas as pd
import cloudscraper

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
a = scraper.get("https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate").text

try:
    driver.get("https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate")
    driver.save_screenshot('coserv/ss.png')
    html=driver.page_source

    table=pd.read_html(a)
    # frames = [table[0], table[1]]
    # result=pd.concat(frames,ignore_index=True)
    print(table)
    # table = driver.find_element_by_xpath("/html/body/main/div/div/article/section[1]/div/div[1]/table")
    table['new_column'] = table['column1'] + table['column2']
    print(table)

    tbl = table.text.split('\n')
    driver.quit()    
except: 
    driver.quit()
    


query = """INSERT INTO public.rate_test(a) VALUES (%s);"""
for row in a:
    cur.execute(query, (row,))
conn.commit()



# if len(a) == 18:
#     stdmnth1 = datetime.strptime(a[2], '%B %Y')
#     stdmnth2 = datetime.strptime(a[13], '%B %Y')
#     stdmnth1kwh1 = a[5].lstrip()[3:11]
#     stdmnth1kwh2 = a[8].lstrip()[3:11]
#     stdmnth1kwh3 = a[11].lstrip()[3:11]
#     stdmnth2kwh = a[10].lstrip()[3:11]

# else:
#     stdmnth1 = datetime.strptime(a[2], '%B %Y')
#     stdmnth2 = datetime.strptime(a[7], '%B %Y')
#     stdmnth1kwh = a[5].lstrip()[3:11]
#     stdmnth2kwh = a[10].lstrip()[3:11]

# try:
#     driver.get("https://support.coserv.com/hc/en-us/articles/360009223233-Time-of-Use-Residential-Closed-")
#     table = driver.find_element_by_xpath("/html/body/main/div/div/article/section[1]/div/div[1]/div/div/div/table")
#     a = table.text.split('\n')
# except: 
#     driver.quit()


# driver.quit()

# stdmnth1 = datetime.strptime(a[2], '%B %Y')
# stdmnth2 = datetime.strptime(a[7], '%B %Y')
# stdmnth1kwh = a[5].lstrip()[3:11]
# stdmnth2kwh = a[10].lstrip()[3:11]

# peakmnth1 = datetime.strptime(a[2], '%B %Y')
# peakmnth2 = datetime.strptime(a[10], '%B %Y')
# peakkwh1 = a[5].lstrip()[3:11]
# peakkwh2 = a[13].lstrip()[3:11]
# offpeakkwh1 = a[6].lstrip()[16:25]
# offpeakkwh2 = a[14].lstrip()[16:25]

# # Insert values 
# values1 = peakmnth1.year, peakmnth1.month, stdmnth1kwh, offpeakkwh1, peakkwh1
# values2 = peakmnth2.year, peakmnth2.month, stdmnth2kwh, offpeakkwh2, peakkwh2

# query = """INSERT INTO public.rates(
#     yr, mnth, reg_rate, off_peak_use_rate, peak_use_rate)
#     VALUES (%s, %s, %s, %s, %s)
#     ON CONFLICT (yr, mnth) DO UPDATE SET
#         reg_rate = excluded.reg_rate, off_peak_use_rate = excluded.off_peak_use_rate, peak_use_rate = excluded.peak_use_rate ;"""
# cur.execute(query, values1)
# cur.execute(query, values2)
# conn.commit()