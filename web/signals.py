from django.contrib.auth.models import User
from django.db.models import signals
from web.models import Customer

def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, plan_name="Trial", asset_limit=10, price=0, type="Free" )


signals.post_save.connect(create_customer, sender=User)
