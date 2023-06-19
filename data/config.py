import os
from dotenv import load_dotenv



load_dotenv()
BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
DEV_MOD = str(os.getenv('DEV_MOD'))
TABLE = str(os.getenv('TABLE'))
SPREADSHEET_ID = str(os.getenv('SPREADSHEET_ID'))
