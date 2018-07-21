flask权限系统，前后台分离模式开发
后端：
1、采用restful接口方式开发；
2、使用jwt框架做token登录校验，此处没有做登录过去校验，实际开发中可以将过期校验逻辑存入redis中，如果访问了不大，也可以直接存入数据库中，具体逻辑请参见utils下面的auth_helper.py；
3、采用flask+sqlalchemy开发；
4、发布使用uwsgi，详细配置见跟目录下的uwsgi.ini配置；
5、数据库为了测试方便，使用的是sqlite，见db/ats.db
前端：
1、vue全家桶+element-ui；
2、通过axios方式与后台交互；
3、前端发布采用nginx；

运行项目：
1、安装python3.6.4；
2、在pycharm中选择venv下的python.exe（也可通过pip install -r requirements.txt安装相关依赖）；
3、根目录下的dist是前端vue编译后的项目，但这样运行每次请求都会进入404，所以生成环境请分开部署；



启动方式一
/home/flask_permission_system>uwsgi --http :443 --file run.py  --callable app  --master --processes 24 --threads 12 >  out.file  2>&1  &
启动方式二
/home/flask_permission_system>uwsgi --ini uwsgi.ini
重载（一般修改参数，或者修改py文件经常用到）
/home/flask_permission_system>uwsgi --reload uwsgi.pid
重启（一般系统环境变化会用到）
/home/flask_permission_system>uwsgi --stop uwsgi.pid
/home/flask_permission_system>netstat -anp | grep 80
/home/flask_permission_system>kill -9 进程号


如果部署多个项目，可以使用虚拟环境
pip install virtualenv
pip install virtualenvwrapper



