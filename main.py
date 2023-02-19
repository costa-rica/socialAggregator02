from apscheduler.schedulers.background import BackgroundScheduler
import json
import requests
from datetime import datetime, timedelta
import os
from config import config
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
from twitter import twitter_scheduler_update
from stack_overflow import stackoverflow_scheduler_update
from github import github_scheduler_update

# import subprocess
import time
from data_service import get_social_activity_for_df
from models import SocialPosts, sess, engine


if not os.path.exists(os.path.join(config.PROJ_ROOT_PATH,'logs')):
    os.mkdir(os.path.join(config.PROJ_ROOT_PATH,'logs'))


#Setting up Logger
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
formatter_terminal = logging.Formatter('%(asctime)s:%(filename)s:%(name)s:%(message)s')

#initialize a logger
logger_init = logging.getLogger(__name__)
logger_init.setLevel(logging.DEBUG)

#where do we store logging information
file_handler = RotatingFileHandler(os.path.join(config.PROJ_ROOT_PATH,'logs','social_agg_schduler.log'), mode='a', maxBytes=5*1024*1024,backupCount=2)
file_handler.setFormatter(formatter)

#where the stream_handler will print
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter_terminal)

logger_init.addHandler(file_handler)
logger_init.addHandler(stream_handler)


def scheduler_funct():
    logger_init.info(f"- Started Scheduler on {datetime.today().strftime('%Y-%m-%d %H:%M')}-")
    logger_init.info(f"- API dest for social activity to destination: {config.API_URL}-")
    logger_init.info(f"- API dest for social activity to destination: {config.CONFIG_TYPE}-")
    scheduler = BackgroundScheduler()

    job_collect_socials = scheduler.add_job(social_aggregator,'cron', hour='*', minute='52', second='29')#Testing
    # job_collect_socials = scheduler.add_job(social_aggregator,'cron', day='*', hour='06', minute='01', second='05')#Production

    scheduler.start()

    while True:
        pass


def social_aggregator():
    logger_init.info(f"- Started social_aggregator on {datetime.today().strftime('%Y-%m-%d %H:%M')}-")
    logger_init.info(f"- config.USE_MIRROR_DF: {config.USE_MIRROR_DF}, type: {type(config.USE_MIRROR_DF)} -")
    logger_init.info(f"- config.HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND: {config.HISTORICAL_DAYS_OF_ACTIVITY_TO_SEND}-")

    github_scheduler_update()
    twitter_scheduler_update()
    stackoverflow_scheduler_update()
    sending_to_dest()
    logger_init.info(f"* completed social aggregator *")

    while True:
        pass


def sending_to_dest():
    logger_init.info(f"- Sending updated social activity to destination: {config.API_URL}-")

    new_dict = get_social_activity_for_df()
    # print(new_dict)
    headers = {'password':config.API_ENDPOINT_TESTER_PASSWORD,'Content-Type': 'application/json'}
    payload = {'new_activity':new_dict}


    response = requests.request("POST", config.API_URL, headers=headers, data=str(json.dumps(payload)))

    logger_init.info(f"- Sent updated social data to destination. Status code: {response.status_code} -")

if __name__ == '__main__':  
    # social_aggregator()
    scheduler_funct()