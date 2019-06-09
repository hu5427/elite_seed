from flask import render_template, current_app, redirect, send_file, session

from info.models import User
from info.modules.index import index_blu


# 将试图函数全部写入此文件中方便开发与管理

@index_blu.route('/')
def index():
    # redis_store.set('a','and')

    user_id = session.get("user_id")

    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    data = {
        "user_info": user.to_dict() if user else None
    }


    return render_template("news/index.html", data=data)


@index_blu.route("/favicon.ico")
def favicon():
    # return send_file("news/favicon.ico")
    # return redirect("news/favicon.ico")
    return current_app.send_static_file("news/favicon.ico")