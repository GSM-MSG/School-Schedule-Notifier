from datetime import datetime
from dateutil.relativedelta import *
from ScheduleCore import send_webhook, fetch_school_schedule, json_to_school_schedule_string

def fetch_monthly_school_schedule():
  today = datetime.today()

  this_month_first_date = datetime(today.year, today.month, 1)

  next_month = datetime(today.year, today.month, 1) + relativedelta(months=1)
  this_month_last_date = next_month + relativedelta(seconds=-1)

  start_date = f"{this_month_first_date.strftime('%Y%m%d')}"
  end_date = f"{this_month_last_date.strftime('%Y%m%d')}"
  return fetch_school_schedule(start_date=start_date, end_date=end_date)

res = fetch_monthly_school_schedule()
schedule_string = json_to_school_schedule_string(res.json())
send_webhook(title=f"{datetime.today().month}월 학사일정", content=schedule_string)
