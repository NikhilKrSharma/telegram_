import os
import sys
import logging
import configparser
import pandas as pd
from datetime import datetime
from telethon import TelegramClient


"""
level=logging.CRITICAL  # won't show errors (same as disabled)
level=logging.ERROR     # will only show errors that you didn't handle
level=logging.WARNING   # will also show messages with medium severity, such as internal Telegram issues
level=logging.INFO      # will also show informational messages, such as connection or disconnections
level=logging.DEBUG     # will show a lot of output to help debugging issues in the library
"""


if not os.path.isdir('logs'):
    os.makedirs('logs')

if not os.path.isdir('data'):
    os.makedirs('data')

# SETTING UP THE LOGGING 
# CURRENT_WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_WORKING_DIR = os.getcwd()
file_name = str(datetime.today()).replace(':', '-') + '.log'
logging.basicConfig(
    filename=(CURRENT_WORKING_DIR + f"/logs/{file_name}"), 
    level=logging.ERROR,
    filemode='w', 
    format='%(name)s - %(levelname)s - %(lineno)d - %(message)s'
)
logger = logging.getLogger()
logger.info('Logger Initialized Successfully')



# READING CREDENTIALS FROM THE CONFIGURATION FILE
config_file_name = 'config.ini'
try:
    logger.info('Reading Configuration File')
    config = configparser.ConfigParser()
    config.read(config_file_name)
    logger.info('Configuration file read successfully.')
    account_credentials = config['ACCOUNT CREDENTIALS']
    api_id = account_credentials['API_ID']
    api_hash = account_credentials['API_HASH']
    group_name = account_credentials['CHANNEL_NAME']
except Exception as e:
    logger.error(e)
    logger.error("Exception occurred", exc_info=True)
    sys.exit(0)



# /////////////////////////////////////////////////////////////////////////////
# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('tele-session', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))

# /////////////////////////////////////////////////////////////////////////////

client = TelegramClient('tele-session', api_id, api_hash)

# /////////////////////////////////////////////////////////////////////////////

async def get_my_details():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

with client:
    a = client.loop.run_until_complete(get_my_details())


# /////////////////////////////////////////////////////////////////////////////

async def get_group_list():
    # You can print all the dialogs/conversations that you are part of:
    data = []
    save_location = 'data/group_list.csv'
    async for dialog in client.iter_dialogs():
        data.append((dialog.name, str(dialog.id)))

    df = pd.DataFrame(data=data, columns=['Channel Name', 'Channel ID'])
    df.to_csv(save_location, index=False)

with client:
    a = client.loop.run_until_complete(get_group_list())


# /////////////////////////////////////////////////////////////////////////////

async def get_messages(group_name):
    # You can print the message history of any chat:
    chat_data = []
    chat_save_location = f'data/{group_name}_chat_data.csv'
    async for message in client.iter_messages(
        group_name,
        limit=3000,
        offset_date=datetime.today(),      # (`datetime`): Offset date (messages *previous* to this date will be retrieved). Exclusive.
        search=None,        # (`str`): The string to be used as a search query.
        filter=None,        # (:tl:`MessagesFilter` | `type`): The filter to use when returning messages. For instance, :tl:`InputMessagesFilterPhotos` would yield only messages containing photos.
        from_user=None,     # (`entity`): Only messages from this entity will be returned.
        reverse=False,      # (`Bool`): If set to `True`, the messages will be returned in reverse order (from oldest to newest, instead of the default newest to oldest)
    ):
            chat_data.append((message.id, message.text))

    df = pd.DataFrame(data=chat_data, columns=['Message ID', 'Message Text'])
    df.to_csv(chat_save_location, index=False)


with client:
    a = client.loop.run_until_complete(get_messages(group_name=group_names[-1]))

group_names = ['cryptodakurobinhooders', 'Satoshi_club', 'cryptodakuofficial', 'InfinityGainzz', 'CryptoRobinhooders']