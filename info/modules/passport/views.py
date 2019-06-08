import random
import re

from flask import request, abort, current_app, jsonify

from info import redis_store
from info.libs.yuntongxun.sms import CCP
from info.modules.passport import passport_blu
from info.utils.captcha.captcha import captcha
from info import constants

from info.utils.captcha.response_code import RET


# 请求url是什么
# 请求的方式
# 参数名字
# return前端参数，参数类型


@passport_blu.route("/")
def get_sms_code():
    dict_data = request.json
    # 1 接收参数 mobile 手机号 image_code 图片验证码 image_code_id 短信验证码
    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.fet("image_code_id")

    # 2 校验参数
    #  全局校验
    if not all([mobile, image_code, image_code_id]):
        return jsonify(error=RET.PARAMERR, errmsg="参数不全")

    # 3 mobile 校验
    if not re.match(r"1[35678]\d{9}$", mobile):
        return jsonify(error=RET.PARAMERR, errmsg="手机号格式不正确")
    # 4 取出真实验证码
    try:
        real_image_code = redis_store.get("ImageCodeId_" + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.NODATA, errmsg="数据库查询错误")

    # 5校验图片验证码
    if not real_image_code:
        return jsonify(error=RET.NODATA, errmsg="图片验证码已经过期")

    if image_code.upper() != real_image_code.upper():
        return jsonify(error=RET.DATAERR, errmsg="图片验证码错误")

    # 6 定义随机6位验证码
    sms_code_str = "%06d" % random.randint(0, 999999)
    current_app.logger.info("短信验证码是：%s" % sms_code_str)
    result = CCP().send_template_sms("mobile", [sms_code_str, constants.SMS_CODE_REDIS_EXPIRES / 60], 1)
    # 7 调用云通讯发送验证码
    if result != 0:
        return jsonify(error=RET.THIRDERR, errmsg="短信发送失败")
    # 8 将验证码存入redis
    try:
        redis_store.setex("SMS_" + mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code_str)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, reemsg="手机验证码保存失败")
    # 9 返回发送成功响应
    return jsonify(error=RET.OK, errmsg="验证码发送成功")
    # 7 校验6位数验证码


@passport_blu.route("/img_code")
def get_image_code():
    image_code_id = request.args.get("ImageCodeId")
    print(image_code_id)
    if not image_code_id:
        abort(404)
    _, text, image = captcha.generate_captcha()
    try:
        redis_store.setex("ImageCodeId" + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    return image
