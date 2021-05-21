import sqlite3, webbrowser

def connect():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS units (id INTEGER PRIMARY KEY, Name text, Address text, Type text, Status text, last_statrep text)")
    print("[HUB] Database created")
    conn.commit()
    conn.close()
    
def get_unit_status(unitname):
    unitname = unitname.lower()
    print(f"[HUB - DATABASE] checking status of {unitname}")
    conn=sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * from units WHERE Name=?", (unitname,))
    result = cur.fetchall()
    
    if result:
        print(f"[HUB - DATABASE] {unitname} found, status: {result}")
        return result
    else:
        print(f"{unitname} not found, it may not have checked in recently")
    
def get_unit_address(unitname):
    unitname = unitname.lower()
    # print(f"Storage: checking address of {unitname}")
    conn=sqlite3.connect("database.db")
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
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    
    try:
        cur.execute(f"SELECT * FROM units")
        units=cur.fetchall()
        conn.close()
        return units
    except:
        print("not found...")
        return "not found"
    
def get_unit(address):    
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM units WHERE address=?", (address,))
    rows=cur.fetchall()
    conn.close()
    return rows

def check_unit_status(address):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM units WHERE address=?", (address,))
    result=cur.fetchall()
    conn.close()
    return result[0][4] # status
    
def insert(id, name, address, type, status, last_statrep):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO units VALUES (?, ?, ?, ?, ?, ?)", (id, name.lower(), address, type, status, last_statrep))
    conn.commit()
    conn.close()
    
def delete(address):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM units WHERE address=?", (address,)) 
    conn.commit()
    conn.close()

def update_unit(address, status, last_statrep):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute(f"UPDATE units SET status=?, last_statrep=? WHERE address=?", (status, last_statrep, address)) 
    conn.commit()
    conn.close()
    
connect()






    #==========HOW TO CHECK ALL TABLES IN DATABASE==========
    # cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    # print(f"\nENTRY CHECK - Searching tables for: {story}")
    # for tablerow in cur.fetchall():
    #     table = tablerow[0]
    #     cur.execute(f"SELECT * FROM {table} where story=?", (story,))
    #     result = cur.fetchall()
    #     if result:
    #         print(f"Already exists in {table.upper()}")
    #         return True