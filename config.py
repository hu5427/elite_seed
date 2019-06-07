# 创建配置类
import logging

from redis import StrictRedis


class Config(object):
    import os
    import base64
    data = base64.b64encode(os.urandom(48))
    SECRET_KEY = data
    DEBUG = True

    # 配置数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1/elite_seed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 集成redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'

    # flask_session 配置信息

    # 1.储存方式指定为redis
    SESSION_TYPE = "redis"
    # 2.设置session签名 加密
    SESSION_USE_SIGNER = True
    # 3.设置存储对象
    SESSION_REDIS = StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT)
    # 4.设置session为永久保存
    SECRET_PERMANENT = False
    # 5.设置存储有效期为一天（单位是秒）
    PERMANENT_SESSION_LIFETIME = 8640


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    # 开发环境下的日志级别
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 生产环境下的日志级别
    LOG_LEVEL = logging.ERROR


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    # 测试环境下的日志级别
    LOG_LEVEL = logging.DEBUG

config = {
    "development": DevelopmentConfig,
    "product": ProductionConfig,
    "testing": TestingConfig
    }