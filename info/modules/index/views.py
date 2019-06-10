from flask import render_template, current_app, redirect, send_file, session

from info import constants
from info.models import User, News
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

    clicks_news = []
    try:
        clicks_news = News.query.order_by(News.clicks.desc()).limit(constants.HOME_PAGE_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)
    clicks_news_li = []
    for news_obj in clicks_news:
        clicks_news_li.append(news_obj)

    data = {
        "user_info": user.to_dict() if user else None,
        "clicks_news_li": clicks_news_li
    }

    return render_template("news/index.html", data=data)


@index_blu.route("/favicon.ico")
def favicon():
    # 三种方法
    # return send_file("news/favicon.ico")
    # return redirect("news/favicon.ico")
    return current_app.send_static_file("news/favicon.ico")
