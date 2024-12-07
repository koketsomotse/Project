import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import NotificationComponent from '../components/NotificationComponent';
import * as websocketService from '../services/websocketService';

jest.mock('../services/websocketService');

describe('NotificationComponent', () => {
    beforeEach(() => {
        // Mock fetch globally
        global.fetch = jest.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve([
                    { id: 1, title: 'Test Notification', message: 'This is a test', notification_type: 'TASK_UPDATED', created_at: new Date().toISOString(), is_read: false }
                ]),
            })
        );
        (websocketService.useWebSocketStore as jest.Mock).mockReturnValue({
            connect: jest.fn(),
            disconnect: jest.fn(),
            socket: { onmessage: jest.fn() },
        });
    });

    test('renders notifications', async () => {
        render(<NotificationComponent />);

        // Wait for the notification to be displayed
        const notificationTitle = await screen.findByText('Test Notification');
        expect(notificationTitle).toBeInTheDocument();
    });

    test('marks notification as read', async () => {
        render(<NotificationComponent />);

        // Wait for the notification to be displayed
        await screen.findByText('Test Notification');

        // Mock the mark as read fetch call
        global.fetch = jest.fn(() => Promise.resolve({ status: 200 }));

        // Click the mark as read button
        fireEvent.click(screen.getByText('Mark as read'));

        // Verify that the notification is marked as read
        expect(global.fetch).toHaveBeenCalledWith('/api/notifications/1/mark_read/', { method: 'POST' });
    });
});
