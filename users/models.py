from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser
from .manager import CustomManager

class NotificationType(models.TextChoices):
    GROUP_INVITATION = 'GROUP_INVITATION', 'Group Invitation'
    FUND_CONTRIBUTION = 'FUND_CONTRIBUTION', 'Fund Contribution'
    FUND_WITHDRAWAL = 'FUND_WITHDRAWAL', 'Fund Withdrawal'
    CONTRIBUTION_DISBURSEMENT = 'CONTRIBUTION_DISBURSEMENT', 'Contribution Disbursement'
    LOAN_REPAYMENT = 'LOAN_REPAYMENT', 'Loan Repayment'
    DEFAULT = 'GENERAL', 'General'

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False, editable=False)
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomManager()

    class Meta:
        db_table = 'users'

    @property
    def group(self):
        from contribution.models import UserGroup
        return UserGroup.objects.filter(user=self).last()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NotificationType.choices, default=NotificationType.DEFAULT)
    amount = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'notifications'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    amount = models.FloatField(default=0)

    class Meta:
        db_table = 'wallets'