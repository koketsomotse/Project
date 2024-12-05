import os
import django
import sys
import json
import requests
from faker import Faker
from datetime import datetime, timedelta
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_system.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notifications, UserPreferences, NotificationType

fake = Faker()

def fetch_json_placeholder_data():
    """Fetch sample data from JSONPlaceholder"""
    users = requests.get('https://jsonplaceholder.typicode.com/users').json()
    todos = requests.get('https://jsonplaceholder.typicode.com/todos').json()
    return users, todos

def create_sample_users(json_users):
    """Create sample users with data from JSONPlaceholder and Faker"""
    created_users = []
    for json_user in json_users[:5]:  # Create 5 users
        username = json_user['username']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=json_user['email'],
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            # Create user preferences
            UserPreferences.objects.create(
                user=user,
                task_updated=random.choice([True, False]),
                task_assigned=random.choice([True, False]),
                task_completed=random.choice([True, False])
            )
            created_users.append(user)
            print(f"Created user: {username}")
    return created_users

def create_sample_notifications(users, todos):
    """Create sample notifications using JSONPlaceholder todos and Faker"""
    notification_types = [choice[0] for choice in NotificationType.choices]
    
    for user in users:
        # Create notifications from todos
        for todo in random.sample(todos, 10):  # 10 notifications per user
            notification_type = random.choice(notification_types)
            created_at = datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23)
            )
            
            # Generate notification content based on todo and type
            if notification_type == 'TASK_UPDATED':
                title = f"Task Updated: {todo['title'][:50]}"
                message = f"The task has been modified. Current status: {'Completed' if todo['completed'] else 'Pending'}"
            elif notification_type == 'TASK_ASSIGNED':
                title = f"New Task Assignment: {todo['title'][:50]}"
                message = f"You have been assigned a new task: {todo['title']}"
            else:  # TASK_COMPLETED
                title = f"Task Completed: {todo['title'][:50]}"
                message = "The task has been marked as complete."

            notification = Notifications.objects.create(
                recipient=user,
                notification_type=notification_type,
                title=title,
                message=message,
                read=random.choice([True, False]),
                created_at=created_at
            )
            print(f"Created notification: {title[:30]}...")

def main():
    """Main function to generate sample data"""
    print("Fetching data from JSONPlaceholder...")
    json_users, todos = fetch_json_placeholder_data()
    
    print("\nCreating sample users...")
    users = create_sample_users(json_users)
    
    print("\nCreating sample notifications...")
    create_sample_notifications(users, todos)
    
    print("\nSample data generation complete!")
    print("\nSample user credentials:")
    for user in users:
        print(f"Username: {user.username} | Password: password123")

if __name__ == '__main__':
    main()
