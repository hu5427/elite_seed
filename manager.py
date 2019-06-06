from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# 一 创建配置类
class Config(object):
    DEBUG = True

    # 配置数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1/elite_seed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(Config)
# 二 集成SQLAlchemy到flask
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()
