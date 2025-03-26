from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from core.constants import MAX_GROUP_USERS

from users.models import User

class UserGroupStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BLOCKED = 'blocked'
    DELETED = 'deleted'

class GroupStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class PaymentStatus(models.TextChoices):
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    UPCOMING = 'upcoming'

class ContributionStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    COMPLETED = 'completed'

class PayoutStatus(models.TextChoices):
    RECEIVED = 'received'
    UPCOMING = 'upcoming'

# enforces amount to be a positive value
def is_positive(value):
    if value < 0:
        raise ValidationError('Value must be positive')


class Group(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[is_positive])
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=GroupStatus.choices, default=GroupStatus.ACTIVE)

    class Meta:
        db_table = 'groups'


# this class maps a user to a group or list of groups
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users')
    position = models.IntegerField(null=False, blank=False, validators=[MaxValueValidator(MAX_GROUP_USERS), MinValueValidator(1)])
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=UserGroupStatus.choices, default=UserGroupStatus.ACTIVE)

    class Meta:
        db_table = 'user_groups'
        unique_together = ('group', 'position')

# holds the contribution for a particular month
class Contribution(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='contributions')
    payout_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payouts', null=True) # the user to receive the payout for the month
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[is_positive])
    position = models.IntegerField(default=1, validators=[MaxValueValidator(MAX_GROUP_USERS), MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=ContributionStatus.choices, default=ContributionStatus.ACTIVE)
    payout_status = models.CharField(max_length=20, choices=PayoutStatus.choices, default=PayoutStatus.UPCOMING)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = 'contributions'
        unique_together = ('group', 'position')

# holds the payment made by a user for a particular contribution
class ContributionPayment(models.Model):
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[is_positive])
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    date_paid = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contribution_payments'
        unique_together = ('contribution', 'user')