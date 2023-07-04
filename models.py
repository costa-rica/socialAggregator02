from sqlalchemy import create_engine, inspect, text
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from config import ConfigLocal, ConfigDev, ConfigProd
import os
from datetime import datetime

# from dotenv import load_dotenv

# load_dotenv()

if os.environ.get('CONFIG_TYPE')=='local':
    config = ConfigLocal()
    
    print('* modelsBase: Development - Local')
    print('SQL_URI: ',config.SQL_URI)
elif os.environ.get('CONFIG_TYPE')=='dev':
    config = ConfigDev()
    print('* modelsBase: Development')
elif os.environ.get('CONFIG_TYPE')=='prod':
    config = ConfigProd()
    print('* modelsBase: Configured for Production')

if not os.path.exists(config.PROJ_DB_PATH):
    os.mkdir(config.PROJ_DB_PATH)

Base = declarative_base()
engine = create_engine(config.SQL_URI, echo = False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)
sess = Session()


class SocialPosts(Base):
    __tablename__ = 'social_posts'
    id = Column(Integer, primary_key = True)
    username = Column(Text)
    user_reputation = Column(Text)
    title = Column(Text)
    description = Column(Text)
    network_post_id = Column(Text)
    view_count = Column(Integer)
    like_count = Column(Integer)
    answered = Column(Text)
    response_count = Column(Integer)
    url = Column(Text)

    social_name = Column(Text)
    social_icon = Column(Text)
    post_date = Column(Text)
    notes = Column(Text)
    time_stamp_utc = Column(DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f'SocialPosts(id: {self.id}, username: {self.username}, title: {self.title},' \
            f'post_date: {self.post_date})'


if 'social_posts' in inspect(engine).get_table_names():
    print("db already exists")
else:

    Base.metadata.create_all(engine)
    print("NEW db created.")