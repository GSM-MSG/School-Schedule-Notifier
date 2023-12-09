from dateutil.relativedelta import *
from ScheduleCore import get_today, send_webhook, fetch_school_schedule, json_to_school_schedule_string

def fetch_daily_school_schedule():
  today = get_today()
  start_date = f"{today.strftime('%Y%m%d')}"
  end_date = f"{today.strftime('%Y%m%d')}"
  return fetch_school_schedule(start_date=start_date, end_date=end_date)

res = fetch_daily_school_schedule()
schedule_string = json_to_school_schedule_string(res.json())
send_webhook(title="오늘 학사일정", content=schedule_string)