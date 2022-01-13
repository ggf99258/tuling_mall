from libs.yuntongxun.yuntongxun.sms import CCP
from celery_tasks.main import app
@app.task
def ytx(mobile,code):
    print('开始')
    CCP().send_template_sms(mobile,[code, 5],1)
    print('ok')