from crum import get_current_request
from django.db.models.signals import post_delete
from django.dispatch import receiver

from core.pos.models import Sale, Logs


@receiver(post_delete, sender=Sale)
def create_logs_post_delete(sender, instance, **kwargs):
    request = get_current_request()
    log = Logs()
    log.customer = instance.customer
    log.employee = instance.employee
    log.date_joined = instance.date_joined
    log.subtotal = instance.subtotal
    log.iva = instance.iva
    log.total = instance.total
    log.cash = instance.cash
    log.change = instance.change
    log.user_log = request.user
    log.action = 'delete'
    log.save()
