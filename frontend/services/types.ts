export interface Notification {
    id: number;
    title: string;
    message: string;
    notification_type: 'TASK_UPDATED' | 'TASK_ASSIGNED' | 'TASK_COMPLETED';
    read: boolean;
    created_at: string;
    updated_at: string;
}

export interface UserPreferences {
    id: number;
    email_notifications: boolean;
    push_notifications: boolean;
    notification_types: string[];
} 