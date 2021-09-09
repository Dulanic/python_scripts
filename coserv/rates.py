from datetime import datetime
from chrome import driver, WebDriverWait, EC, By
from db import cur, conn

try:
    driver.get("https://support.coserv.com/hc/en-us/articles/360009093154-Standard-Residential-Rate")
    table = driver.find_element_by_xpath("/html/body/main/div/div/article/section[1]/div/div[1]/table")
    a = table.text.split('\n')
except: 
    driver.quit()

stdmnth1 = datetime.strptime(a[2], '%B %Y')
stdmnth2 = datetime.strptime(a[7], '%B %Y')
stdmnth1kwh = a[5].lstrip()[3:11]
stdmnth2kwh = a[10].lstrip()[3:11]

try:
    driver.get("https://support.coserv.com/hc/en-us/articles/360009223233-Time-of-Use-Residential-Closed-")
    table = driver.find_element_by_xpath("/html/body/main/div/div/article/section[1]/div/div[1]/div/div/div/table")
    a = table.text.split('\n')
except: 
    driver.quit()

peakmnth1 = datetime.strptime(a[2], '%B %Y')
peakmnth2 = datetime.strptime(a[10], '%B %Y')
peakkwh1 = a[5].lstrip()[3:11]
peakkwh2 = a[13].lstrip()[3:11]
offpeakkwh1 = a[6].lstrip()[16:25]
offpeakkwh2 = a[14].lstrip()[16:25]
driver.quit()

# Insert values 
values1 = peakmnth1.year, peakmnth1.month, stdmnth1kwh, offpeakkwh1, peakkwh1
values2 = peakmnth2.year, peakmnth2.month, stdmnth2kwh, offpeakkwh2, peakkwh2

query = """INSERT INTO public.rates(
	yr, mnth, reg_rate, off_peak_use_rate, peak_use_rate)
	VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;"""
cur.execute(query, values1)
cur.execute(query, values2)
conn.commit()