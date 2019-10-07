import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect  #导入csrf保护
from flask_migrate import Migrate

from flask_restful import Api

import pymysql
pymysql.install_as_MySQLdb()

app=Flask(__name__)#实例化app

app.config.from_pyfile("settings.py")
# app.config.from_envvar()#来源于环境变量，环境变量的值是python文件名称
# app.config.from_json()#来源于json文件，必须符合json格式
# app.config.from_mapping()#字典类型
app.config.from_object("settings.Config")#来源于类对象
app.secret_key="123123"


#第一种，直接写配置文件

#配置参数
# BASE_DIR=os.path.abspath(os.path.dirname(__file__))


# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")#数据库地址sqlite
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True#请求结束后自动提交
# app.config["SQLALCHEMY_RTACK_MODIFICATIONS"]=True#flask1版本之后，添加的选项，目的是跟踪修改


#orm关联应用
models=SQLAlchemy(app)
csrf = CSRFProtect(app) #使用csrf保护
api=Api(app)
migrate=Migrate(app,models)#安装数据库管理插件


