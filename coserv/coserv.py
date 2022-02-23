#!/home/dulanic/python_scripts/coserv/venv/bin/python3.10
from settings import timestamp, ConfigSet, cleardir
from chrome import driver, WebDriverWait, EC, By
from db import cur, conn
import time
from datetime import datetime as dt
from zoneinfo import ZoneInfo
import os.path
from pathlib import Path
import csv, regex, sys

t0 = time.time()

cleardir(getattr(ConfigSet,'dl_folder'))

def ts():
    date_time = dt.now().astimezone(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d %H:%M:%S")
    return date_time

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

def tiny_file_rename(nn, dl_folder):
    filename = max([f for f in os.listdir(dl_folder)], key=lambda xa: \
                   os.path.getctime(os.path.join(dl_folder, xa)))
    os.rename(os.path.join(dl_folder, filename), os.path.join(dl_folder, nn))


cur.execute("SELECT case when count(*) = 0 then '2019-08-01' else max(startdatetime) - INTERVAL '1 DAY'  end FROM public.coserv_cost;")
max_dt = cur.fetchone()[0]
start_dt = str(int(max_dt.timestamp())) + '000'
end_dt = str(int(t0)) + '000'
url_dl = getattr(ConfigSet,'url') + '&startDate=' + start_dt + '&endDate=' + end_dt + getattr(ConfigSet,'url_trail')
c_ct = 0
fn = os.path.basename(__file__)
v = []

# Go to page to login
try:
    driver.get('https://coserv.smarthub.coop/Login.html')
    driver.save_screenshot("screenshot.png")
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,'LoginSubmitButton')))
    driver.find_element(By.ID,'LoginUsernameTextBox').send_keys(getattr(ConfigSet,'clogin'))
    driver.find_element(By.ID,'LoginPasswordTextBox').send_keys(getattr(ConfigSet,'cpass'))
    driver.save_screenshot("screenshot1.png")
    button.click()
    driver.save_screenshot("screenshot2.png")
    WebDriverWait(driver, 20).until(EC.title_is('SmartHub - Home'))
    driver.get(url_dl)
    driver.save_screenshot("screenshot3.png")
except:
    driver.quit()
    print("Failed to pull CoServ data")
    exit()

path = Path(getattr(ConfigSet,'dl_folder'))

for i in range(10):
    if any(path.glob('green*.csv')):
        break
    else:
        if i == 9:
            print (timestamp() + 'File Not found after 10 seconds')
            sys.exit()
        time.sleep(1)

# Rename file
tiny_file_rename(getattr(ConfigSet,'nn'), getattr(ConfigSet,'dl_folder'))

# Close browser cleanly
driver.quit()

with open(getattr(ConfigSet,'file_loc'), 'r') as readFile:
    totrow = sum(1 for line in readFile)

# Now import to list since csv downloaded..

coserv_list = list()
rowct = 0

with open(getattr(ConfigSet,'file_loc')) as f:
    with open(getattr(ConfigSet,'tmp_file_loc'), 'w') as out:
        for line in f:
            if regex.match(r"^\s[0-9]{4}", line):
                out.write(line.lstrip())

# if the destination file already exists.

os.remove(getattr(ConfigSet,'file_loc'))
os.rename(getattr(ConfigSet,'tmp_file_loc'), getattr(ConfigSet,'file_loc'))

# Load file to list

with open(getattr(ConfigSet,'file_loc'), 'r') as readFile:
    reader = csv.reader(readFile)
    for row in reader:
        coserv_list.append(row)

[j.pop(3) for j in coserv_list]
[j.pop(2) for j in coserv_list]

for item in coserv_list:
    c_ct += 1
    query = \
        """INSERT INTO public.coserv(
    dates, "kWh")
    VALUES (%s, %s)
    ON CONFLICT (dates)
        DO UPDATE SET
        "kWh" = excluded."kWh";"""
    values = item
    cur.execute(query, values)
    conn.commit()

cur.execute("select max(left(dates,16)::timestamp) from coserv;")
max_dt1 = cur.fetchone()[0]
t1 = time.time()
rt = str(round((t1 - t0), 3))
print (f"{ts()} - {fn} - Total of {c_ct} record(s) upserted from {max_dt} to {max_dt1} in {rt} seconds to CoServ tables")
