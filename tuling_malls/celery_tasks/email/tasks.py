from django.core.mail import send_mail
from celery_tasks.main import app
@app.task
def send_mails(subject, message, sender, receiver, html_message):
    print('开始')
    send_mail(subject, message, sender, receiver, html_message=html_message)
    print('ok')