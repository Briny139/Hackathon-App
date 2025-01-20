import sqlite3
from datetime import datetime
import uuid

def init_requests_db():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    # Create requests table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id TEXT PRIMARY KEY,
                  need TEXT,
                  requester_id TEXT,
                  requester_name TEXT,
                  time TIMESTAMP,
                  status TEXT,
                  distance TEXT)''')
    
    # Create messages table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id TEXT PRIMARY KEY,
                  request_id TEXT,
                  sender_id TEXT,
                  sender_name TEXT,
                  message TEXT,
                  timestamp TIMESTAMP,
                  FOREIGN KEY(request_id) REFERENCES requests(id))''')
    
    conn.commit()
    conn.close()

def create_request(need, requester_id, requester_name, distance):
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    request_id = str(uuid.uuid4())
    current_time = datetime.now()
    
    c.execute('''INSERT INTO requests (id, need, requester_id, requester_name, time, status, distance)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (request_id, need, requester_id, requester_name, current_time, "active", distance))
    
    conn.commit()
    conn.close()
    return request_id

def get_all_requests():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    c.execute('''SELECT * FROM requests WHERE status = "active" ORDER BY time DESC''')
    requests = c.fetchall()
    
    formatted_requests = []
    for r in requests:
        time_diff = get_time_diff(r[4])
        formatted_requests.append({
            "id": r[0],
            "need": r[1],
            "requester_id": r[2],
            "requester": r[3],
            "time": time_diff,
            "status": r[5],
            "distance": r[6]
        })
    
    conn.close()
    return formatted_requests

def save_message(request_id, sender_id, sender_name, message):
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    message_id = str(uuid.uuid4())
    current_time = datetime.now()
    
    c.execute('''INSERT INTO messages (id, request_id, sender_id, sender_name, message, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (message_id, request_id, sender_id, sender_name, message, current_time))
    
    conn.commit()
    conn.close()

def get_messages(request_id):
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    c.execute('''SELECT sender_name, message, timestamp 
                 FROM messages 
                 WHERE request_id = ? 
                 ORDER BY timestamp''', (request_id,))
    messages = c.fetchall()
    
    formatted_messages = []
    for m in messages:
        formatted_messages.append({
            "sender": m[0],
            "message": m[1],
            "time": m[2]
        })
    
    conn.close()
    return formatted_messages

def get_time_diff(timestamp):
    if isinstance(timestamp, str):
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} days ago"
    hours = diff.seconds // 3600
    if hours > 0:
        return f"{hours} hours ago"
    minutes = (diff.seconds % 3600) // 60
    return f"{minutes} mins ago"

def mark_request_complete(request_id):
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    c.execute('''UPDATE requests SET status = "completed" WHERE id = ?''', (request_id,))
    
    conn.commit()
    conn.close() 