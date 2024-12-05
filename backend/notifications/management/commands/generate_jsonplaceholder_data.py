"""
Management command to generate test data using JSONPlaceholder API alongside Faker.
This provides an alternative source of realistic task-based notifications.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
import requests
import random
from faker import Faker
from notifications.models import Notifications, UserPreferences, NotificationType
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate test data using JSONPlaceholder API and Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users to create notifications for'
        )

    def handle(self, *args, **kwargs):
        num_users = kwargs['users']
        fake = Faker()

        try:
            # Fetch todos to use as task notifications
            todos_response = requests.get('https://jsonplaceholder.typicode.com/todos')
            todos_response.raise_for_status()
            json_todos = todos_response.json()

            self.stdout.write('Creating test users and notifications...')

            users = []
            for i in range(num_users):
                # Create user with Faker data
                username = fake.user_name()
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='testpass123'
                )
                users.append(user)
                # Create user preferences
                UserPreferences.objects.create(user=user)

            # Create notifications from todos for each user
            for user in users:
                # Get 5 random todos
                selected_todos = random.sample(json_todos, min(5, len(json_todos)))
                
                for todo in selected_todos:
                    # Random date within last 30 days
                    created_at = timezone.now() - timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                    
                    # Determine notification type based on todo status
                    if todo['completed']:
                        notification_type = NotificationType.TASK_COMPLETED
                        title = f"Task Completed: {todo['title'][:50]}"
                        message = f"The task '{todo['title']}' has been marked as complete."
                    else:
                        notification_type = NotificationType.TASK_ASSIGNED
                        title = f"New Task: {todo['title'][:50]}"
                        message = f"You have been assigned the task: {todo['title']}"

                    Notifications.objects.create(
                        recipient=user,
                        notification_type=notification_type,
                        title=title,
                        message=message,
                        read=random.choice([True, False]),
                        created_at=created_at
                    )

                    # Also create some random notifications using Faker
                    for _ in range(3):
                        created_at = timezone.now() - timedelta(
                            days=random.randint(0, 30),
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59)
                        )
                        
                        Notifications.objects.create(
                            recipient=user,
                            notification_type=random.choice([choice[0] for choice in NotificationType.choices]),
                            title=fake.sentence(nb_words=4),
                            message=fake.paragraph(),
                            read=random.choice([True, False]),
                            created_at=created_at
                        )

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created notifications for {num_users} users using both '
                f'JSONPlaceholder data and Faker!'
            ))

        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data from JSONPlaceholder: {str(e)}')
            )
