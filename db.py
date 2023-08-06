import sqlite3

def setup(filename="tasks.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tasks (tid INTEGER PRIMARY KEY, category TEXT, description TEXT, date TEXT)")
        conn.commit()

def query(sql, filename="tasks.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur=conn.cursor()
        cur.execute(sql)
        conn.commit()
        rows=[]
        try:
            for row in cur.description:
                rows.append(row[0])
        except:
            print("no description")
        return {"rows":cur.fetchall(), "keys":rows}
    
def todict(sql="SELECT * FROM tasks"):
    tasks=query(sql)["rows"]
    keys=["tid","category","description","date"]
    dicts=[]
    for task in tasks:
        values=list(task)
        dic=dict(zip(keys, values))
        dicts.append(dic)
    return dicts

