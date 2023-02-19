from config import config
from models import SocialPosts, sess, engine, text
from datetime import date, datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
import os
import pandas as pd


if not os.path.exists(os.path.join(config.PROJ_ROOT_PATH,'logs')):
    os.mkdir(os.path.join(config.PROJ_ROOT_PATH,'logs'))


#Setting up Logger
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

#initialize a logger
logger_data_service = logging.getLogger(__name__)
logger_data_service.setLevel(logging.DEBUG)
# logger_terminal = logging.getLogger('terminal logger')
# logger_terminal.setLevel(logging.DEBUG)

#where do we store logging information
file_handler = RotatingFileHandler(os.path.join(config.PROJ_ROOT_PATH,'logs','social_agg_data_service.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

#where the stream_handler will print
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

logger_data_service.addHandler(file_handler)
logger_data_service.addHandler(stream_handler)


def get_social_activity_for_df():
    logger_data_service.info(f"- Inside get_social_activity_for_df  -")
    logger_data_service.info(f"- config.SQL_URI: {config.SQL_URI}  -")

    ############################################################################
    # This function makes the df that get's sent either by:                    #
    # 1. useing a mirror dataframe to keep track of the (USE_MIRROR_DF = True) #
    # 2. setting a number of historical days to send (USE_MIRROR_DF = False \  #
    #     and HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND = ?)                         #
    ############################################################################

    if config.USE_MIRROR_DF:
        logger_data_service.info(f"-***** USE_MIRROR_DF *****-")
        if os.path.exists(os.path.join(config.PROJ_DB_PATH,'df_mirror.pkl')):
            logger_data_service.info(f"- df_mirror Exists  -")
            df_from_db = get_db_social_activity()
            df_existing = pd.read_pickle(os.path.join(config.PROJ_DB_PATH,'df_mirror.pkl'))
            ### make unique index from network_post_id, social_name, title
            df_from_db.set_index(['network_post_id', 'social_name','title'], inplace=True)
            df_existing.set_index(['network_post_id', 'social_name','title'], inplace=True)

            df_to_add = df_from_db[~df_from_db.index.isin(df_existing.index)]

            #Append to df_exisitng
            df_mirror = pd.concat([df_existing, df_to_add]).reset_index()
            #df_existing to pickle
            df_mirror.to_pickle(os.path.join(config.PROJ_DB_PATH,'df_mirror.pkl'))

            df_to_add.reset_index(inplace=True)
        
        else:# - All data is new
            logger_data_service.info(f"- df_mirror NOT exists  -")
            df_to_add = get_db_social_activity()
            df_to_add.to_pickle(os.path.join(config.PROJ_DB_PATH,'df_mirror.pkl'))


        logger_data_service.info(f"- df_to_add.columns:   -")
        logger_data_service.info(df_to_add.columns)
        logger_data_service.info(f"- df_to_add Length:   -")
        logger_data_service.info(len(df_to_add))

        new_dict = df_to_add.to_dict('records')

    else:# send HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND
        logger_data_service.info(f"-***** HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND *****-")
        send_hist_days = config.HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND
        df_from_db = get_db_social_activity()

        #make new column with post date in datetime format
        df_from_db['post_datetime']= pd.to_datetime(df_from_db['post_date'])

        print("lenght of df_form_db: ", len(df_from_db))

        today = datetime.now()
        start_date = today + timedelta(config.HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND * -1)

        df_from_db_subset = df_from_db[df_from_db["post_datetime"]> start_date]

        df_from_db_subset.drop(columns=["post_datetime"], inplace=True)


        logger_data_service.info(f"- df_to_add.columns:   -")
        logger_data_service.info(df_from_db_subset.columns)
        logger_data_service.info(f"- df_to_add Length:   -")
        logger_data_service.info(len(df_from_db_subset))

        new_dict = df_from_db_subset.to_dict('records')



    return new_dict


def get_db_social_activity():
    # Check for duplicate tweets to remove

    base_query = sess.query(SocialPosts)
    df_existing = pd.read_sql(text(str(base_query)), engine.connect())

    table_name = 'social_posts_'
    cols = list(df_existing.columns)
    for col in cols:
        if col[:len(table_name)] == table_name:
            df_existing = df_existing.rename(columns=({col: col[len(table_name):]}))

    return df_existing