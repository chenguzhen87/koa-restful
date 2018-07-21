from app.apis.views.errors import error
from app.apis.views.system_mgr.view_dpt import system_mgr_dpt
from app.apis.views.system_mgr.view_menu import system_mgr_menu
from app.apis.views.system_mgr.view_oper import system_mgr_oper
from app.apis.views.system_mgr.view_role import system_mgr_role
from app.apis.views.system_mgr.view_user import system_mgr_user
from app.apis.views.system_monitor.view_log import system_monitor_log
from app.apis.views.views import main


###这里注册蓝图

def register_app(app):
    ###注册蓝图main和error
    app.register_blueprint(error)
    app.register_blueprint(main)
    ###system_mgr
    app.register_blueprint(system_mgr_user)
    app.register_blueprint(system_mgr_dpt)
    app.register_blueprint(system_mgr_role)
    app.register_blueprint(system_mgr_menu)
    app.register_blueprint(system_mgr_oper)
    ###system_monitor
    app.register_blueprint(system_monitor_log)