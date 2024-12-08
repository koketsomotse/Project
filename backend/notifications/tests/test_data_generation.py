import pytest
from django.contrib.auth.models import User
from notifications.models import NotificationType, Notifications, UserPreferences
from faker import Faker
from datetime import datetime, timedelta
import random
import json
from django.utils import timezone

fake = Faker()

@pytest.mark.django_db
class TestDataGeneration:
    def setup_method(self):
        """Initialize test data"""
        self.notification_types = self._create_notification_types()
        self.users = self._create_users(50)  # Create 50 test users
        self.notifications = self._create_notifications(500)  # Create 500 notifications
        self.test_start_time = timezone.now()
        
    def _create_notification_types(self):
        """Create predefined notification types"""
        types = [
            ("TASK_CREATED", "New task has been created"),
            ("TASK_UPDATED", "Task has been updated"),
            ("COMMENT_ADDED", "New comment added to task"),
            ("MENTION", "User mentioned in a task"),
            ("DEADLINE_APPROACHING", "Task deadline is approaching"),
            ("STATUS_CHANGED", "Task status has changed"),
            ("ASSIGNMENT_CHANGED", "Task assignment has changed"),
            ("PRIORITY_CHANGED", "Task priority has changed")
        ]
        return [NotificationType.objects.create(name=name, description=desc) 
                for name, desc in types]

    def _create_users(self, count):
        """Generate test users with preferences"""
        users = []
        for _ in range(count):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            # Create preferences for user with new fields
            prefs = UserPreferences.objects.create(
                user=user,
                email_notifications=fake.boolean(),
                push_notifications=fake.boolean()
            )
            # Add random enabled notification types
            enabled_types = random.sample(self.notification_types, 
                                       random.randint(1, len(self.notification_types)))
            prefs.enabled_types.set(enabled_types)
            users.append(user)
        return users

    def _create_notifications(self, count):
        """Generate test notifications"""
        notifications = []
        for _ in range(count):
            notification = Notifications.objects.create(
                recipient=random.choice(self.users),
                notification_type=random.choice(self.notification_types),
                title=fake.sentence(),
                message=fake.paragraph(),
                created_at=fake.date_time_between(
                    start_date='-30d',
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()
                ),
                read=fake.boolean(chance_of_getting_true=30),
                priority=random.choice(['LOW', 'MEDIUM', 'HIGH'])
            )
            notifications.append(notification)
        return notifications

    def test_data_distribution(self):
        """Test and report on data distribution"""
        report = {
            'total_users': len(self.users),
            'total_notifications': len(self.notifications),
            'notification_types': len(self.notification_types),
            'notifications_per_type': {},
            'notifications_per_priority': {
                'LOW': 0,
                'MEDIUM': 0,
                'HIGH': 0
            },
            'read_vs_unread': {
                'read': 0,
                'unread': 0
            },
            'notifications_per_user': {},
            'user_preferences': {
                'email_notifications': 0,
                'push_notifications': 0
            }
        }

        # Count notifications per type
        for ntype in self.notification_types:
            count = Notifications.objects.filter(notification_type=ntype).count()
            report['notifications_per_type'][ntype.name] = count

        # Count notifications by priority and read status
        for notification in self.notifications:
            report['notifications_per_priority'][notification.priority] += 1
            if notification.read:
                report['read_vs_unread']['read'] += 1
            else:
                report['read_vs_unread']['unread'] += 1

        # Count notifications per user
        for user in self.users:
            count = Notifications.objects.filter(recipient=user).count()
            report['notifications_per_user'][user.username] = count

        # Count user preferences
        for pref in UserPreferences.objects.all():
            if pref.email_notifications:
                report['user_preferences']['email_notifications'] += 1
            if pref.push_notifications:
                report['user_preferences']['push_notifications'] += 1

        # Generate test report
        self._generate_test_report(report)
        
        # Assertions to verify data integrity
        assert len(self.users) == 50, "Should have created 50 users"
        assert len(self.notifications) == 500, "Should have created 500 notifications"
        assert len(self.notification_types) == 8, "Should have 8 notification types"
        
        # Verify all notifications have valid recipients
        invalid_notifications = Notifications.objects.exclude(recipient__in=self.users)
        assert not invalid_notifications.exists(), "All notifications should have valid recipients"

    def _generate_test_report(self, report):
        """Generate a detailed test report"""
        report_time = timezone.now()
        
        with open('test_data_report.md', 'w') as f:
            f.write(f"# Notification System Test Data Report\n")
            f.write(f"Generated on: {report_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Overview\n")
            f.write(f"- Total Users: {report['total_users']}\n")
            f.write(f"- Total Notifications: {report['total_notifications']}\n")
            f.write(f"- Notification Types: {report['notification_types']}\n\n")
            
            f.write("## Notification Distribution\n")
            f.write("\n### By Type\n")
            for ntype, count in report['notifications_per_type'].items():
                percentage = (count / report['total_notifications']) * 100
                f.write(f"- {ntype}: {count} ({percentage:.1f}%)\n")
            
            f.write("\n### By Priority\n")
            for priority, count in report['notifications_per_priority'].items():
                percentage = (count / report['total_notifications']) * 100
                f.write(f"- {priority}: {count} ({percentage:.1f}%)\n")
            
            f.write("\n### Read vs Unread\n")
            for status, count in report['read_vs_unread'].items():
                percentage = (count / report['total_notifications']) * 100
                f.write(f"- {status.title()}: {count} ({percentage:.1f}%)\n")
            
            f.write("\n## User Statistics\n")
            total_prefs = len(self.users)
            f.write("\n### User Preferences\n")
            for pref, count in report['user_preferences'].items():
                percentage = (count / total_prefs) * 100
                f.write(f"- {pref.replace('_', ' ').title()}: {count} ({percentage:.1f}%)\n")
            
            f.write("\n### Notifications per User (Top 10)\n")
            sorted_users = sorted(
                report['notifications_per_user'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            for username, count in sorted_users:
                percentage = (count / report['total_notifications']) * 100
                f.write(f"- {username}: {count} ({percentage:.1f}%)\n")

            f.write("\n## Test Execution Details\n")
            duration = (report_time - self.test_start_time).total_seconds()
            f.write(f"- Test Duration: {duration:.2f} seconds\n")
            f.write(f"- Average Creation Time per Notification: {(duration/500):.3f} seconds\n")
            f.write(f"- Data Generation Period: 30 days\n")
