# Sample Data Generation Documentation

## Overview
This document outlines the steps taken to generate sample data for the Real-Time Notification Management System. The process involves creating users, their notification preferences, and sample notifications to facilitate testing of the notification system.

## Steps Taken

1. **Environment Setup**  
   - Created a `.env` file containing the necessary environment variables for Django, including the `SECRET_KEY`, `DEBUG` mode, and `DATABASE_URL` for connecting to the PostgreSQL database.
   - Example content of the `.env` file:
     ```
     SECRET_KEY=django-insecure-5k3m!b3+)rdx7zsqv$r4$p0#w9^&1v4e#x3=p8k4d2h7j9x$q2
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
     DATABASE_URL=postgres://avnadmin:AVNS_MLGywjFVmrqDpXsFf-r@pg-2f9aeda3-koketsomotse92-18ca.e.aivencloud.com:25499/defaultdb?sslmode=require
     ```

2. **Database Migrations**  
   - Ran the command `python manage.py migrate` to apply all migrations to the database. This ensures that the database schema is up to date with the models defined in the application.

3. **Sample Data Generation**  
   - Executed the management command `python manage.py generate_sample_data --users 5 --notifications 50` to create:
     - **5 Users** with unique usernames and passwords.
     - **50 Notifications** for each user, with varying types and messages based on predefined templates.
     - **Timestamps**: Each notification now includes a timestamp indicating when it was created and last updated. The `created_at` timestamp is randomized within the last 30 days, and the `updated_at` timestamp is set to the same value as `created_at`.
   - The command also created user preferences for each user, indicating their notification settings.

## Expected Outcomes

- **Users Created**: 5 unique users with the following sample credentials:
  1. **Username**: qbenton, **Password**: password123
  2. **Username**: zmcdonald, **Password**: password123
  3. **Username**: stephenpowers, **Password**: password123
  4. **Username**: linda97, **Password**: password123
  5. **Username**: amy82, **Password**: password123

- **Notifications**: Each user has 50 notifications in the database, simulating real-world scenarios of task updates, assignments, and completions.

- **User Preferences**: Each user has a set of preferences that determine which notifications they will receive.

## Conclusion
This sample data generation process allows for effective testing of the notification management system, ensuring that all components function as expected with realistic data. Further testing can be conducted by logging in with the provided credentials and verifying the notification functionalities.
