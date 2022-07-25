import json
import os
import re
from typing import *
import datetime
from rules import *
from typing import *
from selenium.webdriver import ChromeOptions
from dotenv import load_dotenv
load_dotenv()
CHROME_DRIVER_PATH=os.getenv("CHROME_APP_PATH")

EMAIL = "email"
PASSWORD = "password"
DATA = "data"
FILE_NAME = "./data.json"
POSTSTODAY = "postsToday"
DATEJSON_ENCODING = "%Y-%m-%dT%H:%M:%S.%fZ"
LASTPOSTTIME = "lastTimePost"
POSTSMESSAGENUM="posts_num"
BLOCKING_STATE="blocking_state"


CHROME_OPTIONS = ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
CHROME_OPTIONS.add_experimental_option("prefs", prefs)
CHROME_OPTIONS.add_experimental_option("detach", True)
CHROME_OPTIONS.add_argument("--disable-infobars")
CHROME_OPTIONS.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2  # 1:allow, 2:block
})
CHROME_OPTIONS.add_argument("--log-level=3")
    


def convert_str2time(time:str):
    return datetime.datetime.strptime(time,DATEJSON_ENCODING)
def convert_time2str(time:datetime.datetime):
    return datetime.datetime.strftime(time,DATEJSON_ENCODING)   

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002500-\U00002BEF"  # chinese char
                           u"\U00002702-\U000027B0"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U00010000-\U0010ffff"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"  # dingbats
                           u"\u3030"
                           "]+", re.UNICODE)
FaceBook_pattern = re.compile("((https://)?((www|web|m)\.)?facebook\.com/groups/?)?(\d+)/?")


