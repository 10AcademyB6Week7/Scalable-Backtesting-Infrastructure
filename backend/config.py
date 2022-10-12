from dotenv import load_dotenv
import os
import redis

load_dotenv()


class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql://benkartuser:benkartpass@melachallengedatabase.crlafpfc5g5y.us-east-1.rds.amazonaws.com:5432/benkartdb"
    
    SESSION_TYPE = "redis"
    SESSION_PERMINENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://localhost:6379")