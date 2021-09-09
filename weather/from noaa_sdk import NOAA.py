from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, date, timezone
CHICAGO = ZoneInfo("America/Chicago")

today = datetime.today().astimezone(CHICAGO)
print(today)