from config.celery import app
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage


@app.task(bind=True)
def send_status_email(self, subj, to, msg, addr_from):
    send_mail(subj, msg, addr_from, to, fail_silently=False)


@app.task(bind=True)
def send_email_deal_desk(self, deal_desk_id):
    from hourglass.campaigns.models import DealDesk, DealDeskFiles
    from hourglass.settings.models import HourglassSettings
    deal = DealDesk.objects.filter(id=deal_desk_id).first()

    if not deal:
        return

    user_email = deal.user.email

    hgs = HourglassSettings.objects.all().first()
    desk_email = hgs.deal_desk_request_email
    if deal.user_job_titles:
        jt = deal.user_job_titles
    else:
        jt = ','.join([item.name for item in deal.job_titles.all()])

    if deal.user_lead_type:
        lt = deal.user_lead_type
    else:
        lt = ','.join([item.name for item in deal.lead_type.all()])

    if deal.user_industries:
        ind = deal.user_industries
    else:
        ind = ','.join([item.name for item in deal.industries.all()])

    if deal.user_geolocation:
        geo = deal.user_geolocation
    else:
        geo = ','.join([item.name for item in deal.geolocation.all()])

    if deal.user_company_revenue:
        rev = deal.user_company_revenue
    else:
        rev = ','.join([item.name for item in deal.company_revenue.all()])

    if deal.user_company_size:
        size = deal.user_company_size
    else:
        size = ','.join([item.name for item in deal.company_size.all()])

    if deal.user_seniority:
        sen = deal.user_seniority
    else:
        sen = ','.join([item.name for item in deal.seniority.all()])

    msg = f'''User Name: {deal.user.first_name} {deal.user.last_name}
                Team: {deal.user.team}
                Email: {deal.user.email}
                Client: {deal.client}
                Campaign Name:{deal.campaign_name}
                Budget / CPL:{deal.budget}
                Required Lead Volume:{deal.required_lead_volume}
                Lead Type:{lt}
                Campaign Duration:{deal.campaign_duration}
                Job Titles:{jt}
                Seniority (Job level):{sen}
                Job Area / Job Functions:{deal.job_area}
                Industries:{ind}
                Geolocation:{geo}
                Company Revenue:{rev}
                Company Size (Number of Employees):{size}
                ABM (Account Based Marketing):{deal.abm}
                Lead Cap:{deal.lead_cap}
                Suppression List(s):{deal.suppresion_list}
                Install Base:{deal.install_base}
                Custom Questions:{deal.custom_questions}
                It this a renewal?{deal.is_renewal}
                Notes:{deal.notes}
    '''

    m = EmailMessage('New DealDesk Request', msg, settings.MAIL_FROM, [user_email, desk_email])
    dfiles = DealDeskFiles.objects.filter(deal_desk=deal)
    for f in dfiles:
        m.attach_file(f.file.path)
    m.send()



