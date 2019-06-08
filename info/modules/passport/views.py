from flask import request, abort, current_app

from info import redis_store
from info.modules.passport import passport_blu
from info.utils.captcha.captcha import captcha
from info import constants


@passport_blu.route("/img_code")
def get_image_code():
    image_code_id = request.args.get("imageCodeId")
    print(image_code_id)
    if not image_code_id:
        abort(404)
    _, text, image = captcha.generate_captcha()
    try:
        redis_store.setex("imageCodeId" + image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    return image
