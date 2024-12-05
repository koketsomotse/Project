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
    
    # List all tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    
    tables = cur.fetchall()
    print("\nExisting tables:")
    for table in tables:
        print(table[0])
    
    # Close cursor and connection
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"An error occurred: {e}")
