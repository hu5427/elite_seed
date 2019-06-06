from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis

from config import Config

app = Flask(__name__)

# 一 配置DEBUG
app.config.from_object(Config)

# 二 集成SQLAlchemy到flask
db = SQLAlchemy(app)

# 三 集成redis
redis_store = StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT
)

# 四 配置CSRF
CSRFProtect(app)

# 五 集成flask_session
Session(app)
