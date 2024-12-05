"""
Management command to generate test data for the notification system.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker
from notifications.models import Notifications, UserPreferences, NotificationType

class Command(BaseCommand):
    help = 'Generate test data for notifications app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of test users to create'
        )
        parser.add_argument(
            '--notifications-per-user',
            type=int,
            default=10,
            help='Number of notifications per user'
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        num_users = kwargs['users']
        notifications_per_user = kwargs['notifications-per-user']

        self.stdout.write('Creating test users...')
        users = []
        for i in range(num_users):
            username = f'testuser{i}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='testpass123'
            )
            users.append(user)
            # Create user preferences
            UserPreferences.objects.create(user=user)

        self.stdout.write('Creating test notifications...')
        notification_types = [choice[0] for choice in NotificationType.choices]
        
        for user in users:
            for _ in range(notifications_per_user):
                # Random date within last 30 days
                created_at = timezone.now() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                Notifications.objects.create(
                    recipient=user,
                    notification_type=random.choice(notification_types),
                    title=fake.sentence(nb_words=4),
                    message=fake.paragraph(),
                    read=random.choice([True, False]),
                    created_at=created_at
                )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {num_users} users and '
            f'{num_users * notifications_per_user} notifications!'
        ))
