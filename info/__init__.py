import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis

from config import config

# 将其变为全局变量，在函数中调用init集成SQLAlchemy到flask


db = SQLAlchemy()


# 使用工厂方法配置不同生产环境不同日志级别
def set_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("/home/python/Desktop/elite_seed/logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


redis_store = None # type: StrictRedis
# 使用工厂方法
def create_app(config_name):
    set_log(config_name)
    app = Flask(__name__)

    # 一 配置DEBUG
    app.config.from_object(config[config_name])

    # 二 集成SQLAlchemy到flask
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 三 集成redis

    global redis_store
    redis_store = StrictRedis(
        host=config[config_name].REDIS_HOST,
        port=config[config_name].REDIS_PORT
    )

    # 四 配置CSRF
    CSRFProtect(app)

    # 五 集成flask_session
    Session(app)

    # 注册蓝图
    from modules.index import index_blu
    app.register_blueprint(index_blu)
    return app
