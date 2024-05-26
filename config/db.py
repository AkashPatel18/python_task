import sqlite3

def init_db():
    conn = sqlite3.connect('docker_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docker_data (
            id INTEGER PRIMARY KEY,
            image_url TEXT,
            host_port TEXT,
            container_port TEXT
        )
    ''')
    conn.commit()
    conn.close()

