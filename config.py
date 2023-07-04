import os
import json
from dotenv import load_dotenv

load_dotenv()


with open(os.path.join(os.environ.get('CONFIG_PATH'), os.environ.get('CONFIG_FILE_NAME'))) as config_file:
    config_dict = json.load(config_file)

print('- in config.py -')

class ConfigBase:

    def __init__(self):
        self.CONFIG_TYPE = os.environ.get('CONFIG_TYPE')
        self.SECRET_KEY = config_dict.get('SECRET_KEY')

        #Email stuff
        self.MAIL_SERVER = config_dict.get('MAIL_SERVER_MSOFFICE')
        self.MAIL_PORT = config_dict.get('MAIL_PORT')
        self.MAIL_USE_TLS = True
        self.MAIL_USERNAME = config_dict.get('EMAIL')
        self.MAIL_PASSWORD = config_dict.get('EMAIL_PASSWORD')

        self.PROJ_ROOT_PATH = os.environ.get('PROJ_ROOT_PATH')
        self.PROJ_DB_PATH = os.environ.get('PROJ_DB_PATH')
        self.PROJ_LOGS_DIR = os.path.join(self.PROJ_ROOT_PATH, 'logs')
        self.SQL_URI =  f"sqlite:///{self.PROJ_DB_PATH}socialAggregator.db"

        self.TWITTER_BEARER_TOKEN = config_dict.get('TWITTER_BEARER_TOKEN')
        self.TWITTER_ID = config_dict.get('TWITTER_ID')
        self.TWITTER_USERNAME = config_dict.get('TWITTER_USERNAME')
        self.TWITTER_URL_BASE = f"https://twitter.com/{self.TWITTER_USERNAME}/status/"

        self.STACK_OVERFLOW_ID = config_dict.get('STACK_OVERFLOW_ID')
        self.STACK_OVERFLOW_URL = f"https://api.stackexchange.com/2.2/users/{self.STACK_OVERFLOW_ID}/questions?site=stackoverflow.com"
        self.GITHUB_USERNAME = config_dict.get('GITHUB_USERNAME')
        self.GITHUB_TOKEN = config_dict.get("GITHUB_TOKEN")
        self.SEND_DATA = os.environ.get('SEND_DATA')
        self.API_ENDPOINT_TESTER_PASSWORD = config_dict.get('API_ENDPOINT_TESTER_PASSWORD')
        self.API_IAMNICK_PASSWORD = config_dict.get('API_IAMNICK_PASSWORD')

        self.HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND = config_dict.get('HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND')
        self.USE_MIRROR_DF = config_dict.get('USE_MIRROR_DF')

class ConfigLocal(ConfigBase):

    def __init__(self):
        super().__init__()
        
    DEBUG = True
    API_URL = config_dict.get('UPDATE_SOCIAL_POSTS_API_URL_LOCAL')
    API_ENDPOINT_TESTER_URL = config_dict.get('API_ENDPOINT_TESTER_URL')
    
            

class ConfigDev(ConfigBase):

    def __init__(self):
        super().__init__()

    DEBUG = True
    API_URL = config_dict.get('UPDATE_DESTINATION_URL_DEV')
    API_ENDPOINT_TESTER_URL = config_dict.get('API_ENDPOINT_TESTER_URL')
            

class ConfigProd(ConfigBase):

    def __init__(self):
        super().__init__()

    DEBUG = False
    API_URL = config_dict.get('UPDATE_SOCIAL_POSTS_API_URL_PRODUCTION')
    API_ENDPOINT_TESTER_URL = config_dict.get('API_ENDPOINT_TESTER_URL')


################################
# from config import config    #
# where config is instantiated #
################################
if os.environ.get('CONFIG_TYPE')=='local':
    config = ConfigLocal()
elif os.environ.get('CONFIG_TYPE')=='dev':
    config = ConfigDev()
elif os.environ.get('CONFIG_TYPE')=='prod':
    config = ConfigProd()