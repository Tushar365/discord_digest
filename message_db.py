import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id TEXT PRIMARY KEY, 
                  content TEXT, 
                  author TEXT, 
                  timestamp DATETIME,
                  channel_id TEXT)''')
    conn.commit()
    conn.close()

def store_message(message):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    try:
        c.execute('INSERT OR IGNORE INTO messages VALUES (?,?,?,?,?)',
                  (str(message.id),  # Ensure id is string
                   message.content, 
                   str(message.author), 
                   message.created_at, 
                   str(message.channel.id)))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Message {message.id} already exists")
    except Exception as e:
        print(f"Error storing message: {e}")
    finally:
        conn.close()

def get_daily_messages(channel_ids=None):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
    
    if channel_ids:
        # Convert channel_ids to a comma-separated string for IN clause
        channels_str = ','.join(f"'{ch}'" for ch in channel_ids)
        query = f'''SELECT content, author, timestamp , channel_id
                    FROM messages 
                    WHERE timestamp >= ? AND channel_id IN ({channels_str})'''
        c.execute(query, (twenty_four_hours_ago,))
    else:
        c.execute('''SELECT content, author, timestamp 
                     FROM messages 
                     WHERE timestamp >= ?''', 
                  (twenty_four_hours_ago,))
    
    results = c.fetchall()
    conn.close()
    return results
    
    