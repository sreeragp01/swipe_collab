from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from swipe.models import SwipeAction
from matches.models import Match
from chat.models import ChatRoom

User = get_user_model()


class Command(BaseCommand):
    help = 'Create mutual swipes and matches between test users'

    def handle(self, *args, **kwargs):

        pairs = [
            ('alex@test.com',  'techcorp@test.com'),
            ('priya@test.com', 'designstudio@test.com'),
            ('rahul@test.com', 'ailab@test.com'),
            ('sara@test.com',  'techcorp@test.com'),
        ]

        match_count = 0

        for freelancer_email, company_email in pairs:

            try:
                freelancer = User.objects.get(email=freelancer_email)
                company    = User.objects.get(email=company_email)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'  Skipping {freelancer_email} / {company_email} — user not found. Run seed_test_users first.'
                    )
                )
                continue

            if Match.objects.filter(
                Q(user1=freelancer, user2=company) |
                Q(user1=company,    user2=freelancer)
            ).exists():
                self.stdout.write(
                    f'  Skipping {freelancer_email} <-> {company_email} — match already exists'
                )
                continue

            SwipeAction.objects.get_or_create(
                swiper=freelancer,
                target=company,
                defaults={'action': SwipeAction.ACTION_LIKE}
            )

            SwipeAction.objects.get_or_create(
                swiper=company,
                target=freelancer,
                defaults={'action': SwipeAction.ACTION_LIKE}
            )

            match = Match.create(freelancer, company)
            ChatRoom.objects.get_or_create(match=match)

            self.stdout.write(
                self.style.SUCCESS(
                    f'  Created: {freelancer_email} <-> {company_email}'
                )
            )
            match_count += 1

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'Done! {match_count} matches created.')
        )
        self.stdout.write('Login and visit /matches/ to see them.')