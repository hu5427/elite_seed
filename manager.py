from flask import Flask, session
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session
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

# 六 集成flask_script
manager = Manager(app)

# 七 集成flask_migrate
Manager(app, db)
manager.add_command("db", MigrateCommand)


@app.route('/')
def index():
    session['name1'] = 'join'
    redis_store.set('hello', 'world')
    return 'hello world'


if __name__ == '__main__':
    manager.run()
