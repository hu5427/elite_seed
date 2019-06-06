from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis

from config import config

# 将其变为全局变量，在函数中调用init集成SQLAlchemy到flask
db = SQLAlchemy()


# 使用工厂方法
def create_app(config_name):
    app = Flask(__name__)

    # 一 配置DEBUG
    app.config.from_object(config[config_name])

    # 二 集成SQLAlchemy到flask
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 三 集成redis
    redis_store = StrictRedis(
        host=config[config_name].REDIS_HOST,
        port=config[config_name].REDIS_PORT
    )

    # 四 配置CSRF
    CSRFProtect(app)

    # 五 集成flask_session
    Session(app)
    return app
