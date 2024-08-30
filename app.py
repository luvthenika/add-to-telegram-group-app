from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError
import time
import random
api_id = '*********' # int value
api_hash = '**********'  
name = "my_session"

contacts = [
   {
    "firstName": "*****",
    "lastName": "**********",
    "phoneNumber": "******",
    
  }
]

with TelegramClient('session_name', api_id, api_hash) as client:
    input_contacts = []
    for contact in contacts:
        input_contacts.append(types.InputPhoneContact(
            client_id=random.randrange(-2**63, 2**63),
            phone=contact['phoneNumber'],
            first_name=contact['firstName'],
            last_name=contact['lastName']
        ))

    result = client(functions.contacts.ImportContactsRequest(
        contacts=input_contacts
    ))

    user_ids = [user.id for user in result.users]
    print(user_ids)

import asyncio
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest

async def invite_users(client, chat_id, user_ids):
    while user_ids:
        try:
            batch = user_ids[:100] 
            user_ids = user_ids[100:] 
            result = await client(InviteToChannelRequest(
                chat_id,
                batch
            ))
            print(result.stringify())
            await asyncio.sleep(20) 
        except FloodWaitError as e:
            wait_time = e.seconds
            print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
            await asyncio.sleep(wait_time)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

chat_id = '*******' #int value
with TelegramClient('session_name', api_id, api_hash) as client:
    client.loop.run_until_complete(invite_users(client, chat_id, user_ids))