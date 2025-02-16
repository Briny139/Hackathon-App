import sqlite3
from datetime import datetime
import uuid

class DatabaseManager:
    @staticmethod
    def init_db():
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        
        try:
            # Create requests table
            c.execute('''CREATE TABLE IF NOT EXISTS requests
                         (id TEXT PRIMARY KEY,
                          need TEXT,
                          requester_id TEXT,
                          requester_name TEXT,
                          time TIMESTAMP,
                          status TEXT DEFAULT 'active',
                          distance TEXT)''')
            conn.commit()
            
            # Create messages table
            c.execute('''CREATE TABLE IF NOT EXISTS messages
                         (id TEXT PRIMARY KEY,
                          request_id TEXT NOT NULL,
                          sender_id TEXT NOT NULL,
                          sender_name TEXT NOT NULL,
                          message TEXT NOT NULL,
                          timestamp TIMESTAMP)''')
            conn.commit()
            
            # Create users table
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id TEXT UNIQUE NOT NULL,
                          name TEXT NOT NULL,
                          resources TEXT,
                          services TEXT,
                          latitude REAL,
                          longitude REAL,
                          address TEXT,
                          registration_date TIMESTAMP)''')
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()

    @classmethod
    def clear_all_tables(cls):
        #Clear all data from all tables
        try:
            with cls.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM messages")
                cursor.execute("DELETE FROM requests")
                cursor.execute("DELETE FROM users")
                print("All tables cleared successfully")
                conn.commit()
                return True
        except Exception as e:
            print(f"Error clearing all tables: {e}")
            return False
        
    @staticmethod
    def save_registration(name, resources, services, latitude, longitude, address):
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        
        try:
            current_time = datetime.now()
            user_id = str(uuid.uuid4())  # Generate unique user ID
            
            c.execute('''INSERT INTO users 
                         (user_id, name, resources, services, latitude, longitude, address, registration_date)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (user_id, name, resources, services, latitude, longitude, address, current_time))
            conn.commit()
            print(f"Registration successful with user_id: {user_id}")
            return user_id
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        
        finally:
            conn.close()

    @staticmethod
    def create_request(need, requester_id, requester_name, distance):
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        
        try:
            request_id = str(uuid.uuid4())
            current_time = datetime.now()
            
            c.execute('''INSERT INTO requests 
                         (id, need, requester_id, requester_name, time, status, distance)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (request_id, need, requester_id, requester_name, current_time, "active", distance))
            
            conn.commit()
            return request_id
        except sqlite3.Error as e:
            print(f"Database error in create_request: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all_requests():
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        
        c.execute('''SELECT * FROM requests WHERE status = "active" ORDER BY time DESC''')
        requests = c.fetchall()
        
        formatted_requests = []
        for r in requests:
            time_diff = DatabaseManager.get_time_diff(r[4])
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def mark_request_complete(request_id):
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        
        c.execute('''UPDATE requests SET status = "completed" WHERE id = ?''', (request_id,))
        
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_details(user_id):
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        try:
            c.execute('''SELECT name, resources, services, latitude, longitude, address 
                         FROM users WHERE user_id = ?''', (user_id,))
            result = c.fetchone()
            if result:
                return {
                    'name': result[0],
                    'resources': result[1],
                    'services': result[2],
                    'latitude': result[3],
                    'longitude': result[4],
                    'address': result[5]
                }
            return {}
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {}
        finally:
            conn.close()

    @staticmethod
    def update_profile(user_id, name, resources, services):
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        try:
            c.execute('''UPDATE users 
                         SET name = ?, resources = ?, services = ?
                         WHERE user_id = ?''',
                      (name, resources, services, user_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()

