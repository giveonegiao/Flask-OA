import os
from app import create,models
# from app.main.views import app
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate


app=create()
manage=Manager(app)
migrate=Migrate(app,models)
app.secret_key="123123"
# @manage.command
# def hello():#安装hello命令，当执行python manage.py hello的时候调用hello函数
#     print("hello")
#
# @manage.command#同步数据库
# def migrate():
#     models.create_all()

manage.add_command("db",MigrateCommand)




if __name__ == '__main__':
    manage.run()
    # os.system("python manage.py runserver")
    # command=sys.argv[1]
    # if command=="migrate":
    #     models.create_all()
    # elif command=="runserver":
    #     app.run(host="127.0.0.1",port=8000,debug=True)


