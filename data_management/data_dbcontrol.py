import sqlite3

def connect():
    conn = sqlite3.connect("data_db.db")
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS test (BSSID TEXT PRIMARY KEY, channel text, power_readings text, ESSID text, maker text, sightings text)")
    print("[DATA - Database] Database created")
    conn.commit()
    conn.close()

def get_all_test():    
    conn=sqlite3.connect("data_db.db")
    cur=conn.cursor()
    
    try:
        cur.execute(f"SELECT * FROM test")
        test=cur.fetchall()
        conn.close()
        return test
    except:
        print("not found...")
        return "not found"
    

    
def insert(bssid, channel, power, essid, maker, sightings):
    conn=sqlite3.connect("data_db.db", timeout=5)
    cur=conn.cursor()
    try:
        cur.execute("INSERT INTO test VALUES (?, ?, ?, ?, ?, ?)", (bssid, channel, power, essid, maker, sightings))
    except:
        raise Exception("exists")
    conn.commit()
    conn.close()
    
def check_device(bssid):
    conn=sqlite3.connect("data_db.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM test WHERE BSSID=?", (bssid,))
    result=cur.fetchall()
    conn.close()
    
    
    if result != []:
        return result
    else:
        return None
    
def delete(bssid):
    conn=sqlite3.connect("data_db.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM test WHERE BSSID=?", (bssid,)) 
    conn.commit()
    conn.close()

def update_device(bssid, channel, power, essid, maker, sightings):
    conn=sqlite3.connect("data_db.db", timeout=10)
    cur=conn.cursor()
    cur.execute(f"UPDATE test SET channel=?, power_readings=?, ESSID=?, maker=?, sightings=? WHERE BSSID=?", (channel, power, essid, maker, sightings, bssid))
    conn.commit()
    conn.close()
    

