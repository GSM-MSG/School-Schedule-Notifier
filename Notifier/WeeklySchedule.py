from datetime import datetime, timedelta
from dateutil.relativedelta import *
from ScheduleCore import get_today, send_webhook, fetch_school_schedule, json_to_school_schedule_string

def fetch_weekly_school_schedule():
  today = get_today()
  current_weekday = today.weekday()

  days_until_monday = (current_weekday + 1) % 7
  delta_days = timedelta(days=days_until_monday)

  this_monday = today - delta_days

  days_until_sunday = (6 - current_weekday) % 7
  delta_days = timedelta(days=days_until_sunday)

  this_sunday = today + delta_days

  start_date = f"{this_monday.strftime('%Y%m%d')}"
  end_date = f"{this_sunday.strftime('%Y%m%d')}"
  return fetch_school_schedule(start_date=start_date, end_date=end_date)

res = fetch_weekly_school_schedule()
schedule_string = json_to_school_schedule_string(res.json())
send_webhook(title="이번주 학사일정", content=schedule_string)