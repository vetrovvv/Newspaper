import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import *
from datetime import datetime,timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMultiAlternatives
logger = logging.getLogger(__name__)


def my_job():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    for cat in Category.objects.all():
        subscribers = set(User.objects.filter(subscribing_categories=cat))
        posts = Post.objects.filter(created_at__gte=last_week,category__id=cat.id)
        for u in subscribers:
            html_content = render_to_string(
                'news/weekly_message.html',
                {
                'cat': cat,
                'posts': posts,
                'link': 'http://127.0.0.1:8000',
                'user': u,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f"Недельная сводка новостей",
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[u.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")