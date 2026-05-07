import sqlite3
import uuid
import bcrypt

DB_PATH = 'visimind.db'

def create_user():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    user_id = str(uuid.uuid4())
    email = 'test@visimind.local'
    password = 'password123'
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # Check if exists
    c.execute("SELECT id FROM users WHERE email=?", (email,))
    if c.fetchone():
        print("User already exists. Deleting...")
        c.execute("DELETE FROM users WHERE email=?", (email,))
        
    c.execute("""
        INSERT INTO users (id, email, password_hash, company_name, company_url, email_verified)
        VALUES (?, ?, ?, ?, ?, 1)
    """, (user_id, email, hashed, 'Test Company', 'https://testcompany.com'))
    
    # Check if brand profile exists for this user, if not, we can create one or leave it for the UI
    conn.commit()
    conn.close()
    print(f"Created test user: {email} / {password}")

if __name__ == '__main__':
    create_user()
