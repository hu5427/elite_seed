from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

app = Flask(__name__)


# 创建配置类
class Config(object):
    DEBUG = True

    # 配置数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1/elite_seed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 集成redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'


# 一 配置DEBUG
app.config.from_object(Config)

# 二 集成SQLAlchemy到flask
db = SQLAlchemy(app)

# 三 集成redis
redis_store = StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT
)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()
