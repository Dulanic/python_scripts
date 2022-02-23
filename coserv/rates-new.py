from datetime import datetime
from firefox import driver
from db import cur, conn
import calendar as cal
import pandas as pd


try:
    driver.get("https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate")
    driver.save_screenshot('coserv/ss.png')
    html=driver.page_source
    df = pd.read_html(html)
    df = df[0]
    table = driver.find_element_by_xpath("/html/body/main/div/div/article/section[1]/div/div[1]/table")    
    tbl = table.text.split('\n')
    driver.quit()    
except: 
    driver.quit()

if len(tbl) == 18:
    stdmnth1 = datetime.strptime(tbl[2], '%B %Y')
    stdmnth2 = datetime.strptime(tbl[13], '%B %Y')
    g = cal.month_name[stdmnth2.month]
    stdmnth1kwh1 = tbl[5].lstrip()[3:11]
    stdmnth1kwh2 = tbl[8].lstrip()[3:11]
    stdmnth1kwh3 = tbl[11].lstrip()[3:11]
    stdmnth2kwh = tbl[16].lstrip()[3:11]

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
values1 = stdmnth1.year, stdmnth2.month, stdmnth1kwh1, offpeakkwh1, peakkwh1, stdmnth1kwh1, stdmnth1kwh2, stdmnth1kwh3
values2 = peakmnth2.year, peakmnth2.month, stdmnth2kwh, offpeakkwh2, peakkwh2, stdmnth1kwh1, stdmnth1kwh2, stdmnth1kwh3

query = """INSERT INTO public.rates(
    yr, mnth, reg_rate, off_peak_use_rate, peak_use_rate, reg_rate_first700, reg_rate_next300, reg_rate_over1000)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (yr, mnth) DO UPDATE SET
        reg_rate = excluded.reg_rate, off_peak_use_rate = excluded.off_peak_use_rate, peak_use_rate = excluded.peak_use_rate ;"""
cur.execute(query, values1)
cur.execute(query, values2)
conn.commit()