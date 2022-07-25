import json
import asyncio
from datetime import date, datetime
from telethon import TelegramCLIENT
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)
import os
from dotenv import load_dotenv
load_dotenv()
WANTED_KEYS="date","message","id","edit_date","to_id"

GROUP_LINK=os.getenv("groupLink")
PHONE = os.getenv('phone')

API_ID = os.getenv('api_id')
API_HASH = os.getenv('api_hash')
USER_NAME = os.getenv('username')
CLIENT = TelegramCLIENT(USER_NAME, API_ID, API_HASH)
# Setting configuration values



# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)

# Create the CLIENT and connect

async def main(phone):
    await CLIENT.start()
    print("CLIENT Created")
    # Ensure you're authorized
    if await CLIENT.is_user_authorized() == False:
        await CLIENT.send_code_request(phone)
        while True:
            try:
                try:
                    await CLIENT.sign_in(phone, input('Enter the code: '))
                    break
                except SessionPasswordNeededError:
                    await CLIENT.sign_in(password=input('Password: '))
                    break
                except Exception as e:
                    print(e)
            except:pass
    me = await CLIENT.get_me()

    my_channel = await CLIENT.get_entity(GROUP_LINK)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await CLIENT(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            data=dict(message.to_dict())
            keys=set(WANTED_KEYS)-set(data)
            for unwanted in keys:
                if unwanted in data:
                    del data[unwanted]
            all_messages.append(data)
        offset_id = messages[len(messages) - 1].id
        
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open('channel_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder)
if __name__=="__main__":
    with CLIENT:
        CLIENT.loop.run_until_complete(main(PHONE))
