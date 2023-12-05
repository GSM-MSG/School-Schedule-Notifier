from discord_webhook import DiscordEmbed, DiscordWebhook
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from pytz import timezone
import requests
import os

load_dotenv()
datetime.now(timezone('Asia/Seoul'))

def send_webhook(title: str, content: str):
  webhookURL = os.getenv("WEBHOOK")

  webhook = DiscordWebhook(url=webhookURL)
  embed = DiscordEmbed(title=title, description=content, color="776AF2")
  webhook.add_embed(embed=embed)
  webhook.execute()

def fetch_school_schedule(start_date: str, end_date: str):
  neis_school_schedule_request_url = "https://open.neis.go.kr/hub/SchoolSchedule"
  params = {
    "KEY": os.getenv("NEIS"),
    "Type": "json",
    "pIndex": 1,
    "pSize": 100,
    "ATPT_OFCDC_SC_CODE": "F10",
    "SD_SCHUL_CODE": "7380292",
    "AA_FROM_YMD": start_date,
    "AA_TO_YMD": end_date
  }
  return requests.get(url=neis_school_schedule_request_url, params=params, json=True)

def json_to_school_schedule_string(json):
  try:
    _ = json["SchoolSchedule"][1]["row"]
  except KeyError:
    if json["RESULT"]["CODE"] == 'INFO-200':
      return "학사일정이 없어요"
  except:
    return "학사일정을 찾을 수 없어요"
  responseJSON = json["SchoolSchedule"][1]["row"]
  responseJSON.sort(key= lambda x : x['AA_YMD'])

  weekday_dict = {
      0: '월',
      1: '화',
      2: '수',
      3: '목',
      4: '금',
      5: '토',
      6: '일'
  }

  result = ""
  for value in responseJSON:
    event_date = date.fromisoformat(value['AA_YMD'])
    result += f"{value['AA_YMD'][-2:]} {weekday_dict[event_date.weekday()]} - {value['EVENT_NM']}\n"
  return result