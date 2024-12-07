# Test Case Documentation

This document provides an overview of the test cases implemented for the Real-Time Notification Management System.

## Overview
The test cases are designed to ensure the functionality and reliability of the notification system. They cover various aspects such as API endpoints, WebSocket connections, and user preferences.

## Test Cases

### 1. Notifications Model Tests
- **Purpose**: Verify the creation and integrity of notification objects in the database.
- **Test Case**: `test_notification_creation`
  - **Description**: Ensures that a notification can be created with the correct attributes.
  - **Expected Outcome**: The notification should be created and stored in the database with the specified attributes.

### 2. Notifications API Tests
- **Purpose**: Test the REST API endpoints for managing notifications.
- **Test Cases**:
  - **`test_create_notification`**
    - **Description**: Tests the creation of a notification via the API.
    - **Expected Outcome**: The API should return a `201 Created` status and the notification should be added to the database.
  - **`test_list_notifications`**
    - **Description**: Tests retrieving a list of notifications.
    - **Expected Outcome**: The API should return a `200 OK` status with a list of notifications.
  - **`test_mark_notification_read`**
    - **Description**: Tests marking a notification as read.
    - **Expected Outcome**: The API should return a `200 OK` status and the notification's read status should be updated.

### 3. User Preferences Tests
- **Purpose**: Verify the management of user notification preferences.
- **Test Cases**:
  - **`test_create_preferences`**
    - **Description**: Tests creating user preferences.
    - **Expected Outcome**: The API should return a `201 Created` status and the preferences should be stored in the database.
  - **`test_update_preferences`**
    - **Description**: Tests updating user preferences.
    - **Expected Outcome**: The API should return a `200 OK` status and the preferences should be updated.
  - **`test_duplicate_preferences`**
    - **Description**: Ensures that a user cannot create multiple sets of preferences.
    - **Expected Outcome**: The API should prevent duplicate preferences from being created.

### 4. WebSocket Tests
- **Purpose**: Ensure the functionality of WebSocket connections for real-time notifications.
- **Test Case**: `test_websocket_connection`
  - **Description**: Tests establishing a WebSocket connection and receiving notifications.
  - **Expected Outcome**: The WebSocket connection should be successfully established and notifications should be received in real-time.

## How to Run Tests

To run the tests for the Real-Time Notification Management System, follow these steps:

1. **Set Up the Environment**:
   - Ensure that your development environment is set up with all necessary dependencies.
   - Activate your virtual environment if using one.

2. **Run Tests**:
   - Navigate to the backend directory in your terminal.
   - Execute the following command to run all tests:
     ```bash
     python -m pytest
     ```
   - Review the test results in the terminal output.

3. **Debugging Failures**:
   - If any tests fail, check the error messages and logs for details.
   - Use print statements or a debugger to inspect the state of your application during tests.

## How to Generate Sample Data

To generate sample data for testing purposes, use the Django management command provided:

1. **Navigate to the Backend Directory**:
   - Open your terminal and navigate to the backend directory of the project.

2. **Run the Management Command**:
   - Execute the following command to generate sample data:
     ```bash
     python manage.py generate_sample_data
     ```
   - This command will create sample users and notifications as defined in the `generate_sample_data.py` script.

3. **Verify Data Generation**:
   - Check the database to ensure that the sample data has been created successfully.
   - Use Django's admin interface or a database client to view the data.

## Conclusion
These test cases are critical for validating the core functionalities of the Real-Time Notification Management System. They help ensure that the system behaves as expected under various conditions and scenarios.
