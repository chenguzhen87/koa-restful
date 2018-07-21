import sqlite3
from threading import Lock
import eventlet
from flask import session, request
from flask_socketio import Namespace, emit, SocketIO
from app.apis.utils.log_helper import mylog
import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
socket_news = SocketIO(app, async_mode="eventlet")
thread = None
FuserId=None
thread_lock = Lock()

def background_thread():
    while True:
        eventlet.sleep(1)
        try:
            conn = sqlite3.connect('db/atsweb.db')
            c = conn.cursor()
            cursor=c.execute("select Fid,FtaskId,FflowNodeId,Fstatus from bill_approveInfo where FapproveUserId="+FuserId)
            msg=["2","rere"]
            socket_news.emit('my_response', msg, broadcast=True, namespace='/socket_news')
            # for row in cursor:
            #     msg.append({"Fid":row[0],"FtaskId": row[1],"FflowNodeId": row[2],"Fstatus": row[3]})
            # if msg:
            #     socket_news.emit('my_response', msg, broadcast=True,namespace='/socket_news')
            # else:
            #     return False
        except Exception as ex:
            mylog.error(ex)
        finally:
            conn.close()


class MyNamespace(Namespace):

    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_connect(self):
        global thread
        global FuserId
        with thread_lock:
            if thread is None:
                thread = socket_news.start_background_task(
                    target=background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})
        FuserId=request.values.get("FuserId",type=str)
        mylog.info('Client connected by user '+FuserId)

    def on_disconnect(self):
        mylog.info('Client disconnected by user '+FuserId)




def startSocketNews():
    socket_news.on_namespace(MyNamespace('/socket_news'))
    socket_news.run(app, host='0.0.0.0',port=9001,debug=True)

if __name__ == '__main__':
    startSocketNews()
