import errno
from flask import render_template, current_app, redirect, send_file, session, request, jsonify

from info import constants
from info.models import User, News, Category
from info.modules.index import index_blu


# 将试图函数全部写入此文件中方便开发与管理
from info.utils.captcha.response_code import RET


@index_blu.route("")
def get_news_list():
    """
    1 接收参数
    2 校验参数合法性
    3 查询出新闻 ——关系分类（时间排序
    3 返回响应以及数据
    :return:
    """

    cid = request.args.get("cid")
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    try:
        paginate = News.query.filter(News.category_id==cid)\
            .order_by(News.create_time.desc()).paginate(page,per_page,False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg="数据库查询错误")

    new_list = paginate.items
    current_page = paginate.page
    total_page = paginate.pages

    news_dict_li = list()
    for news in new_list:
        news_dict_li.append(news.to_dict())

    data = {
        "news_dict_li": news_dict_li,
        "current_page": current_page,
        "total_page": total_page
    }

    return jsonify(errno=RET.OK,errmsg="ok",data=data)


@index_blu.route('/')
def index():
    # redis_store.set('a','and')
    # 登录后右上角显示用户信息
    user_id = session.get("user_id")

    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    # 与数据库同步显示点击率排行
    clicks_news = []
    try:
        clicks_news = News.query.order_by(News.clicks.desc()).limit(constants.HOME_PAGE_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)
    # clicks_news_li = []
    # for news_obj in clicks_news:
    #     clicks_news_li.append(news_obj)
    clicks_news_li = [ news_obj for news_obj in clicks_news ]

    # 显示新闻分类
    category = []
    try:
        category = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
    category_li = [category_dict for category_dict in category ]


    data = {
        "user_info": user.to_dict() if user else None,
        "clicks_news_li": clicks_news_li,
        "category_li": category_li
    }

    return render_template("news/index.html", data=data)


@index_blu.route("/favicon.ico")
def favicon():
    # 三种方法
    # return send_file("news/favicon.ico")
    # return redirect("news/favicon.ico")
    return current_app.send_static_file("news/favicon.ico")
