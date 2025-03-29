from contribution.models import Contribution, Group, GroupStatus, UserGroup
from core.constants import MAX_GROUP_USERS
from utils.date_utils import DateUtil
from contribution.models import Group, GroupStatus, ContributionStatus, UserGroup

from users.models import Notification, NotificationType
from .notification_service import NotificationService
from users.models import User

import random

class ContributionService:

    @staticmethod
    def add_member(user, amount):
        group = ContributionService._create_group(amount=amount)
        user.groups.add(group[0])
        user_group, created = UserGroup.objects.get_or_create(
            user=user,
            group=group[0],
            defaults={'position': group[1]+1, 'user': user, 'group': group[0]}
        )

        # set rotation for users
        for contribution, _user in zip(user_group.group.contributions.all(), user_group.group.users.all()):
            if contribution.position == user_group.position:
                contribution.payout_to = _user.user

                if contribution.position != 1: # other contributions should be inactive
                    contribution.status = ContributionStatus.INACTIVE

                    contribution.save()
        
        try:
            NotificationService.send_email('Group Notification', f'Hello {user.name},\n\n' \
                f'You have been added to a thrift contribution group.\nGroup name: {group[0].name}\nYour turn: {user.group.position}', user_group.user.email)
        except:
            pass
        Notification.objects.create(
                    user=contribution.payout_to,
                    notification_type=NotificationType.GROUP_INVITATION,
                    message=f'You have been added to group {group[0].name}',
                    amount=None
                )
        
    @staticmethod
    def _create_group(amount):
        group = None
        for g in Group.objects.filter(status=GroupStatus.ACTIVE, contribution_amount=amount):
            print(g.users.count())
            if g.users.count() < 12:
                group = g
                break
        print(group)
         
        if group == None:
            rand_int = random.randint(100,999)
            group = Group.objects.create(
                    created_by = ContributionService._get_admin(),
                    name = f"Group {rand_int}",
                    contribution_amount = amount,
                    description = f"This is group - {rand_int}"
                )
        print("111")
        # create contributions
        for i in range(1, MAX_GROUP_USERS+1):
            start_date = DateUtil.get_date(i-1)[0]
            end_date = DateUtil.get_date(i-1)[1]

            Contribution.objects.get_or_create(
                    group=group, position=i, defaults={'payout_to': None, 'amount': group.contribution_amount, 'start_date': start_date, 'end_date': end_date}
            )
        print("222")

        # set rotation for users
        for contribution, user in zip(group.contributions.all(), group.users.all()):
            contribution.payout_to = user.user
            contribution.save()
        print("333")
        return group, group.users.count()
        
    @staticmethod
    def _get_admin():
        admin = None
        for user in User.objects.filter(is_admin=True):
            admin = user
            if admin:
                break
        
        if admin == None:
            admin, created = User.objects.get_or_create(
                email = 'emehinolasam01@gmail.com',
                name = 'Admin',
                phone = None,
                address = None,
                is_admin = True
            )
        return admin