import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'defaultdb',
    'user': 'avnadmin',
    'password': 'AVNS_MLGywjFVmrqDpXsFf-r',
    'host': 'pg-2f9aeda3-koketsomotse92-18ca.e.aivencloud.com',
    'port': '25499',
    'sslmode': 'require'
}

try:
    # Establish connection
    conn = psycopg2.connect(**db_params)
    print("Successfully connected to the database!")
    
    # Create a cursor
    cur = conn.cursor()
    
    # Drop all relevant tables
    tables_to_drop = [
        'notifications_notifications',
        'notifications_notificationtype',
        'notifications_userpreferences',
        'django_migrations',
        'auth_group_permissions',
        'auth_user_groups',
        'auth_user_user_permissions',
        'auth_group',
        'auth_permission',
        'django_admin_log',
        'django_content_type',
        'auth_user',
        'django_session',
        'authtoken_token'
    ]
    
    # Drop each table
    for table in tables_to_drop:
        try:
            cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
            print(f"Dropped table {table}")
        except Exception as e:
            print(f"Error dropping {table}: {e}")
    
    # Commit the changes
    conn.commit()
    print("Successfully dropped all tables!")
    
    # Close cursor and connection
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"An error occurred: {e}")
