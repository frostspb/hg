from config.celery import app
from django.core.mail import send_mail
#from gradeis.settings import MAIL_FROM


@app.task(bind=True)
def send_status_email(self, subj, to, msg, addr_from):
    send_mail(subj, msg, addr_from, to, fail_silently=False #, html_message=msg
    )

