import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import NotificationSystem from '../components/NotificationSystem';
import { NotificationProvider } from '../contexts/NotificationContext';
import { AuthProvider } from '../contexts/AuthContext';
import { act } from 'react-dom/test-utils';

// Mock WebSocket
class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.onmessage = null;
    this.onclose = null;
    this.onopen = null;
    setTimeout(() => this.onopen && this.onopen({ data: 'Connected' }), 0);
  }

  send(data) {
    // Simulate receiving notifications after fetch request
    if (JSON.parse(data).type === 'fetch_notifications') {
      setTimeout(() => {
        this.onmessage({
          data: JSON.stringify({
            type: 'notifications',
            notifications: mockNotifications
          })
        });
      }, 100);
    }
  }

  close() {
    this.onclose && this.onclose();
  }
}

global.WebSocket = MockWebSocket;

// Mock notification data
const mockNotifications = [
  {
    id: 1,
    title: 'Test Notification 1',
    message: 'This is a test notification',
    created_at: new Date().toISOString(),
    notification_type: {
      name: 'TASK_CREATED',
      description: 'Task Created Notification'
    }
  },
  {
    id: 2,
    title: 'Test Notification 2',
    message: 'Another test notification',
    created_at: new Date().toISOString(),
    notification_type: {
      name: 'MENTION',
      description: 'Mention Notification'
    }
  }
];

// Mock API responses
const server = setupServer(
  rest.get('/api/notifications/', (req, res, ctx) => {
    return res(ctx.json({
      results: mockNotifications,
      count: mockNotifications.length
    }));
  }),

  rest.get('/api/notifications/preferences/', (req, res, ctx) => {
    return res(ctx.json({
      email_notifications: true,
      push_notifications: false,
      notification_types: ['TASK_CREATED', 'MENTION']
    }));
  }),

  rest.post('/api/notifications/preferences/', (req, res, ctx) => {
    return res(ctx.json(req.body));
  }),

  rest.post('/api/notifications/:id/mark-read/', (req, res, ctx) => {
    return res(ctx.json({ success: true }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('NotificationSystem Integration Tests', () => {
  const renderNotificationSystem = () => {
    return render(
      <AuthProvider>
        <NotificationProvider>
          <NotificationSystem />
        </NotificationProvider>
      </AuthProvider>
    );
  };

  test('loads and displays notifications', async () => {
    renderNotificationSystem();

    // Wait for notifications to load
    await waitFor(() => {
      expect(screen.getByText('Test Notification 1')).toBeInTheDocument();
      expect(screen.getByText('Test Notification 2')).toBeInTheDocument();
    });
  });

  test('handles real-time notifications', async () => {
    renderNotificationSystem();

    // Simulate receiving a real-time notification
    act(() => {
      const ws = new MockWebSocket('ws://localhost/ws/notifications/');
      ws.onmessage({
        data: JSON.stringify({
          type: 'notification',
          notification: {
            id: 3,
            title: 'Real-time Notification',
            message: 'This is a real-time notification',
            created_at: new Date().toISOString(),
            notification_type: {
              name: 'TASK_UPDATED',
              description: 'Task Updated Notification'
            }
          }
        })
      });
    });

    await waitFor(() => {
      expect(screen.getByText('Real-time Notification')).toBeInTheDocument();
    });
  });

  test('filters notifications by type', async () => {
    renderNotificationSystem();

    // Wait for notifications to load
    await waitFor(() => {
      expect(screen.getByText('Test Notification 1')).toBeInTheDocument();
    });

    // Click filter dropdown
    fireEvent.click(screen.getByText('Filter'));

    // Select TASK_CREATED filter
    fireEvent.click(screen.getByText('Task Created'));

    // Verify only task created notifications are shown
    expect(screen.getByText('Test Notification 1')).toBeInTheDocument();
    expect(screen.queryByText('Test Notification 2')).not.toBeInTheDocument();
  });

  test('marks notifications as read', async () => {
    renderNotificationSystem();

    // Wait for notifications to load
    await waitFor(() => {
      expect(screen.getByText('Test Notification 1')).toBeInTheDocument();
    });

    // Click mark as read button
    const markReadButtons = screen.getAllByRole('button', { name: /mark as read/i });
    fireEvent.click(markReadButtons[0]);

    // Verify notification is marked as read
    await waitFor(() => {
      expect(screen.getByText('Test Notification 1')).toHaveClass('read');
    });
  });

  test('updates notification preferences', async () => {
    renderNotificationSystem();

    // Open preferences modal
    fireEvent.click(screen.getByText('Preferences'));

    // Toggle email notifications
    fireEvent.click(screen.getByLabelText('Email Notifications'));

    // Save preferences
    fireEvent.click(screen.getByText('Save Preferences'));

    // Verify preferences are updated
    await waitFor(() => {
      expect(screen.getByLabelText('Email Notifications')).toBeChecked();
    });
  });

  test('handles pagination', async () => {
    // Mock paginated response
    server.use(
      rest.get('/api/notifications/', (req, res, ctx) => {
        const page = parseInt(req.url.searchParams.get('page')) || 1;
        const pageSize = 10;
        const start = (page - 1) * pageSize;
        const end = start + pageSize;
        
        return res(ctx.json({
          results: mockNotifications.slice(start, end),
          count: mockNotifications.length,
          next: end < mockNotifications.length ? `/api/notifications/?page=${page + 1}` : null,
          previous: page > 1 ? `/api/notifications/?page=${page - 1}` : null
        }));
      })
    );

    renderNotificationSystem();

    // Wait for initial notifications to load
    await waitFor(() => {
      expect(screen.getByText('Test Notification 1')).toBeInTheDocument();
    });

    // Click next page button
    fireEvent.click(screen.getByText('Next'));

    // Verify page change
    await waitFor(() => {
      expect(screen.getByText('Page 2')).toBeInTheDocument();
    });
  });
});
