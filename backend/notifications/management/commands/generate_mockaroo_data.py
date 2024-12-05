"""
Management command to generate test data using Mockaroo API.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
import requests
import json
from notifications.models import Notifications, UserPreferences, NotificationType

class Command(BaseCommand):
    help = 'Generate test data using Mockaroo API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of notifications to generate'
        )
        parser.add_argument(
            '--api-key',
            type=str,
            required=True,
            help='Mockaroo API key'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        api_key = kwargs['api_key']
        
        # Mockaroo API endpoint
        url = f'https://api.mockaroo.com/api/generate.json'
        
        # Schema for notification data
        schema = {
            'id': {'type': 'row_number'},
            'user_email': {'type': 'email'},
            'notification_type': {
                'type': 'custom_list',
                'values': [choice[0] for choice in NotificationType.choices]
            },
            'title': {'type': 'words', 'min': 3, 'max': 7},
            'message': {'type': 'sentences', 'min': 1, 'max': 3},
            'created_at': {'type': 'datetime', 'min': '1month', 'max': 'now'},
            'read': {'type': 'boolean'}
        }

        try:
            # Make request to Mockaroo API
            response = requests.post(
                url,
                headers={'X-API-Key': api_key},
                json={
                    'count': count,
                    'fields': schema
                }
            )
            response.raise_for_status()
            mock_data = response.json()

            self.stdout.write('Creating test users and notifications...')
            
            for item in mock_data:
                # Create or get user
                username = item['user_email'].split('@')[0]
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': item['user_email'],
                        'password': 'testpass123'
                    }
                )

                # Create user preferences if new user
                if created:
                    UserPreferences.objects.create(user=user)

                # Create notification
                Notifications.objects.create(
                    recipient=user,
                    notification_type=item['notification_type'],
                    title=item['title'],
                    message=item['message'],
                    read=item['read'],
                    created_at=item['created_at']
                )

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {count} notifications with Mockaroo data'
            ))

        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data from Mockaroo: {str(e)}')
            )
