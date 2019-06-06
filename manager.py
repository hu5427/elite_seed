from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session

app = Flask(__name__)


# 创建配置类
class Config(object):
    SECRET_KEY = 'dictionary'
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
        host=REDIS_HOST,port=REDIS_PORT)
    # 4.设置session为永久保存
    SECRET_PERMANENT = False
    # 5.设置存储有效期为一天（单位是秒）
    PERMANENT_SESSION_LIFETIME = 8640



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


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()
