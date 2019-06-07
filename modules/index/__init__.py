from flask import Blueprint

# 创建蓝图实例对象
index_blu = Blueprint("index", __name__)

# 导入views所有视图函数
from .views import *
