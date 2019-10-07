import os
import hashlib
import datetime
import functools

from flask import session
from main import app
from models import *
from flask import render_template
from flask import request
from models import User
from flask import redirect
from main import csrf

class Pager:
    """
    flask分页通过sqlalachemy查询进行分页
    offset 偏移，开始查询的位置
    limit 单页条数
    分页器需要具备的功能
    页码
    分页数据
    是否第一页
    是否最后一页
    """

    def __init__(self, data, page_size):
        """
        :param data: 要分页的数据
        :param page_size: 每页多少条
        """
        self.data = data #总数据
        self.page_size = page_size #单页数据
        self.is_start = False
        self.is_end = False
        self.page_count = len(data)
        self.next_page=0  #下一页
        self.previous_page=0  #上一页

        self.page_nmuber = self.page_count/page_size
        #(data+page_size-1)//page_size
        if self.page_nmuber == int(self.page_nmuber):
            self.page_nmuber = int(self.page_nmuber)
        else:
            self.page_nmuber = int(self.page_nmuber)+1

        self.page_range = range(1,self.page_nmuber+1)#页码范围
    def page_data(self,page):
        """
        返回分页数据
        :param page: 页码

        """
        self.next_page=int(page)+1
        self.previous_page=int(page)-1
        if page <= self.page_range[-1]:
            page_start = (page - 1)*self.page_size
            page_end = page*self.page_size
            # data = self.data.offset(page_start).limit(self.page_size)
            data = self.data[page_start:page_end]
            if page == 1:
                self.is_start = True
            else:
                self.is_start = False
            if page == self.page_range[-1]:
                self.is_end = True
            else:
                self.is_end = False
        else:
            data = ["没有数据"]
        return data

class Calendar:
    """
    当前类实现日历功能
    1、返回列表嵌套列表的日历
    2、安装日历格式打印日历
    # 如果一号周周一那么第一行1-7号   0
    # 如果一号周周二那么第一行empty*1+1-6号  1
    # 如果一号周周三那么第一行empty*2+1-5号  2
    # 如果一号周周四那么第一行empty*3+1-4号  3
    # 如果一号周周五那么第一行empyt*4+1-3号  4
    # 如果一号周周六那么第一行empty*5+1-2号  5
    # 如果一号周日那么第一行empty*6+1号   6
    # 输入 1月
    # 得到1月1号是周几
    # [] 填充7个元素 索引0对应周一
    # 返回列表
    # day_range 1-30
    """

    def __init__(self, month="now"):
        self.result = []

        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        # 获取当前月
        now = datetime.datetime.now()
        if month == "now":
            month = now.month
            first_date = datetime.datetime(now.year, now.month, 1, 0, 0)
            # 年 月 日 时 分
        else:
            first_date = datetime.datetime(now.year, now.month, 1, 0, 0)
        if month in big_month:
            day_range = range(1, 32)  # 指定月份的总天数
        elif month in small_month:
            day_range = range(1, 31)
        else:
            day_range = range(1, 29)

        # 获取指定月天数
        self.day_range = list(day_range)
        first_week = first_date.weekday()  # 获取指定月1号是周几

        line1 = []  # 第一行数据
        for e in range(first_week):
            line1.append("暂无")
        for d in range(7 - first_week):
            line1.append(str(self.day_range.pop(0))+"-Django")
        self.result.append(line1)
        while self.day_range:  # 如果总天数列表有值，就接着循环
            line = []  # 每个子列表
            for i in range(7):
                if len(line) < 7 and self.day_range:
                    line.append(str(self.day_range.pop(0))+"-Django")
                else:
                    line.append("暂无")
            self.result.append(line)

    def return_month(self):
        """
        返回列表嵌套列表的日历
        """
        return self.result

    def print_month(self):
        """
        按照日历格式打印日历
        """
        print("星期一  星期二  星期三  星期四  星期五  星期六  星期日")
        for line in self.result:
            for day in line:
                day = day.center(6)
                print(day, end="  ")
            print()


def loginValid(fun):
    @functools.wraps(fun)#保留原函数的名称
    def inner(*args,**kwargs):
        username=request.cookies.get("username")
        id=request.cookies.get("id","0")
        user=User.query.get(int(id))
        session_username=session.get("username")
        if user:#检测是否有对应id的用户
            if user.user_name == username and username==session_username:  #用户名是否对应
                return fun(*args, **kwargs)
            else:
                return redirect("/login/")
        else:
            return redirect("/login/")
    return inner


def return_month(self):
    """
    返回列表嵌套列表的日历
    """
    return self.result
def print_month(self):
    """
    按照日历格式打印日历
    """
    print("星期一  星期二  星期三  星期四  星期五  星期六  星期日")
    for line in self.result:
        for day in line:
            day = day.center(6)
            print(day, end="  ")
        print()
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

@app.route("/login/",methods=["GET","POST"])  # 路由
# @csrf.exempt
def login():  # 视图
    error_meg=""
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        if email:
            user=User.query.filter_by(email=email).first()
            if user:
                db_password=user.password
                if db_password==password:
                    response=redirect("/index/")
                    response.set_cookie("username",user.user_name)
                    response.set_cookie("email",user.email)
                    response.set_cookie("id",str(user.id))
                    session["username"]=user.user_name
                    return response
                else:
                    error_meg="密码不正确"
            else:
                error_meg="用户不存在"
        else:
            error_meg="邮箱不能为空"
    return render_template("login.html",**locals())

@app.route("/logout/")
def logout():
    response=redirect("/login/")
    response.delete_cookie("username")
    response.delete_cookie("email")
    response.delete_cookie("id")
    session.pop("username")#两种皆可
    # del session["username"]
    return response

@app.route("/index/")#然后再进行路由
@loginValid    #先执行loginValid
def index():  # 视图
    c=Curriculum()
    c.c_id="0001"
    c.c_name="python基础"
    c.c_time=datetime.datetime.now()
    c.save()
    curr_list=Curriculum.query.all()
    return render_template("index.html",curr_list=curr_list)


@app.route("/userinfo/")
@loginValid
def userinfo():
    calendar = Calendar().return_month()
    now = datetime.datetime.now()
    return render_template("userinfo.html", **locals())

@app.route("/register/",methods=["GET","POST"])
def register():
    """
    form 表单提交的数据由request.form接受
    """
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        user=User()
        user.user_name=username
        user.email=email
        user.password=password
        user.save()
    return render_template("register.html")



@app.route("/holiday_leave/",methods=["GET","POST"])
@csrf.exempt
def holiday_leave():
    if request.method=="POST":
        request_name=request.form.get("request_user")
        request_type=request.form.get("request_type")
        request_phone=request.form.get("phone")
        start_time=request.form.get("start_time")
        end_time=request.form.get("end_time")
        request_description=request.form.get("request_description")

        leave=Leave()
        leave.request_id=request.cookies.get("id")
        leave.request_name=request_name
        leave.request_type=request_type  #假期类型
        leave.request_phone=request_phone  #联系方式
        leave.request_start_time=start_time  #起始时间
        leave.request_end_time=end_time  #结束时间
        leave.request_description=request_description  #描述
        leave.save()
        return redirect("/leave_list/")
    return render_template('holiday_leave.html')


@app.route("/leave_list/<int:page>/")
@loginValid
def leave_list(page):
    """
    分页
    :return:
    """
    leaves=Leave.query.all()
    pager=Pager(leaves,5)
    page_data=pager.page_data(page)
    return render_template("leave_list.html",**locals())


from flask import jsonify #flask封装后的json方法
# @app.route("/cancel/<int:id>/")
# def cancel(id):
#     leave=Leave.query.get(id)
#     leave.delete()
#     return jsonify({"data":"删除成功"})

@app.route("/cancel/",methods=["GET","POST"])
def cancel():
    # id = request.args.get("id")#通过args接受get请求数据
    id = request.form.get("id")
    leave = Leave.query.get(int(id))
    leave.delete()
    return jsonify({"data":"删除成功"})    #返回json数据


from forms import TaskForm
@app.route('/add_task/',methods=["GET","POST"])
def add_task():
    errors = ""
    task = TaskForm()
    if request.method == "POST":
        if task.validate_on_submit():   #判断是否是一个有效的post请求
            formData = task.data
        else:
            errors_list = list(task.errors.keys())
            # errors_list = list(task.errors.values())
            errors = task.errors
            # print(errors)
            # print(task.errors) # 表单校验错误
            # print(task.validate_on_submit())# 判断是否是一个有效的post请求
            # print(task.validate())   # 判断是否是一个合法的post请求
            # print(task.data) # 提交的数据
    return render_template("add_task.html",**locals())


from settings import STATICFILES_DIR
@app.route('/picture/',methods=["GET","POST"])
def picture():
    p = {"picture":"img/1.jpg"}
    if request.method == "POST":
        file = request.files.get("photo")
        file_name = file.filename
        file_path = "img/%s"%file_name
        save_path =os.path.join(STATICFILES_DIR,file_path)
        file.save(save_path)
        p = Picture()
        p.picture = file_path
        p.save()
    return render_template("picture.html",p = p)

@app.route("/empty/")
def empty():
    return render_template("empty.html")

from main import api
from flask_restful import Resource

@api.resource("/Api/leave/")
class LeaveApi(Resource):
    def __init__(self):
        """
        定义返回的格式
        """
        super(LeaveApi,self).__init__()
        self.result = {
            "version": "1.0",
            "data": ""
        }
    def set_data(self,leave):
        """
        定义返回的数据
        """
        result_data = {
            "request_name": leave.request_name,
            "request_type": leave.request_type,
            "request_start_time": leave.request_start_time,
            "request_end_time": leave.request_end_time,
            "request_description": leave.request_description,
            "request_phone": leave.request_phone,
        }
        return result_data
    def get(self):
        """
        处理get请求
        """
        data = request.args #获取请求的数据
        id = data.get("id") #获取id
        if id: #如果id存在，返回当前id数据
            leave = Leave.query.get(int(id))
            result_data = self.set_data(leave)
        else: #如果id不存在，返回所有数据
            leaves = Leave.query.all()
            result_data = []
            for leave in leaves:
                result_data.append(self.set_data(leave))
        self.result["data"] = result_data
        return self.result
    def post(self):
        """
        这是post请求，负责保存数据
        """
        data = request.form
        request_id = data.get("request_id")
        request_name = data.get("request_name")
        request_type = data.get("request_type")
        request_start_time = data.get("request_start_time")
        request_end_time = data.get("request_end_time")
        request_description = data.get("request_description")
        request_phone = data.get("request_phone")

        leave = Leave()
        leave.request_id = request_id
        leave.request_name = request_name
        leave.request_type = request_type  # 假期类型
        leave.request_start_time = request_start_time  # 起始时间
        leave.request_end_time = request_end_time  # 结束时间
        leave.request_description = request_description  # 请假事由
        leave.request_phone = request_phone  # 联系方式
        leave.request_status = "0"  # 假条状态
        leave.save()

        self.result["data"] = self.set_data(leave)
        return self.result
    def put(self):
        data = request.form #请求数据，类字典对象
        id = data.get("id") #data里面的id
        leave = Leave.query.get(int(id)) #在数据库里面找到
        # request_name = data.get("request_name",leave.request_name)
        # request_type = data.get("request_type",leave.request_type)
        # request_start_time = data.get("request_start_time",leave.request_start_time)
        # request_end_time = data.get("request_end_time",leave.request_end_time)
        # request_description = data.get("request_description",leave.request_description)
        # request_phone = data.get("request_phone",leave.request_phone)
        #
        # leave.request_name = request_name
        # leave.request_type = request_type  # 假期类型
        # leave.request_start_time = request_start_time  # 起始时间
        # leave.request_end_time = request_end_time  # 结束时间
        # leave.request_description = request_description  # 请假事由
        # leave.request_phone = request_phone  # 联系方式
        for key,value in data.items():
            if key != "id":
                setattr(leave,key,value)
        leave.save()
        self.result["data"] = self.set_data(leave)
        return self.result


    def delete(self):
        data = request.form  # 请求数据，类字典对象
        id = data.get("id")  # data里面的id

        leave = Leave.query.get(int(id))
        leave.delete()
        self.result["data"] = "id 为 %s的数据删除成功"%id
        return self.result

