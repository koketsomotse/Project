# Setup Instructions for Real-Time Notification Management System

## Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- PostgreSQL 12 or higher
- Redis (for caching)

## Backend Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Backend Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**:
   - Create a PostgreSQL database and user.
   - Update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

## Frontend Setup

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```

3. **Run the Development Server**:
   ```bash
   npm run dev
   ```

## Running Tests

### Backend Tests
To run the backend tests, use:
```bash
pytest
```

### Frontend Tests
To run the frontend tests, use:
```bash
npm test
```

## Common Issues and Solutions

### WebSocket Connection Issues
1. Check if the Django server is running with Channels.
2. Verify WebSocket URL in the client matches server configuration.
3. Ensure the authentication token is valid.
4. Check the browser console for connection errors.

### Database Connection Issues
1. Verify PostgreSQL service is running.
2. Check connection details in the `.env` file.
3. Ensure SSL certificates are properly configured.
4. Test connection using the `psql` command.