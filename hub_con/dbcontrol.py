import sqlite3, webbrowser

def connect():
    conn = sqlite3.connect("hub_db.sqlite3")
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS units (id INTEGER PRIMARY KEY, Name text, Address text, Type text, Status text, last_statrep text, location text)")
    cur.execute(f"CREATE TABLE IF NOT EXISTS authorised_users (id INTEGER PRIMARY KEY, Name text, Type text)") # where id should be telegram chat id or USER id? probably user
    print("[HUB - Database] Database created")
    conn.commit()
    conn.close()
    
    
# ==========UNIT MANAGEMENT DATABASE COMMANDS==========
    
def get_unit_status(unitname):
    unitname = unitname.lower()
    print(f"[HUB - DATABASE] checking status of {unitname}")
    conn=sqlite3.connect("hub_db.sqlite3")
    cur = conn.cursor()

    cur.execute("SELECT * from units WHERE Name=?", (unitname,))
    result = cur.fetchall()
    
    if result:
        # print(f"[HUB - DATABASE] {unitname} found, status: {result}")
        return result[0][4], result[0][5]
    else:
        print(f"{unitname} not found, it may not have checked in recently")
        return "Not found"
    
def get_unit_address(unitname):
    unitname = unitname.lower()
    # print(f"Storage: checking address of {unitname}")
    conn=sqlite3.connect("hub_db.sqlite3")
    cur = conn.cursor()

    cur.execute("SELECT * from units WHERE name=?", (unitname,))
    result = cur.fetchall()
    conn.close()
    
    if result:
        # print(f"{unitname} found: {result}")
        return result[0][2]
    else:
        print(f"[HUB - DATABASE] {unitname} not found, it may not have checked in recently")
        
def get_all_units():    
    conn=sqlite3.connect("hub_db.sqlite3")
    cur=conn.cursor()
    
    try:
        cur.execute(f"SELECT * FROM units")
        units=cur.fetchall()
        conn.close()
        return units
    except:
        print("not found...")
        return "not found"
    
def get_unit_name(address):    
    conn=sqlite3.connect("hub_db.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT * FROM units WHERE address=?", (address,))
    rows=cur.fetchall()
    conn.close()
    return rows[0][1]

def check_unit_status(address):
    conn=sqlite3.connect("hub_db.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT * FROM units WHERE address=?", (address,))
    result=cur.fetchall()
    conn.close()
    return result[0][4] # status
    
def insert(id, name, address, type, status, last_statrep, location):
    conn=sqlite3.connect("hub_db.sqlite3", timeout=5)
    cur=conn.cursor()
    cur.execute("INSERT INTO units VALUES (?, ?, ?, ?, ?, ?, ?)", (id, name.lower(), address, type, status, last_statrep, location))
    conn.commit()
    conn.close()
    
def delete(address):
    conn=sqlite3.connect("hub_db.sqlite3")
    cur=conn.cursor()
    cur.execute("DELETE FROM units WHERE address=?", (address,)) 
    conn.commit()
    conn.close()

def update_unit(address, status, last_statrep):
    conn=sqlite3.connect("hub_db.sqlite3", timeout=10)
    cur=conn.cursor()
    cur.execute(f"UPDATE units SET status=?, last_statrep=? WHERE address=?", (status, last_statrep, address)) 
    conn.commit()
    conn.close()
    
# ==========AUTHORISED USER DATABASE COMMANDS==========

def add_authorised_user(id, name, type):
    conn=sqlite3.connect("hub_db.sqlite3", timeout=5)
    cur=conn.cursor()
    cur.execute("INSERT INTO authorised_users VALUES (?, ?, ?)", (id, name.lower(), type))
    conn.commit()
    conn.close()
    
def check_user(id):
    conn=sqlite3.connect("hub_db.sqlite3")
    cur=conn.cursor()
    cur.execute("SELECT * FROM authorised_users WHERE id=?", (id,))
    result=cur.fetchall()
    conn.close()
    
    print(result)
    
    if result != []:
        return result[0][2]
    else:
        return None
    
def get_all_users():    
    conn=sqlite3.connect("hub_db.sqlite3")
    cur=conn.cursor()
    
    try:
        cur.execute(f"SELECT * FROM authorised_users")
        users=cur.fetchall()
        conn.close()
        return users
    except:
        print("not found...")
        return "not found"
    

if __name__ == '__main__':
    connect()

