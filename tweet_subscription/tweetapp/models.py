from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    tweet_limit = models.PositiveIntegerField(null=True, blank=True)  # None for unlimited

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    tweet_count = models.PositiveIntegerField(default=0)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
