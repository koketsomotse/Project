# Real-Time Notification Management System

## Overview
The Real-Time Notification Management System is designed to provide users with real-time notifications for task updates, assignments, and completions. The system utilizes WebSockets for real-time communication and offers a user-friendly interface for managing notifications and preferences.

## Key Features
- **Real-Time Notifications**: Notifications are delivered instantly to connected users when tasks are updated, assigned, or completed.
- **User Preferences**: Users can set their notification preferences to opt-in or opt-out of certain notification types.
- **WebSocket Integration**: Utilizes Django Channels for real-time communication.
- **API Development**: RESTful API endpoints for managing notifications and user preferences.
- **Testing Utilities**: Comprehensive testing suite using Jest for the frontend and pytest for the backend.

## Technical Architecture
- **Backend Framework**: Django 4.2.7
- **Database**: PostgreSQL (Aiven Cloud)
- **Real-time Communication**: Django Channels
- **API Framework**: Django REST Framework
- **Authentication**: Token-based system
- **WebSocket**: Channels WebSocket Consumer
- **Testing**: Django TestCase & Custom Tools
- **Sample Data**: Faker & JSONPlaceholder

## Setup Instructions
Refer to the [SETUP.md](./SETUP.md) file for detailed setup instructions for both the backend and frontend.

## Testing
### Running Tests
- **Backend Tests**: Use `pytest` to run backend tests.
- **Frontend Tests**: Use `npm test` to run frontend tests.

### Expected Outcomes
- All tests should pass, indicating that the system functions as expected.

## Documentation
- **API Documentation**: Comprehensive API documentation is available in the `docs` directory.
- **Test Case Documentation**: Overview of implemented test cases is available in the `docs/test_case_documentation.md`.

## License
This project is licensed under the MIT License.