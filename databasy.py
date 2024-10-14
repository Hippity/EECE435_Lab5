import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''CREATE TABLE users (
                        user_id INTEGER PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        address TEXT NOT NULL,
                        country TEXT NOT NULL);''')  
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print(f'User table creation failed\n{e}')
    finally:
        conn.close()

def insert_user(user):
    inserted_user = {}
    try:
        conn : sqlite3.Connection = connect_to_db()
        cur : sqlite3.Cursor   = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)"
                    ,(user['name'],user['email'],user['phone'],user['address'],user['country'],))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        inserted_user = {}
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

def get_users():
    users = []
    try:
        conn : sqlite3.Connection = connect_to_db()
        conn.row_factory = sqlite3.Row 
        cur : sqlite3.Cursor  = conn.cursor() 
        cur.execute("SELECT * FROM users") 
        rows = cur.fetchall()
        for row in rows:
            user = {}
            user["user_id"] = row["user_id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["phone"] = row["phone"]
            user["address"] = row["address"] 
            user["country"] = row["country"] 
            users.append(user)
    except Exception as e:
        users = []
        print(e)
    finally:
        conn.close()
    return users

def get_user_by_id(user_id):
    user = {}
    try:
        conn : sqlite3.Connection = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur : sqlite3.Cursor  = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?",(user_id,)) 
        row = cur.fetchone()
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"] 
        user["country"] = row["country"] 
    except Exception as e:
        user = {}
        print(e)
    finally:
        conn.close()
    return user

def update_user(user):
    updated_user = {}
    try:
        conn : sqlite3.Connection = connect_to_db()
        cur : sqlite3.Cursor = conn.cursor()
        if get_user_by_id(user['user_id']) == {}:
            raise Exception("User not found in update")
        cur.execute("UPDATE users SET name = ?, email = ?, phone =?, address = ?, country = ? WHERE user_id =?"
                    ,(user['name'],user['email'],user['phone'],user['address'],user['country'],user["user_id"],))

        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        updated_user = {}
        print(e,'jere')
        conn.rollback()
    finally:
        conn.close()
    return updated_user

def delete_user(user_id):
    message = {}
    try:
        conn : sqlite3.Connection = connect_to_db()
        cur : sqlite3.Cursor = conn.cursor()
        if get_user_by_id(user_id) == {}:
            raise Exception("User not found in delete")
        cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        message["status"] = "Cannot delete user"
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return message