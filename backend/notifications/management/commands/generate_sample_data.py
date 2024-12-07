from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notifications.models import Notifications, UserPreferences
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    """
    Django management command to generate sample data for the notification system.
    
    Generates:
    - Users with different roles
    - User preferences
    - Sample notifications with various types and states
    """
    
    help = 'Generates sample data for the notification system'

    def __init__(self):
        super().__init__()
        self.fake = Faker()
        self.notification_types = ['TASK_UPDATED', 'TASK_ASSIGNED', 'TASK_COMPLETED']
        self.task_titles = [
            'Update documentation',
            'Review pull request',
            'Deploy to production',
            'Fix critical bug',
            'Implement new feature',
            'Optimize database queries',
            'Write unit tests',
            'Update dependencies',
            'Refactor legacy code',
            'Setup monitoring'
        ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users to create'
        )
        parser.add_argument(
            '--notifications',
            type=int,
            default=50,
            help='Number of notifications per user'
        )

    def _create_users(self, count):
        """Creates sample users with unique usernames"""
        self.stdout.write('Creating users...')
        users = []
        for _ in range(count):
            username = self.fake.user_name()
            while User.objects.filter(username=username).exists():
                username = self.fake.user_name()
            
            user = User.objects.create_user(
                username=username,
                email=self.fake.email(),
                password='password123'
            )
            users.append(user)
            self.stdout.write(f'Created user: {username}')
        return users

    def _create_preferences(self, user):
        """Creates randomized notification preferences for a user"""
        # Ensure at least one preference is True
        prefs = {
            'task_updated': random.choice([True, False]),
            'task_assigned': random.choice([True, False]),
            'task_completed': random.choice([True, False])
        }
        if not any(prefs.values()):
            # If all are False, randomly set one to True
            key = random.choice(list(prefs.keys()))
            prefs[key] = True

        UserPreferences.objects.create(
            user=user,
            **prefs
        )
        self.stdout.write(f'Created preferences for user: {user.username}')

    def _create_notifications(self, user, count):
        """Creates sample notifications for a user"""
        self.stdout.write(f'Creating notifications for user: {user.username}')
        
        # Create notifications with varying dates
        for _ in range(count):
            notification_type = random.choice(self.notification_types)
            task_title = random.choice(self.task_titles)
            
            # Generate a random date within the last 30 days
            created_at = timezone.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            updated_at = created_at  # Set updated_at to the same value as created_at
            
            # Generate notification message based on type
            if notification_type == 'TASK_ASSIGNED':
                message = f'You have been assigned to: {task_title}'
            elif notification_type == 'TASK_UPDATED':
                message = f'Task updated: {task_title} - {self.fake.sentence()}'
            else:  # TASK_COMPLETED
                message = f'Task completed: {task_title}'

            Notifications.objects.create(
                recipient=user,
                notification_type=notification_type,
                title=task_title,
                message=message,
                read=random.choice([True, False]),
                created_at=created_at,
                updated_at=updated_at
            )

    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write('Starting sample data generation...')
        
        # Create users
        users = self._create_users(options['users'])
        
        # Create preferences and notifications for each user
        for user in users:
            self._create_preferences(user)
            self._create_notifications(user, options['notifications'])
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {len(users)} users with '
            f'{options["notifications"]} notifications each'
        ))
        
        # Print sample login credentials
        self.stdout.write('\nSample Login Credentials:')
        for user in users[:3]:
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write('Password: password123')
            self.stdout.write('')
