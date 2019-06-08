from flask import render_template

from info.modules.index import index_blu


# 将试图函数全部写入此文件中方便开发与管理

@index_blu.route('/')
def index():
    # redis_store.set('a','and')
    return render_template("news/index.html")
