import random
import re
from datetime import datetime

from flask import request, abort, current_app, jsonify, make_response, session
from werkzeug.security import generate_password_hash

from info import redis_store, constants, db
from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.modules.passport import passport_blu
from info.utils.captcha.captcha import captcha
from info.utils.captcha.response_code import RET


@passport_blu.route("/login")
def login():
    dict_data = request.json
    mobile = dict_data.get("mobile")
    password = dict_data.get("password")

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    if not re.match(r"1[35678]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号不正确")

    try:
        user = User.query.filter_by(mobile=User.mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA, errsg="数据库查询失败")

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户没有注册")

    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg="密码错误")

    user.last_login = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库保存失败")

    session["user_id"] = user.id

    return jsonify(errno=RET.OK, errmsg="登录成功")


@passport_blu.route("/register", methods=["POST"])
def register():
    dict_data = request.json

    mobile = dict_data.get("mobile")
    smscode = dict_data.get("smscode")
    password = dict_data.get("password")

    if not all([mobile, smscode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    if not re.match(r"1[35678]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号不正确")
    try:
        real_sms_code = redis_store.get("SMS_" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA, errsg="数据库查询失败")

    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码已过期")

    if real_sms_code != smscode:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码输入错误")

    # 密码待修复

    user = User()
    user.nick_name = mobile
    # user.password = password
    user.password_hash = generate_password_hash(password)
    user.mobile = mobile

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库保存失败")

    session['user_id'] = user.id
    return jsonify(errno=RET.OK, errmsg="注册成功")


# 请求url是什么
# 请求的方式
# 参数名字
# return前端参数，参数类型


@passport_blu.route("/sms_code", methods=["POST"])
def get_sms_code():
    # return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")
    dict_data = request.json
    # 1 接收参数 mobile 手机号 image_code 图片验证码 image_code_id 短信验证码
    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")
    print("前端收到的手机号：%s" % str(mobile))
    print("前端收到的图片码：%s" % image_code.upper())
    print("前端收到的短信码：%s" % str(image_code_id))
    # 2 校验参数
    #  全局校验
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 3 mobile 校验
    if not re.match(r"1[35678]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")
    # 4 取出真实验证码
    try:
        real_image_code = redis_store.get("ImageCodeId_" + image_code_id)
        print("数据库取出图片验证码：%s" % real_image_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA, errmsg="数据库查询错误")

    # 5校验图片验证码
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码已经过期")

    if image_code.upper() != real_image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 6 定义随机6位验证码
    sms_code_str = "%06d" % random.randint(0, 999999)
    current_app.logger.info("短信验证码是：%s" % sms_code_str)
    # result = CCP().send_template_sms(mobile, [sms_code_str, constants.SMS_CODE_REDIS_EXPIRES / 60], 1)
    # # ccp.send_template_sms('18339303172', ['天道酬勤', 5], 1)
    # # 7 调用云通讯发送验证码
    # if result != 0:
    #     return jsonify(errno=RET.THIRDERR, errmsg="短信发送失败")
    # 8 将验证码存入redis
    try:
        redis_store.setex("SMS_" + mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code_str)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, reemsg="手机验证码保存失败")
    # 9 返回发送成功响应
    return jsonify(errno=RET.OK, errmsg="验证码发送成功")
    # 7 校验6位数验证码


@passport_blu.route("/img_code")
def get_image_code():
    image_code_id = request.args.get("ImageCodeId")
    if not image_code_id:
        abort(404)
    _, text, image = captcha.generate_captcha()
    print("后台生成图片验证码：%s" % text)
    try:
        redis_store.setex("ImageCodeId_" + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    return image
