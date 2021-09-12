import sqlite3, webbrowser, socket
from datetime import datetime

unit_name = socket.gethostname()

def connect():
    conn = sqlite3.connect(f"{unit_name}_database.db")
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS unit_details (Status text)")
    # cur.execute(f"CREATE TABLE IF NOT EXISTS units (id INTEGER PRIMARY KEY, Name text, Address text, Type text, Status text, last_statrep text)")
    print(f"[{unit_name.upper()}] Database created")
    conn.commit()
    conn.close()
    
def get_own_status():
    
    print(f"[{unit_name.upper()} - DATABASE] checking status")
    conn=sqlite3.connect(f"{unit_name}_database.db")
    cur = conn.cursor()

    cur.execute("SELECT Status from unit_details")
    result = cur.fetchall()
    
    if result:
        print("[{unit_name.upper()} - DATABASE] STATUS:")
        print(result)
        return result # this may need playing with...
    else:
        print(f"[{unit_name.upper()} - DATABASE] Status not found...")
        return "Not found"
    
def update_status(new_status):
    print(f"[{unit_name.upper()} - DATABASE] updating status")
    conn=sqlite3.connect(f"{unit_name}database.db", timeout=10)
    cur=conn.cursor()
    cur.execute(f"UPDATE unit_details SET status=?", (new_status)) 
    conn.commit()
    print(f"[{unit_name.upper()} - DATABASE] Status set to {new_status}")
    conn.close()
    
connect()