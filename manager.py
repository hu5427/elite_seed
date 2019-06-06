from flask import Flask

app = Flask(__name__)

# 创建配置类
class Config():
    DEBUG = True


app.config.from_object(Config)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()